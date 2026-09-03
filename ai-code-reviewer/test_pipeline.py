from dotenv import load_dotenv
from src.agents.graph import build_review_graph
from src.agents.state import CodeReviewState

load_dotenv()

buggy_code = """
def process_user_data(data):
    # Undefined variable and potential divide by zero
    val = data["count"]
    result = total / val
    return result
"""

initial_state: CodeReviewState = {
    "file_path": "pipeline_test.py",
    "original_code": buggy_code,
    "language": "python",
    "ast_data": None,
    "syntax_errors": [],
    "detected_bugs": [],
    "messages": [],
    "fixed_code": None,
    "diff": None,
    "verification_passed": False,
    "retry_count": 0,
}

print("🚀 Executing Full Multi-Agent LangGraph Pipeline...")
app = build_review_graph()
final_state = app.invoke(initial_state)

print("\n--- Pipeline Logs ---")
for msg in final_state["messages"]:
    print("•", msg)

print("\n--- Final Fixed Code ---")
print(final_state["fixed_code"])

print("\n--- Final Unified Diff ---")
print(final_state["diff"])

print("\nVerification Status:", final_state["verification_passed"])
print("\n[SUCCESS]: Full Agent Graph compiled and executed cleanly!")
