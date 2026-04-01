import os
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from agent.state import AgentState, ClassifierOutput, PlannerOutput
from agent.tools import PLANNER_TOOL_SCHEMAS, GENERATOR_TOOL_SCHEMAS, execute_tool
from agent.prompts import (
    CLASSIFIER_SYSTEM_PROMPT,
    PLANNER_SYSTEM_PROMPT,
    GENERATOR_SYSTEM_PROMPT,
)

import json

# ── LLM 초기화 ──────────────────────────────────────────────

_llm = init_chat_model("openai:gpt-4o", temperature=0)

# Classifier: 구조화 출력 강제
_classifier_llm = _llm.with_structured_output(ClassifierOutput)

# Planner: Tool Calling 필요
_planner_llm = _llm.bind_tools(PLANNER_TOOL_SCHEMAS)

# Generator: read_skill Tool Calling
_generator_llm = _llm.bind_tools(GENERATOR_TOOL_SCHEMAS)


# ══════════════════════════════════════════════════════════════
# Node 1: Classifier
# ══════════════════════════════════════════════════════════════

def run_classifier(state: AgentState) -> dict:
    """use case 분류 + 한 줄 요약"""

    messages = [
        SystemMessage(content=CLASSIFIER_SYSTEM_PROMPT),
        HumanMessage(content=state["messages"][-1].content),
    ]

    result = _classifier_llm.invoke(messages)

    return {
        "use_case":   result["use_case"],
        "types":      result["types"],
        "confidence": result["confidence"],
    }


# ══════════════════════════════════════════════════════════════
# Node 2: Planner (Tool Calling 루프)
# ══════════════════════════════════════════════════════════════

def run_planner(state: AgentState) -> dict:
    """features, steps 결정 + 필요시 Tool 호출"""

    planner_input = json.dumps({
        "user_input": state.get("use_case", ""),
        "types":      state.get("types", []),
    }, ensure_ascii=False)

    messages = [
        SystemMessage(content=PLANNER_SYSTEM_PROMPT),
        HumanMessage(content=planner_input),
    ]

    MAX_ITERATIONS = 5
    for _ in range(MAX_ITERATIONS):
        response = _planner_llm.invoke(messages)
        messages.append(response)

        # Tool 호출 없으면 최종 답변
        if not response.tool_calls:
            break

        # Tool 실행
        for tool_call in response.tool_calls:
            tool_result = execute_tool(
                tool_call["name"],
                tool_call["args"],
            )
            messages.append(
                ToolMessage(
                    content=tool_result,
                    tool_call_id=tool_call["id"],
                )
            )

    # 마지막 응답에서 JSON 파싱
    raw = response.content.strip()
    try:
        if "```" in raw:
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        data: PlannerOutput = json.loads(raw.strip())
    except json.JSONDecodeError:
        return {"error": f"Planner 파싱 실패: {raw}"}

    return {
        "features": data["features"],
        "steps":    data["steps"],
        "reasoning": data.get("reasoning", ""),
    }


# ══════════════════════════════════════════════════════════════
# Node 3: Generator (Tool Calling 루프)
# ══════════════════════════════════════════════════════════════

def run_generator(state: AgentState) -> dict:
    """steps별 Skill 파일을 read_skill로 읽으면서 구현 가이드 생성"""

    generator_input = json.dumps({
        "user_input": state.get("use_case", ""),
        "features":  state.get("features", []),
        "steps":     state.get("steps", []),
    }, ensure_ascii=False)

    messages = [
        SystemMessage(content=GENERATOR_SYSTEM_PROMPT),
        HumanMessage(content=generator_input),
    ]

    MAX_ITERATIONS = 10  # step 수 * 2 (skill 파일 + 하위 파일)
    for _ in range(MAX_ITERATIONS):
        response = _generator_llm.invoke(messages)
        messages.append(response)

        # Tool 호출 없으면 최종 가이드 완성
        if not response.tool_calls:
            break

        # read_skill tool 실행
        for tool_call in response.tool_calls:
            tool_result = execute_tool(
                tool_call["name"],
                tool_call["args"],
            )
            messages.append(
                ToolMessage(
                    content=tool_result,
                    tool_call_id=tool_call["id"],
                )
            )

    guide = response.content.strip()

    return {
        "guide":    guide,
        "messages": [{"role": "assistant", "content": guide}],
    }


# ══════════════════════════════════════════════════════════════
# Graph 구성
# ══════════════════════════════════════════════════════════════

memory = MemorySaver()

builder = StateGraph(AgentState)
builder.add_node("classifier", run_classifier)
builder.add_node("planner",    run_planner)
builder.add_node("generator",  run_generator)

builder.add_edge(START,        "classifier")
builder.add_edge("classifier", "planner")
builder.add_edge("planner",    "generator")
builder.add_edge("generator",  END)

graph = builder.compile(checkpointer=memory)