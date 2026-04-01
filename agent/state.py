from typing import Optional
from langgraph.graph import MessagesState
from typing_extensions import TypedDict


class AgentState(MessagesState):
    use_case: Optional[str]

    # Classifier 출력
    types: Optional[list[str]]
    confidence: Optional[float]

    # Planner 출력
    features: Optional[list[str]]
    steps: Optional[list[str]]
    reasoning: Optional[str]

    # Generator 출력
    guide: Optional[str]

    # 에러
    error: Optional[str]


class ClassifierOutput(TypedDict):
    use_case: str
    types: list[str]
    confidence: float


class PlannerOutput(TypedDict):
    features: list[str]
    steps: list[str]
    reasoning: str


# #1.classifier output
# output: ["Agent Task", "AI Generation", "Data Update"]


# #2.planner output
# Output:
# {
#   "features": ["Setup", "Layout", "Prompt Template", "Flow"],
#   "reasoning": "Single object automation with AI generation can be handled by Flow and Prompt Template.",
#   "steps": ["Setup", "Layout", "Prompt Template", "Flow"]
# }

# #3.generator output
# Output Format:
# Return in structured markdown:

# # 구현 가이드

# ## Step 1: {{Step Name}}
# {{detailed guide}}

# ## Step 2: {{Step Name}}
# {{detailed guide}}

# ...