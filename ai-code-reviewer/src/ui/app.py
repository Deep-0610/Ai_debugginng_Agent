import os
import sys
import streamlit as st

# Ensure project root is on Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from dotenv import load_dotenv
from src.agents.graph import build_review_graph
from src.agents.state import CodeReviewState

load_dotenv()

# Streamlit Page Setup
st.set_page_config(
    page_title="AI Agentic Code Reviewer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark Modern CSS Styling
st.markdown("""
<style>
    /* Dark Theme Base */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    
    /* Header Styling */
    .title-text {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #58a6ff, #bc8cff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .subtitle-text {
        font-size: 0.95rem;
        color: #8b949e;
        margin-bottom: 25px;
    }

    /* Metric Glassmorphism Cards */
    .metric-container {
        display: flex;
        gap: 15px;
        margin-bottom: 20px;
    }
    .metric-card {
        flex: 1;
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .metric-value-pass {
        font-size: 1.5rem;
        font-weight: 700;
        color: #3fb950;
    }
    .metric-value-fail {
        font-size: 1.5rem;
        font-weight: 700;
        color: #f85149;
    }
    .metric-value-neutral {
        font-size: 1.5rem;
        font-weight: 700;
        color: #58a6ff;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 4px;
    }

    /* Button Styling */
    .stButton>button {
        background: linear-gradient(135deg, #238636, #2ea043) !important;
        color: #ffffff !important;
        border: none !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        height: 3.2em !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(46, 160, 67, 0.4) !important;
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid #30363d;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        border-radius: 6px 6px 0px 0px;
        color: #8b949e;
        background-color: #161b22;
        border: 1px solid #30363d;
        border-bottom: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: #21262d !important;
        color: #58a6ff !important;
        font-weight: 600;
        border-top: 2px solid #58a6ff !important;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<p class="title-text">⚡ AI Agentic Code Reviewer & Auto-Fixer</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">Multi-agent LangGraph workflow featuring static AST checks, LLM reasoning, and verified patch generation.</p>', unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.markdown("### ⚙️ Engine Settings")
    language = st.selectbox("Language Engine", ["python"])
    file_name = st.text_input("Target Filename", "main.py")
    
    st.markdown("---")
    st.markdown("### 🤖 Agent Pipeline Architecture")
    st.markdown("""
    - **1. AST & Static Linter**: Extracts AST metadata and pyflakes syntax errors.
    - **2. Reviewer Agent**: Evaluates logical bugs via LLM reasoning.
    - **3. Patch Generator**: Generates clean fix and unified diff.
    - **4. Verification Node**: Validates patch against static checks before release.
    """)

# Default Sample Code
default_code = """def calculate_discount(price, discount):
    # Missing type/value validation, zero division risk, and unused variables
    temp_var = 100
    final_price = price - (price * discount)
    return final_price / price"""

# Main Input Section
col_left, col_right = st.columns([1, 1], gap="medium")

with col_left:
    st.subheader("Source Input Code")
    input_code = st.text_area("", value=default_code, height=320, key="code_input")
    run_btn = st.button("🚀 Execute Autonomous Review & Fix Pipeline", type="primary")

with col_right:
    st.subheader("System Status")
    if "final_state" not in st.session_state and not run_btn:
        st.info("Paste your source code in the left editor and hit Execute to trigger the agent review cycle.")

# Execution Trigger
if run_btn:
    if not input_code.strip():
        st.error("Provide non-empty source code to begin analysis.")
    else:
        with st.spinner("Processing AST parsing, LLM review, and automated patching..."):
            initial_state: CodeReviewState = {
                "file_path": file_name,
                "original_code": input_code,
                "language": language.lower(),
                "ast_data": None,
                "syntax_errors": [],
                "detected_bugs": [],
                "messages": [],
                "fixed_code": None,
                "diff": None,
                "verification_passed": False,
                "retry_count": 0
            }

            graph = build_review_graph()
            st.session_state["final_state"] = graph.invoke(initial_state)

# Display Analysis Output
if "final_state" in st.session_state:
    final_state = st.session_state["final_state"]
    is_passed = final_state.get("verification_passed", False)
    bugs = final_state.get("detected_bugs", [])
    linter_count = len(bugs[0].get("linter_issues", [])) if bugs else 0

    # Custom HTML Metrics Dashboard
    st.markdown("---")
    st.subheader("📊 Execution Results Dashboard")
    
    status_html = f'<div class="metric-value-pass">PASSED</div>' if is_passed else f'<div class="metric-value-fail">FAILED</div>'
    
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-card">
            {status_html}
            <div class="metric-label">Verification Gate</div>
        </div>
        <div class="metric-card">
            <div class="metric-value-neutral">{linter_count}</div>
            <div class="metric-label">Static Lint Issues</div>
        </div>
        <div class="metric-card">
            <div class="metric-value-neutral">{final_state.get("retry_count", 0)}</div>
            <div class="metric-label">Auto-Repair Cycles</div>
        </div>
        <div class="metric-card">
            <div class="metric-value-neutral">{language.upper()}</div>
            <div class="metric-label">Target Engine</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Output Tabs
    tab_fix, tab_diff, tab_report, tab_logs = st.tabs([
        "📄 Side-by-Side Comparison", 
        "🔍 Unified Diff", 
        "🤖 LLM Audit Report", 
        "📋 Agent Workflow Logs"
    ])

    with tab_fix:
        c1, c2 = st.columns(2)
        with c1:
            st.caption("Original Code")
            st.code(input_code, language=language.lower())
        with c2:
            st.caption("Auto-Corrected Code")
            st.code(final_state.get("fixed_code", "# No fix generated"), language=language.lower())

    with tab_diff:
        diff_output = final_state.get("diff", "")
        if diff_output:
            st.code(diff_output, language="diff")
        else:
            st.info("No code modifications were required.")

    with tab_report:
        if bugs and "llm_analysis" in bugs[0]:
            st.markdown(bugs[0]["llm_analysis"])
        else:
            st.write("No report generated.")

    with tab_logs:
        for msg in final_state.get("messages", []):
            st.markdown(f"`{msg}`")