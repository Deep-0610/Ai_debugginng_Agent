import os
from dotenv import load_dotenv
from src.agents.state import CodeReviewState
from src.agents.reviewer import analyze_code_node
from src.agents.patcher import generate_patch_node

load_dotenv()

buggy_python_code = """
def find_average(numbers):
    total = 0
    for i in range(len(numbers)):
        total += numbers[i]
    return total / len(numbers)
"""

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
    "retry_count": 0,
}

print("🚀 Step 1: Running Bug Detection Node...")
state = analyze_code_node(state)

print("🛠️ Step 2: Running Patch Generator Node...")
state = generate_patch_node(state)

print("\n--- GENERATED FIX ---")
print(state["fixed_code"])

print("\n--- UNIFIED DIFF ---")
print(state["diff"])

assert state["fixed_code"] is not None, "Failed to generate fixed code"
assert state["diff"] != "", "Failed to generate unified diff"

print("\n[SUCCESS]: Patch Generator Node executed successfully!")
