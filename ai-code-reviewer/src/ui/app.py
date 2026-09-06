import os
import re
import requests
import streamlit as st
import pandas as pd
from typing import Dict, Any, Tuple

# Page Configuration
st.set_page_config(
    page_title="AI Code Reviewer & Debugger",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS Styling
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E88E5;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #666666;
        margin-bottom: 1.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def fetch_github_file(url_or_path: str, token: str = "") -> Tuple[str, str]:
    """
    Fetches raw code content from a GitHub file URL or 'owner/repo/filepath' format.
    Returns a tuple of (file_content, detected_language).
    """
    # Standardize blob/raw GitHub URLs
    url = url_or_path.strip()
    if "github.com" in url:
        url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            # Auto-detect language based on file extension
            ext = url.split(".")[-1].lower()
            ext_map = {
                "py": "Python", "js": "JavaScript", "ts": "TypeScript",
                "c": "C", "cpp": "C++", "java": "Java", "go": "Go",
                "rs": "Rust", "sql": "SQL", "html": "HTML", "css": "CSS"
            }
            detected_lang = ext_map.get(ext, "Python")
            return response.text, detected_lang
        else:
            st.error(f"Failed to fetch GitHub file. HTTP Status: {response.status_code}")
            return "", "Python"
    except Exception as e:
        st.error(f"Error fetching from GitHub: {str(e)}")
        return "", "Python"


def mock_ai_code_reviewer(code: str, language: str, mode: str) -> Dict[str, Any]:
    """
    Placeholder/Fallback reviewer function.
    Replace this with your backend AI agent pipeline (e.g. LangChain / OpenAI).
    """
    return {
        "status": "success",
        "bugs_found": [
            {"line": 2, "issue": "Unbound variable risks runtime crash.", "severity": "High"},
            {"line": 5, "issue": "Missing error check on response payload.", "severity": "Medium"}
        ],
        "refactored_code": f"# Refactored {language} Code ({mode} Mode)\n\n" + code,
        "explanation": f"1. Optimized syntax for {language}.\n2. Added exception handling and edge-case guards.\n3. Followed standard linting standards.",
        "complexity": {"Before": "O(N^2)", "After": "O(N)"}
    }


def main():
    # --- Sidebar Configuration ---
    st.sidebar.title("⚙️ Settings & Keys")
    
    # API Keys
    openai_key = st.sidebar.text_input(
        "OpenAI / Agent API Key",
        type="password",
        value=os.getenv("OPENAI_API_KEY", ""),
        help="API Key for AI analysis."
    )
    
    github_token = st.sidebar.text_input(
        "GitHub Access Token (Optional)",
        type="password",
        value=os.getenv("GITHUB_TOKEN", ""),
        help="Optional: Needed for fetching from private GitHub repositories."
    )

    st.sidebar.markdown("---")
    st.sidebar.title("🛠 Review Options")
    
    review_mode = st.sidebar.radio(
        "Analysis Mode",
        ["Comprehensive", "Bug Fixes Only", "Performance & Refactoring", "Security Audit"],
        index=0
    )

    # --- Main Header ---
    st.markdown('<div class="main-header">🤖 AI Code Reviewer & Debugging Agent</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Fetch code directly from GitHub or paste snippets to perform automated debugging, security checks, and code cleanup.</div>', unsafe_allow_html=True)

    col_input, col_output = st.columns([1, 1], gap="medium")

    # Left Column: Inputs
    with col_input:
        st.subheader("📥 Input Source")
        
        input_source = st.radio("Choose Input Method:", ["Paste Code", "Fetch from GitHub"], horizontal=True)

        user_code = ""
        selected_language = "Python"

        if input_source == "Fetch from GitHub":
            default_url = "https://github.com/Deep-0610/Ai_debugginng_Agent/blob/main/ai-code-reviewer/src/ui/app.py"
            repo_url = st.text_input("GitHub File URL:", value=default_url)
            
            if st.button("📥 Fetch Code from GitHub", use_container_width=True):
                if repo_url:
                    fetched_code, detected_lang = fetch_github_file(repo_url, github_token)
                    if fetched_code:
                        st.session_state["fetched_code"] = fetched_code
                        st.session_state["detected_lang"] = detected_lang
                        st.success("Successfully loaded repository code!")

            user_code = st.session_state.get("fetched_code", "")
            detected_lang = st.session_state.get("detected_lang", "Python")
            
            lang_list = ["Python", "JavaScript", "TypeScript", "C", "C++", "Java", "Go", "Rust", "SQL"]
            default_index = lang_list.index(detected_lang) if detected_lang in lang_list else 0
            selected_language = st.selectbox("Detected Language:", lang_list, index=default_index)

            user_code = st.text_area("Preview / Edit Fetched Code:", value=user_code, height=300)

        else:
            selected_language = st.selectbox(
                "Programming Language:",
                ["Python", "JavaScript", "TypeScript", "C", "C++", "Java", "Go", "Rust", "SQL"]
            )
            sample_code = "def process_data(items):\n    for i in range(len(items)):\n        print(items[i])"
            user_code = st.text_area("Paste Code Snippet:", value=sample_code, height=380)

        btn_analyze = st.button("🚀 Run AI Analysis", type="primary", use_container_width=True)

    # Right Column: Output
    with col_output:
        st.subheader("📊 Review & Debug Results")

        if btn_analyze:
            if not user_code.strip():
                st.warning("⚠️ Please provide code either by pasting or fetching from GitHub.")
                return

            with st.spinner("Analyzing code base with AI agent..."):
                try:
                    # Run backend analysis
                    results = mock_ai_code_reviewer(user_code, selected_language, review_mode)

                    st.success("Analysis Completed!")

                    # Results Tabs
                    tab_summary, tab_code, tab_bugs = st.tabs(["📋 Analysis Summary", "⚡ Refactored Code", "🐞 Detected Issues"])

                    with tab_summary:
                        st.markdown("### Explanation & Recommendations")
                        st.markdown(results["explanation"])

                        st.markdown("#### Complexity Metrics")
                        m1, m2 = st.columns(2)
                        m1.metric("Current Time Complexity", results["complexity"]["Before"])
                        m2.metric("Optimized Time Complexity", results["complexity"]["After"])

                    with tab_code:
                        st.markdown("### Proposed Fix")
                        refactored = results["refactored_code"]
                        st.code(refactored, language=selected_language.lower())

                        st.download_button(
                            label="📥 Download Clean Code",
                            data=refactored,
                            file_name=f"cleaned_code.{selected_language.lower()}",
                            mime="text/plain"
                        )

                    with tab_bugs:
                        st.markdown("### Bug & Vulnerability Breakdown")
                        bugs_df = pd.DataFrame(results["bugs_found"])
                        st.dataframe(bugs_df, use_container_width=True)

                except Exception as err:
                    st.error(f"Failed to analyze code: {str(err)}")
        else:
            st.info("👈 Enter a GitHub URL or paste code on the left, then click **Run AI Analysis**.")


if __name__ == "__main__":
    main()
