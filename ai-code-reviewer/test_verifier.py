from src.agents.state import CodeReviewState
from src.agents.verifier import verify_patch_node

# Valid fixed code
clean_patch_state: CodeReviewState = {
    "file_path": "math_utils.py",
    "original_code": "def find_average(numbers):\n    return sum(numbers) / len(numbers)",
    "language": "python",
    "ast_data": None,
    "syntax_errors": [],
    "detected_bugs": [],
    "messages": [],
    "fixed_code": "def find_average(numbers):\n    if not numbers:\n        return 0\n    return sum(numbers) / len(numbers)",
    "diff": None,
    "verification_passed": False,
    "retry_count": 0,
}

print("🚀 Testing Verification Node on Clean Fix...")
verified_state = verify_patch_node(clean_patch_state)

print("Verification Passed:", verified_state["verification_passed"])
print("Latest Log:", verified_state["messages"][-1])

assert (
    verified_state["verification_passed"] is True
), "Verifier rejected a valid code patch!"

print("\n[SUCCESS]: Verification Node verified!")
