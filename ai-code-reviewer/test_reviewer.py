import os
from dotenv import load_dotenv
from src.agents.state import CodeReviewState
from src.agents.reviewer import analyze_code_node

load_dotenv()

# Sample code containing a logical off-by-one error
buggy_python_code = """
def find_average(numbers):
    total = 0
    for i in range(len(numbers)):
        total += numbers[i]
    # Bug: Division by zero risk + wrong average logic if empty
    return total / len(numbers)
"""

# Define initial state
state: CodeReviewState = {
    "file_path": "math_utils.py",
    "original_code": buggy_python_code,
    "language": "python",
    "ast_data": None,
    "syntax_errors": [],
    "detected_bugs": [],
    "messages": [],
    "fixed_code": None,
    "diff": None,
    "verification_passed": False,
    "retry_count": 0
}

print("🚀 Running Bug Detection Node...")
updated_state = analyze_code_node(state)

print("\n--- LLM Review Summary ---")
print(updated_state["detected_bugs"][0]["llm_analysis"])
print("\n[SUCCESS]: Bug Detection Node executed successfully!")