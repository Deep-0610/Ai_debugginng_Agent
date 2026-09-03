from src.utils.linter import run_ruff_linter

# Unused import (F401) + Undefined variable (F821)
bad_code = """
import os
import sys

def compute():
    return x + 10
"""

clean_code = """
def compute(x: int) -> int:
    return x + 10
"""

print("--- Testing Code with Lint Errors ---")
linter_res = run_ruff_linter(bad_code)
print("Lint Issues Found:", linter_res["issue_count"])
for issue in linter_res["issues"]:
    print(" -", issue)

print("\n--- Testing Clean Code ---")
clean_res = run_ruff_linter(clean_code)
print("Clean Code Passed:", clean_res["passed"])

assert linter_res["issue_count"] > 0, "Linter failed to detect issues"
assert clean_res["passed"] is True, "Clean code failed linter check"

print("\n[SUCCESS]: Ruff Linter Integration verified!")
