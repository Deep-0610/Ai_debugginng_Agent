from src.agents.state import CodeReviewState

# Instantiate a mock state dictionary
initial_state: CodeReviewState = {
    "file_path": "example.py",
    "original_code": "def add(a, b):\n return a + b",
    "language": "python",
    "ast_data": None,
    "syntax_errors": [],
    "detected_bugs": [],
    "messages": ["Initialization complete."],
    "fixed_code": None,
    "diff": None,
    "verification_passed": False,
    "retry_count": 0,
}

print("[SUCCESS]: CodeReviewState schema verified!")
print("Initial File Target:", initial_state["file_path"])
