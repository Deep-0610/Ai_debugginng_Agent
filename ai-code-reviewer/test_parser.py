from src.parsers.tree_sitter_parser import parse_code_structure

sample_buggy_code = """
def calculate_total(price, tax):
    return price + 
"""

sample_valid_code = """
class Calculator:
    def add(self, a, b):
        return a + b
"""

print("--- Testing Invalid Code ---")
invalid_res = parse_code_structure(sample_buggy_code, "python")
print("Syntax Errors Found:", invalid_res["syntax_errors"])

print("\n--- Testing Valid Code ---")
valid_res = parse_code_structure(sample_valid_code, "python")
print("Functions Extracted:", valid_res["functions"])
print("Classes Extracted:", valid_res["classes"])

assert len(invalid_res["syntax_errors"]) > 0, "Parser failed to catch syntax error"
assert "Calculator" in valid_res["classes"], "Parser failed to extract class"

print("\n[SUCCESS]: Parser node functionality verified!")