import os
import time
import json
import string
import pandas as pd
import streamlit as st
from collections import Counter
from utils.gemini_client import ask_gemini

# --- Config ---
st.set_page_config(page_title="Startup AI Command Center", layout="wide", initial_sidebar_state="collapsed")

# Modern professional dark theme via CSS injection
st.markdown(
    """
    <style>
    /* Import modern fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* Global modern dark theme */
    .reportview-container, .main, .block-container {
        background: #000000;
        color: #ffffff;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        line-height: 1.6;
    }
    
    /* Hide sidebar completely */
    .sidebar {
        display: none !important;
    }
    
    /* Main content area */
    .main .block-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
        background: #000000;
    }
    
    /* Modern headings */
    h1, h2, h3, h4 {
        color: #ffffff;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        letter-spacing: -0.025em;
        margin-bottom: 1rem;
    }
    
    h1 {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #a1a1aa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 3rem;
        letter-spacing: -0.05em;
    }
    
    h2 {
        font-size: 1.875rem;
        font-weight: 700;
        color: #ffffff;
        border-bottom: 2px solid #27272a;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    
    h3 {
        font-size: 1.5rem;
        font-weight: 600;
        color: #a1a1aa;
    }
    
    /* Modern navigation tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: #18181b;
        border-radius: 12px;
        padding: 4px;
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #71717a;
        font-weight: 500;
        padding: 12px 24px;
        border: none;
        transition: all 0.2s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: #27272a;
        color: #ffffff;
        font-weight: 600;
    }
    
    /* Modern buttons */
    .stButton>button {
        background: #27272a;
        color: #ffffff;
        border: 1px solid #3f3f46;
        border-radius: 8px;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 0.875rem;
        padding: 10px 20px;
        transition: all 0.2s ease;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-height: 40px;
    }
    
    .stButton>button:hover {
        background: #3f3f46;
        border-color: #52525b;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    .stButton>button:active {
        transform: translateY(0);
    }
    
    /* Modern input fields */
    textarea, input, .stTextInput>div>input, .stSelectbox>div>div>div {
        background: #18181b;
        color: #ffffff;
        border: 1px solid #3f3f46;
        border-radius: 8px;
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        padding: 12px 16px;
        transition: all 0.2s ease;
        outline: none;
    }
    
    textarea:focus, input:focus, .stTextInput>div>input:focus, .stSelectbox>div>div>div:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        background: #1f1f23;
    }
    
    /* Placeholder styling */
    textarea::placeholder, input::placeholder {
        color: #71717a;
    }
    
    /* Selectbox styling */
    .stSelectbox>div>div>div {
        background: #18181b;
        color: #ffffff;
    }
    
    /* Number input styling */
    .stNumberInput>div>div>input {
        background: #18181b;
        color: #ffffff;
        border: 1px solid #3f3f46;
        border-radius: 8px;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        text-align: center;
    }
    
    /* Slider styling */
    .stSlider>div>div>div>div {
        background: #6366f1;
    }
    
    .stSlider>div>div>div>div>div {
        background: #ffffff;
        border: 2px solid #6366f1;
    }
    
    /* Modern tables */
    .stDataFrame table { 
        color: #ffffff;
        background: #18181b;
        border: 1px solid #3f3f46;
        border-radius: 8px;
        overflow: hidden;
        font-family: 'Inter', sans-serif;
    }
    
    .stDataFrame th {
        background: #27272a;
        color: #ffffff;
        font-weight: 600;
        font-size: 0.875rem;
        padding: 12px 16px;
        border-bottom: 1px solid #3f3f46;
    }
    
    .stDataFrame td {
        background: #18181b;
        color: #ffffff;
        border-bottom: 1px solid #27272a;
        padding: 12px 16px;
        font-size: 0.875rem;
    }
    
    /* Code blocks */
    .stCode {
        background: #18181b;
        border: 1px solid #3f3f46;
        border-radius: 8px;
        color: #ffffff;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.875rem;
        padding: 16px;
        line-height: 1.5;
    }
    
    /* Metrics styling */
    .metric-container {
        background: #18181b;
        border: 1px solid #3f3f46;
        border-radius: 8px;
        padding: 16px;
        margin: 8px 0;
    }
    
    .metric-label {
        color: #71717a;
        font-size: 0.75rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .metric-value {
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 4px;
    }
    
    /* Charts */
    .stChart {
        background: #18181b;
        border: 1px solid #3f3f46;
        border-radius: 8px;
        padding: 16px;
    }
    
    /* Download button */
    .stDownloadButton>button { 
        background: #27272a;
        color: #ffffff;
        border: 1px solid #3f3f46;
        border-radius: 8px;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 0.875rem;
        padding: 10px 20px;
        transition: all 0.2s ease;
    }
    
    .stDownloadButton>button:hover {
        background: #3f3f46;
        border-color: #52525b;
        transform: translateY(-1px);
    }
    
    /* Checkbox styling */
    .st-ck { 
        color: #ffffff; 
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #18181b;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #3f3f46;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #52525b;
    }
    
    /* Remove Streamlit footer */
    footer {visibility: hidden;}
    
    /* Card-like containers */
    .stMarkdown {
        background: #18181b;
        border: 1px solid #3f3f46;
        border-radius: 12px;
        padding: 24px;
        margin: 16px 0;
    }
    
    /* AI Response content styling */
    .stMarkdown:has(p) {
        background: #000000;
        border: 1px solid #333333;
        border-radius: 8px;
        padding: 16px;
        margin: 0 0 20px 0;
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        line-height: 1.6;
        color: #ffffff;
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #22c55e;
        margin-right: 8px;
    }
    
    /* Divider styling */
    hr {
        border: none;
        height: 1px;
        background: #3f3f46;
        margin: 2rem 0;
    }
    
    /* Link styling */
    a {
        color: #6366f1;
        text-decoration: none;
        transition: color 0.2s ease;
    }
    
    a:hover {
        color: #818cf8;
    }
    
    /* Ultra Enhanced AI response styling */
    .ai-response-container {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 25%, #0f0f0f 50%, #1a1a1a 75%, #0a0a0a 100%);
        border: 2px solid transparent;
        border-radius: 20px;
        padding: 28px;
        margin: 24px 0;
        box-shadow: 
            0 12px 40px rgba(99, 102, 241, 0.3),
            0 0 0 1px rgba(99, 102, 241, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
        animation: containerGlow 3s ease-in-out infinite alternate;
    }
    
    .ai-response-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, 
            rgba(99, 102, 241, 0.1) 0%, 
            rgba(139, 92, 246, 0.05) 25%, 
            rgba(99, 102, 241, 0.1) 50%, 
            rgba(139, 92, 246, 0.05) 75%, 
            rgba(99, 102, 241, 0.1) 100%);
        border-radius: 20px;
        z-index: -1;
        animation: backgroundShift 4s ease-in-out infinite;
    }
    
    .ai-response-header {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
        gap: 16px;
        position: relative;
        z-index: 2;
    }
    
    .ai-status-indicator {
        width: 14px;
        height: 14px;
        background: linear-gradient(45deg, #22c55e, #16a34a);
        border-radius: 50%;
        animation: pulse 2s infinite, statusGlow 3s ease-in-out infinite;
        box-shadow: 0 0 10px rgba(34, 197, 94, 0.5);
        position: relative;
    }
    
    .ai-status-indicator::after {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #22c55e, #16a34a, #22c55e);
        border-radius: 50%;
        z-index: -1;
        animation: statusRing 2s linear infinite;
    }
    
    .ai-response-title {
        margin: 0;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 1.4rem;
        background: linear-gradient(135deg, #ffffff 0%, #6366f1 50%, #ffffff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 20px rgba(99, 102, 241, 0.3);
        animation: titleGlow 4s ease-in-out infinite alternate;
    }
    
    .ai-response-timer {
        margin-left: auto;
        font-size: 0.9rem;
        color: #a1a1aa;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        background: rgba(99, 102, 241, 0.1);
        padding: 6px 12px;
        border-radius: 20px;
        border: 1px solid rgba(99, 102, 241, 0.2);
        backdrop-filter: blur(5px);
    }
    
    .ai-response-content {
        background: linear-gradient(135deg, #000000 0%, #0a0a0a 100%);
        border: 1px solid #27272a;
        border-radius: 16px;
        padding: 24px;
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        line-height: 1.8;
        color: #ffffff;
        white-space: pre-wrap;
        overflow-x: auto;
        position: relative;
        z-index: 2;
        box-shadow: 
            inset 0 1px 0 rgba(255, 255, 255, 0.05),
            0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .ai-response-content::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.3), transparent);
        border-radius: 16px 16px 0 0;
    }
    
    .shimmer-effect {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #6366f1, #8b5cf6, #6366f1);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.7; transform: scale(1.1); }
    }
    
    @keyframes containerGlow {
        0% { box-shadow: 0 12px 40px rgba(99, 102, 241, 0.3), 0 0 0 1px rgba(99, 102, 241, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.1); }
        100% { box-shadow: 0 12px 40px rgba(99, 102, 241, 0.5), 0 0 0 1px rgba(99, 102, 241, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.15); }
    }
    
    @keyframes backgroundShift {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }
    
    @keyframes statusGlow {
        0%, 100% { box-shadow: 0 0 10px rgba(34, 197, 94, 0.5); }
        50% { box-shadow: 0 0 20px rgba(34, 197, 94, 0.8); }
    }
    
    @keyframes statusRing {
        0% { transform: rotate(0deg); opacity: 0.8; }
        100% { transform: rotate(360deg); opacity: 0.2; }
    }
    
    @keyframes titleGlow {
        0% { text-shadow: 0 0 20px rgba(99, 102, 241, 0.3); }
        100% { text-shadow: 0 0 30px rgba(99, 102, 241, 0.6); }
    }
    
    /* Enhanced markdown styling for AI responses */
    .ai-response-content h1, .ai-response-content h2, .ai-response-content h3 {
        color: #ffffff;
        border-bottom: 1px solid #27272a;
        padding-bottom: 8px;
        margin-top: 24px;
        margin-bottom: 16px;
    }
    
    .ai-response-content strong {
        color: #6366f1;
        font-weight: 600;
    }
    
    .ai-response-content em {
        color: #a1a1aa;
        font-style: italic;
    }
    
    .ai-response-content ul, .ai-response-content ol {
        margin: 16px 0;
        padding-left: 24px;
    }
    
    .ai-response-content li {
        margin: 8px 0;
        color: #e5e5e5;
    }
    
    .ai-response-content blockquote {
        border-left: 4px solid #6366f1;
        padding-left: 16px;
        margin: 16px 0;
        color: #a1a1aa;
        font-style: italic;
    }
    
    .ai-response-content code {
        background: #1a1a1a;
        color: #22c55e;
        padding: 2px 6px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.875rem;
    }
    
    .ai-response-content pre {
        background: #1a1a1a;
        border: 1px solid #27272a;
        border-radius: 8px;
        padding: 16px;
        overflow-x: auto;
        margin: 16px 0;
    }
    
    .ai-response-content pre code {
        background: none;
        padding: 0;
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Helper utilities ---
DATA_DIR = os.path.join(os.getcwd(), "data")
os.makedirs(DATA_DIR, exist_ok=True)
USAGE_LOG = os.path.join(DATA_DIR, "usage_logs.csv")

STOPWORDS = {
    "the","and","to","of","a","in","for","is","on","that","with","as","are","it","be","by","or","from",
    "this","an","at","we","our","you","your","will","can","has","have"
}

def text_metrics(text: str):
    words = [w.strip(string.punctuation).lower() for w in text.split() if w.strip(string.punctuation)]
    words = [w for w in words if w]
    word_count = len(words)
    unique = len(set(words))
    reading_time_min = round(word_count / 200, 2)  # ~200 wpm
    # keyword frequencies (filter stopwords and single chars)
    keywords = [w for w in words if w not in STOPWORDS and len(w) > 2]
    top = Counter(keywords).most_common(10)
    return {
        "word_count": word_count,
        "unique_words": unique,
        "reading_time_min": reading_time_min,
        "top_keywords": top
    }

def log_usage(module: str, prompt: str, response: str, latency_s: float):
    row = {
        "timestamp": pd.Timestamp.now().isoformat(),
        "module": module,
        "prompt": prompt,
        "response_word_count": len(response.split()),
        "latency_s": round(latency_s, 3)
    }
    # append to CSV (create if not exists)
    df_row = pd.DataFrame([row])
    if os.path.exists(USAGE_LOG):
        df_row.to_csv(USAGE_LOG, mode="a", header=False, index=False)
    else:
        df_row.to_csv(USAGE_LOG, index=False)

def display_response_and_analytics(prompt: str, resp_text: str, start_time: float, module_name: str):
    latency = time.time() - start_time
    
    # Create header container
    st.markdown(f"""
    <div style="
        background: #000000;
        border: 1px solid #333333;
        border-radius: 12px;
        padding: 16px;
        margin: 20px 0 0 0;
        font-family: 'Inter', sans-serif;
    ">
        <div style="
            display: flex;
            align-items: center;
            gap: 12px;
        ">
            <div style="
                width: 12px;
                height: 12px;
                background: #22c55e;
                border-radius: 50%;
            "></div>
            <h3 style="
                margin: 0;
                color: #ffffff;
                font-family: 'Inter', sans-serif;
                font-weight: 600;
                font-size: 1.2rem;
            ">🤖 AI Response</h3>
            <div style="
                margin-left: auto;
                font-size: 0.875rem;
                color: #a1a1aa;
                font-family: 'Inter', sans-serif;
            ">Generated in {latency:.2f}s</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create content container with styling
    st.markdown("""
    <style>
    .ai-response-box {
        background: #000000;
        border: 1px solid #333333;
        border-radius: 8px;
        padding: 16px;
        margin: 0 0 20px 0;
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        line-height: 1.6;
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create a container div and render the content
    st.markdown('<div class="ai-response-box">', unsafe_allow_html=True)
    st.markdown(resp_text)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Log usage (hidden from UI)
    log_usage(module_name, prompt, resp_text, latency)

# --- App UI ---
st.title("Startup AI Command Center")
st.markdown("A professional, minimalist AI workspace for founders and operators. Responses are returned raw and formatted for direct use.")

# Main navigation using tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "Idea Generator",
    "Market Research", 
    "Business Model (BMC)",
    "Pitch Refinement",
    "Financial Forecast",
    "SWOT & Risks",
    "Investor Q&A",
    "Branding Kit"
])

# Usage info
st.markdown("---")
st.markdown("**Usage logs will be stored locally at:** `data/usage_logs.csv`")

with tab1:
    st.header("AI Startup Idea Generator")
    keywords = st.text_input("Keywords (comma-separated):", placeholder="AI, logistics, Southeast Asia")
    tone = st.selectbox("Output tone", ["Professional", "Investor-ready", "Technical"], index=0)
    if st.button("Generate"):
        prompt = f"Keywords: {keywords}, Tone: {tone}"
        start = time.time()
        resp = ask_gemini(prompt, task_type="startup_idea", context={"tone": tone})
        display_response_and_analytics(prompt, resp, start, "Idea Generator")

with tab2:
    st.header("Market Research Assistant")
    topic = st.text_input("Topic / Company / Market:")
    timeframe = st.text_input("Timeframe (e.g., 2020-2025) or leave blank:")
    if st.button("Analyze"):
        prompt = f"Topic: {topic}, Timeframe: {timeframe}"
        start = time.time()
        resp = ask_gemini(prompt, task_type="market_research", context={"timeframe": timeframe})
        display_response_and_analytics(prompt, resp, start, "Market Research")

with tab3:
    st.header("Business Model Canvas (AI-assisted)")
    name = st.text_input("Startup name:")
    description = st.text_area("One-line description / problem you solve:")
    if st.button("Build Canvas"):
        prompt = f"Startup: {name}, Description: {description}"
        start = time.time()
        resp = ask_gemini(prompt, task_type="business_model", context={"startup_name": name})
        display_response_and_analytics(prompt, resp, start, "Business Model Canvas")

with tab4:
    st.header("Refine Pitch (Investor Format)")
    pitch = st.text_area("Paste your pitch (single paragraph or bullet points):")
    if st.button("Refine Pitch"):
        prompt = f"Pitch: {pitch}"
        start = time.time()
        resp = ask_gemini(prompt, task_type="pitch_refinement")
        display_response_and_analytics(prompt, resp, start, "Pitch Refinement")

with tab5:
    st.header("Quick Financial Forecast")
    initial = st.number_input("Current monthly revenue ($):", value=1000.0)
    growth = st.number_input("Expected monthly growth rate (%):", value=10.0) / 100.0
    months = st.slider("Months to project:", min_value=6, max_value=36, value=12)
    if st.button("Project"):
        # local simple projection
        rows = []
        rev = initial
        for m in range(1, months + 1):
            rows.append({"Month": m, "Projected Revenue": round(rev, 2)})
            rev = rev * (1 + growth)
        df = pd.DataFrame(rows)
        st.subheader("Projected revenue")
        st.line_chart(df.set_index("Month"))
        st.dataframe(df)
        # AI summary for the projection
        prompt = f"Revenue projection analysis"
        start = time.time()
        resp = ask_gemini(prompt, task_type="financial_forecast", context={
            "initial": initial,
            "growth": growth * 100,
            "months": months
        })
        display_response_and_analytics(prompt, resp, start, "Financial Forecast")

with tab6:
    st.header("SWOT & Risk Assessment")
    summary = st.text_area("Provide a short summary of your startup or product:")
    if st.button("Run SWOT"):
        prompt = f"Startup summary: {summary}"
        start = time.time()
        resp = ask_gemini(prompt, task_type="swot_analysis")
        display_response_and_analytics(prompt, resp, start, "SWOT & Risks")

with tab7:
    st.header("Investor Q&A Practice")
    pitch = st.text_area("Paste concise pitch / executive summary:")
    rounds = st.slider("Number of investor questions to simulate:", 3, 10, 5)
    if st.button("Simulate Q&A"):
        prompt = f"Pitch: {pitch}"
        start = time.time()
        resp = ask_gemini(prompt, task_type="investor_qa", context={"rounds": rounds})
        display_response_and_analytics(prompt, resp, start, "Investor Q&A")

with tab8:
    st.header("Branding Kit")
    desc = st.text_input("Describe your product in one line:")
    locale = st.selectbox("Preferred language / locale (for tone)", ["Global English", "India English", "US English"])
    if st.button("Generate Branding Kit"):
        prompt = f"Product: {desc}, Locale: {locale}"
        start = time.time()
        resp = ask_gemini(prompt, task_type="branding_kit", context={"locale": locale})
        display_response_and_analytics(prompt, resp, start, "Branding Kit")

# Footer: show usage log quick summary
st.markdown("---")
st.subheader("Usage Metrics")
if os.path.exists(USAGE_LOG):
    logs = pd.read_csv(USAGE_LOG)
    total = len(logs)
    avg_latency = logs["latency_s"].mean()
    st.write(f"Total AI calls recorded: {total}")
    st.write(f"Average latency (s): {avg_latency:.2f}")
    st.dataframe(logs.tail(10))
else:
    st.write("No usage logs yet.")
