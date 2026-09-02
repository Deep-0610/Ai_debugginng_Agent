import os
import json
from groq import Groq
from src.agents.state import CodeReviewState
from src.parsers.tree_sitter_parser import parse_code_structure
from src.utils.linter import run_ruff_linter

def analyze_code_node(state: CodeReviewState) -> CodeReviewState:
    """
    LangGraph Node: Collects static analysis and uses LLM to identify 
    logical bugs, security flaws, and performance anti-patterns.
    """
    code = state["original_code"]
    lang = state.get("language", "python")

    # 1. Run Static Tools
    ast_res = parse_code_structure(code, lang)
    lint_res = run_ruff_linter(code)

    # Update state with static analysis
    state["ast_data"] = ast_res
    state["syntax_errors"] = ast_res.get("syntax_errors", [])

    # 2. Query LLM for Logical Bugs
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    # Retrieve model IDs and exclude non-chat endpoints
    models_page = client.models.list()
    excluded_keywords = ["whisper", "guard", "embed", "vision", "compound", "canopylabs"]
    
    chat_models = [
        m.id for m in models_page.data 
        if not any(keyword in m.id.lower() for keyword in excluded_keywords)
    ]
    
    if not chat_models:
        raise ValueError("No valid chat model found in Groq account.")

    target_model = chat_models[0]
    print(f"🔍 Reviewer Agent using model: '{target_model}'")

    prompt = f"""
    You are an expert AI code auditor. Review the following {lang} code.
    
    STATIC LINTING ISSUES:
    {json.dumps(lint_res.get('issues', []), indent=2)}
    
    EXTRACTED AST METADATA:
    Functions: {ast_res.get('functions', [])}
    Classes: {ast_res.get('classes', [])}
    
    SOURCE CODE:
    ```{lang}
    {code}
    ```

    Identify any logical bugs, potential edge-case failures, or performance issues. 
    Provide your analysis as a concise summary.
    """

    response = client.chat.completions.create(
        model=target_model,
        messages=[{"role": "user", "content": prompt}]
    )

    review_output = response.choices[0].message.content

    # Update state history and bugs list
    state["messages"].append("[Reviewer Node]: Analysis complete.")
    state["detected_bugs"] = [{
        "linter_issues": lint_res.get("issues", []),
        "llm_analysis": review_output
    }]

    return state