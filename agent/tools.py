import json
from pathlib import Path
from langchain_tavily import TavilySearch
from salesforce_client import SalesforceClient

sf_client = SalesforceClient()
SKILLS_DIR = Path(__file__).parent.parent / "skills"

_tavily = TavilySearch(
    max_results=3,
    include_domains=[
        "trailhead.salesforce.com",
        "help.salesforce.com",
        "howtoagentforce.com",
        "github.com",
    ],
)

# ── Tool 실행 함수 ──────────────────────────────────────────

def search(query: str) -> str:
    results = _tavily.invoke(query)
    return str(results)


def get_objects() -> str:
    objects = sf_client.get_core_objects()
    return json.dumps(objects, ensure_ascii=False)


def describe_object(object_name: str) -> str:
    result = sf_client.describe_object(object_name)
    return json.dumps(result, ensure_ascii=False)


def get_prompt_templates() -> str:
    templates = sf_client.get_prompt_templates()
    return json.dumps(templates, ensure_ascii=False)


def read_skill(skill_name: str) -> str:
    """Skill 파일을 읽어서 반환한다."""
    # 허용된 파일 목록 (경로 traversal 방지)
    allowed = {
        "setup_skill.md",
        "layout_skill.md",
        "prompt_skill.md",
        "flow_skill.md",
        "apex_skill.md",
        "agent_skill.md",
        "prompt_type/field_generation.md",
        "prompt_type/flex.md",
        "prompt_type/sales_email.md",
    }
    if skill_name not in allowed:
        return f"허용되지 않은 skill 파일: {skill_name}"
    path = SKILLS_DIR / skill_name
    if not path.exists():
        return f"파일 없음: {skill_name}"
    return path.read_text(encoding="utf-8")


# ── Tool Schema ──────────────────────────────────────────────

# Planner용 (Salesforce 메타데이터 조회 + 검색)
PLANNER_TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": (
                "Salesforce 관련 최신 정보를 검색한다. "
                "구현 방법, 기능 제약, UI 경로, 최신 기능이 필요할 때 사용한다."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "검색 쿼리"}
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_objects",
            "description": (
                "현재 Salesforce Org의 핵심 객체 목록(이름, 레이블)을 반환한다. "
                "사용자 요청과 관련된 객체를 파악할 때 사용한다."
            ),
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "describe_object",
            "description": (
                "특정 Salesforce 객체의 필드 목록(이름, 레이블, 타입)을 반환한다. "
                "시나리오 설계 시 사용 가능한 필드를 파악할 때 사용한다."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "object_name": {
                        "type": "string",
                        "description": "Salesforce 객체 API 이름 (예: Account, Contact)",
                    }
                },
                "required": ["object_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_prompt_templates",
            "description": (
                "현재 Salesforce Org에 등록된 Custom Prompt Template 목록을 반환한다. "
                "시나리오 설계 시 기존 템플릿 재활용 가능 여부를 판단할 때 사용한다."
            ),
            "parameters": {"type": "object", "properties": {}},
        },
    },
]

# Generator용 (Skill 파일 읽기)
GENERATOR_TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "read_skill",
            "description": (
                "구현 가이드 작성에 필요한 Skill 파일을 읽는다. "
                "각 step에 해당하는 Skill 파일을 반드시 읽은 후 가이드를 작성한다. "
                "사용 가능한 파일: setup_skill.md / layout_skill.md / prompt_skill.md / "
                "flow_skill.md / apex_skill.md / agent_skill.md / "
                "prompt_type/field_generation.md / prompt_type/flex.md / prompt_type/sales_email.md"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "skill_name": {
                        "type": "string",
                        "description": "읽을 Skill 파일명 (예: setup_skill.md, prompt_type/field_generation.md)",
                    }
                },
                "required": ["skill_name"],
            },
        },
    },
]

# 하위 호환성 유지
TOOL_SCHEMAS = PLANNER_TOOL_SCHEMAS

# ── Tool 실행 디스패처 ──────────────────────────────────────

TOOL_MAP = {
    "search": lambda args: search(args["query"]),
    "get_objects": lambda args: get_objects(),
    "describe_object": lambda args: describe_object(args["object_name"]),
    "get_prompt_templates": lambda args: get_prompt_templates(),
    "read_skill": lambda args: read_skill(args["skill_name"]),
}


def execute_tool(name: str, args: dict) -> str:
    fn = TOOL_MAP.get(name)
    if not fn:
        return f"알 수 없는 tool: {name}"
    try:
        return fn(args)
    except Exception as e:
        return f"Tool 실행 오류: {str(e)}"