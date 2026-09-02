from typing import TypedDict, List, Dict, Any, Optional, Annotated
import operator

class CodeReviewState(TypedDict):
    """
    State schema for the Autonomous AI Code Reviewer & Bug Fixer Agent.
    """
    # Core Code Details
    file_path: str
    original_code: str
    language: str
    
    # AST Analysis (Tree-sitter output)
    ast_data: Optional[Dict[str, Any]]
    
    # Bug Detection & Linting Results
    syntax_errors: List[str]
    detected_bugs: List[Dict[str, Any]]
    
    # Cumulative Conversation / Agent Logs
    # Using operator.add to append logs/messages instead of overwriting
    messages: Annotated[List[str], operator.add]
    
    # Patch Generation & Verification
    fixed_code: Optional[str]
    diff: Optional[str]
    verification_passed: bool
    retry_count: int