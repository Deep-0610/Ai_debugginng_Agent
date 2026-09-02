from src.agents.state import CodeReviewState
from src.parsers.tree_sitter_parser import parse_code_structure
from src.utils.linter import run_ruff_linter

def verify_patch_node(state: CodeReviewState) -> CodeReviewState:
    """
    LangGraph Node: Validates generated patch code using AST parsing 
    and pyflakes linting to ensure no new errors were introduced.
    """
    fixed_code = state.get("fixed_code")
    lang = state.get("language", "python")

    if not fixed_code:
        state["verification_passed"] = False
        state["messages"].append("[Verifier Node]: Failed - No fixed code found.")
        return state

    # 1. Run AST verification on the fix
    ast_res = parse_code_structure(fixed_code, lang)
    
    # 2. Run static linting on the fix
    lint_res = run_ruff_linter(fixed_code)

    is_valid_ast = ast_res.get("is_valid", False)
    is_clean_lint = lint_res.get("passed", False)

    if is_valid_ast and is_clean_lint:
        state["verification_passed"] = True
        state["messages"].append("[Verifier Node]: Verification PASSED. Patch is clean.")
    else:
        state["verification_passed"] = False
        state["retry_count"] = state.get("retry_count", 0) + 1
        errors = ast_res.get("syntax_errors", []) + lint_res.get("issues", [])
        state["messages"].append(f"[Verifier Node]: Verification FAILED. Issues: {errors}")

    return state