from langgraph.graph import StateGraph, END
from src.agents.state import CodeReviewState
from src.agents.reviewer import analyze_code_node
from src.agents.patcher import generate_patch_node
from src.agents.verifier import verify_patch_node


def should_retry(state: CodeReviewState) -> str:
    """
    Conditional Routing Function:
    - If verification passes, end the pipeline.
    - If verification fails and retries remain (< 3), loop back to patcher.
    - Otherwise, terminate.
    """
    if state.get("verification_passed", False):
        return "end"

    if state.get("retry_count", 0) < 3:
        return "patch"

    return "end"


def build_review_graph():
    """
    Constructs and compiles the multi-agent execution pipeline.
    """
    workflow = StateGraph(CodeReviewState)

    # 1. Add Nodes
    workflow.add_node("analyze", analyze_code_node)
    workflow.add_node("patch", generate_patch_node)
    workflow.add_node("verify", verify_patch_node)

    # 2. Define Sequential Flow
    workflow.set_entry_point("analyze")
    workflow.add_edge("analyze", "patch")
    workflow.add_edge("patch", "verify")

    # 3. Define Conditional Loop Routing
    workflow.add_conditional_edges(
        "verify", should_retry, {"patch": "patch", "end": END}
    )

    return workflow.compile()
