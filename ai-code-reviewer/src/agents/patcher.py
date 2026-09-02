import os
import difflib
from groq import Groq
from src.agents.state import CodeReviewState

def generate_patch_node(state: CodeReviewState) -> CodeReviewState:
    """
    LangGraph Node: Takes detected bugs and original code to generate 
    a corrected code version and computes the unified diff.
    """
    original_code = state["original_code"]
    lang = state.get("language", "python")
    bugs_data = state.get("detected_bugs", [])

    analysis_summary = bugs_data[0]["llm_analysis"] if bugs_data else "No issues identified."

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    # Filter for active chat models
    models_page = client.models.list()
    excluded_keywords = ["whisper", "guard", "embed", "vision", "compound", "canopylabs"]
    chat_models = [
        m.id for m in models_page.data 
        if not any(keyword in m.id.lower() for keyword in excluded_keywords)
    ]
    target_model = chat_models[0]

    prompt = f"""
    You are an expert automated code fixer. Fix all bugs and issues described in the audit summary.

    AUDIT SUMMARY:
    {analysis_summary}

    ORIGINAL CODE:
    ```{lang}
    {original_code}
    ```

    CRITICAL INSTRUCTIONS:
    - Return ONLY the executable, corrected {lang} code.
    - Do NOT wrap code in markdown code blocks (do not use ```).
    - Do NOT include introductory text, explanations, or comments before/after the code.
    """

    response = client.chat.completions.create(
        model=target_model,
        messages=[{"role": "user", "content": prompt}]
    )

    fixed_code = response.choices[0].message.content.strip()

    # Clean potential stray markdown formatting if LLM includes it
    if fixed_code.startswith("```"):
        lines = fixed_code.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        fixed_code = "\n".join(lines).strip()

    # Calculate Unified Diff
    orig_lines = original_code.splitlines(keepends=True)
    fixed_lines = fixed_code.splitlines(keepends=True)
    diff_generator = difflib.unified_diff(
        orig_lines, 
        fixed_lines, 
        fromfile="a/" + state.get("file_path", "target.py"), 
        tofile="b/" + state.get("file_path", "target.py")
    )
    computed_diff = "".join(diff_generator)

    # Update State
    state["fixed_code"] = fixed_code
    state["diff"] = computed_diff
    state["messages"].append("[Patcher Node]: Fix applied and diff generated.")

    return state