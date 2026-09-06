import os
import streamlit as st
import pandas as pd
from typing import Dict, Any

# Page Configuration
st.set_page_config(
    page_title="AI Code Reviewer & Debugger",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E88E5;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #555555;
        margin-bottom: 1.5rem;
    }
    .stCodeBlock {
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=False,
)


def mock_ai_code_reviewer(code: str, language: str, analysis_type: str) -> Dict[str, Any]:
    """
    Placeholder/Fallback reviewer function.
    Replace or integrate this with your backend agent logic (e.g., LangChain/LlamaIndex/OpenAI agent).
    """
    # Import your custom agent logic here if available:
    # from src.agent.reviewer import analyze_code
    
    return {
        "status": "success",
        "bugs_found": [
            {"line": 1, "issue": "Potential missing type hints.", "severity": "Low"},
            {"line": 3, "issue": "Unhandled edge case for null/empty input.", "severity": "Medium"}
        ],
        "refactored_code": f"# Refactored {language} Code\n" + code + "\n\n# Optimized for performance & safety",
        "explanation": "1. Added type safety checks.\n2. Improved error handling.\n3. Followed PEP8/best-practice conventions.",
        "complexity": {"Before": "O(N^2)", "After": "O(N)"}
    }


def main():
    # --- Sidebar Configuration ---
    st.sidebar.title("⚙️ Configuration")
    
    # API Key Handling
    api_key = st.sidebar.text_input(
        "API Key (OpenAI / Anthropic)",
        type="password",
        help="Enter your API key to run the agent.",
        value=os.getenv("OPENAI_API_KEY", "")
    )
    
    language = st.sidebar.selectbox(
        "Programming Language",
        ["Python", "JavaScript", "TypeScript", "C++", "Java", "Go", "Rust", "SQL"],
        index=0
    )
    
    review_mode = st.sidebar.radio(
        "Review Mode",
        ["Comprehensive", "Bug Fixes Only", "Performance & Refactoring", "Security Audit"],
        index=0
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info(
        "💡 **Tip:** Select specific modes to tailor the debugging depth and response structure."
    )

    # --- Main UI Content ---
    st.markdown('<div class="main-header">🤖 AI Code Reviewer & Debugging Agent</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Paste your code below to analyze bugs, security risks, performance bottlenecks, and automated refactoring.</div>',
        unsafe_allow_html=True
    )

    col_input, col_output = st.columns([1, 1], gap="medium")

    # Left Column: Input Code
    with col_input:
        st.subheader("📝 Source Code")
        
        sample_code = """def calculate_total(items):
    total = 0
    for item in items:
        total += item['price'] * item['quantity']
    return total"""

        user_code = st.text_area(
            "Enter or paste code:",
            value=sample_code,
            height=380,
            help="Paste the snippet you want the agent to review.",
        )

        btn_analyze = st.button("🚀 Analyze & Debug Code", type="primary", use_container_width=True)

    # Right Column: Output & Results
    with col_output:
        st.subheader("🔍 Agent Insights")

        if btn_analyze:
            if not user_code.strip():
                st.warning("⚠️ Please enter some code to analyze.")
                return

            with st.spinner("Analyzing code structure, logic, and potential vulnerabilities..."):
                try:
                    # Execute analysis (Replace mock function with your actual backend integration)
                    result = mock_ai_code_reviewer(user_code, language, review_mode)

                    st.success("Analysis Complete!")

                    # Results Tabs
                    tab_summary, tab_refactored, tab_bugs = st.tabs(
                        ["📋 Feedback & Explanation", "⚡ Refactored Code", "🐞 Identified Issues"]
                    )

                    with tab_summary:
                        st.markdown("### Agent Feedback")
                        st.markdown(result.get("explanation", "No detailed summary provided."))
                        
                        st.markdown("#### Complexity Comparison")
                        comp = result.get("complexity", {})
                        c1, c2 = st.columns(2)
                        c1.metric("Time Complexity (Before)", comp.get("Before", "N/A"))
                        c2.metric("Time Complexity (After)", comp.get("After", "N/A"))

                    with tab_refactored:
                        st.markdown("### Suggested Improved Code")
                        refactored_code = result.get("refactored_code", "")
                        st.code(refactored_code, language=language.lower())

                        # Download button for refactored code
                        st.download_button(
                            label="📥 Download Refactored Code",
                            data=refactored_code,
                            file_name=f"refactored_code.{language.lower()}",
                            mime="text/plain",
                        )

                    with tab_bugs:
                        st.markdown("### Detected Issues")
                        bugs = result.get("bugs_found", [])
                        if bugs:
                            df_bugs = pd.DataFrame(bugs)
                            st.dataframe(df_bugs, use_container_width=True)
                        else:
                            st.info("No explicit bugs detected in this snippet.")

                except Exception as e:
                    st.error(f"An error occurred during execution: {str(e)}")
        else:
            st.info("👈 Paste your code on the left and click **Analyze & Debug Code** to start.")


if __name__ == "__main__":
    main()
