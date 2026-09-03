import ast
from typing import Dict, Any, List


def parse_code_structure(code_content: str, language: str = "python") -> Dict[str, Any]:
    """
    Parses code string to extract structural metadata (functions, classes, imports)
    and detect raw syntax errors prior to agent processing.
    """
    syntax_errors: List[str] = []
    functions: List[str] = []
    classes: List[str] = []

    if language.lower() == "python":
        try:
            tree = ast.parse(code_content)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)
        except SyntaxError as se:
            syntax_errors.append(f"Line {se.lineno}: {se.msg}")
        except Exception as e:
            syntax_errors.append(str(e))

    return {
        "is_valid": len(syntax_errors) == 0,
        "functions": functions,
        "classes": classes,
        "syntax_errors": syntax_errors,
    }
