import streamlit as st
import requests
import time

# ── Config ──────────────────────────────────────────────────────────────────
API_URL = "https://Phantom611-autonoumous-research-agent.hf.space"

st.set_page_config(
    page_title="Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&    family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap');

/* Reset & base */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f;
    color: #e8e6e0;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: 
        radial-gradient(ellipse 80% 50% at 20% 10%, rgba(255,140,50,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(100,80,255,0.05) 0%, transparent 60%),
        #0a0a0f;
}

[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] { display: none; }
section[data-testid="stMain"] > div { padding-top: 2rem; }

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* Typography */
h1, h2, h3 { font-family: 'DM Serif Display', serif; }

/* Hero */
.hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.hero-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #ff8c32;
    margin-bottom: 1rem;
}
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2.5rem, 6vw, 4.5rem);
    font-weight: 400;
    line-height: 1.1;
    color: #f0ede6;
    margin: 0 0 1rem;
}
.hero-title em {
    font-style: italic;
    color: #ff8c32;
}
.hero-subtitle {
    font-size: 1rem;
    color: #888;
    font-weight: 300;
    max-width: 500px;
    margin: 0 auto;
    line-height: 1.6;
    text-align: center;
    display: block;
    width: 100%;
}

/* Input area */
.input-wrapper {
    max-width: 720px;
    margin: 2rem auto;
    position: relative;
}

/* Override Streamlit input */
[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #e8e6e0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 1rem 1.2rem !important;
    transition: border-color 0.2s !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: rgba(255,140,50,0.5) !important;
    box-shadow: 0 0 0 3px rgba(255,140,50,0.1) !important;
}
[data-testid="stTextInput"] input::placeholder { color: #555 !important; }
[data-testid="stTextInput"] label { color: #666 !important; font-size: 0.75rem !important; }

/* Button */
[data-testid="stButton"] button {
    background: linear-gradient(135deg, #ff8c32, #ff6b00) !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 0.7rem 2rem !important;
    transition: all 0.2s !important;
    width: 100% !important;
}
[data-testid="stButton"] button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(255,140,50,0.3) !important;
}

/* Status card */
.status-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    max-width: 720px;
    margin: 1.5rem auto;
}
.status-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #555;
    margin-bottom: 0.5rem;
}
.status-running {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    color: #ff8c32;
    font-family: 'DM Mono', monospace;
    font-size: 0.9rem;
}
.pulse {
    width: 8px;
    height: 8px;
    background: #ff8c32;
    border-radius: 50%;
    animation: pulse 1.5s ease-in-out infinite;
    flex-shrink: 0;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.8); }
}

/* Metrics row */
.metrics-row {
    display: flex;
    gap: 1rem;
    max-width: 720px;
    margin: 1.5rem auto;
}
.metric-card {
    flex: 1;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
}
.metric-value {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: #ff8c32;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.metric-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #555;
}

/* Grounding badge */
.grounding-badge {
    display: inline-block;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.badge-grounded { background: rgba(80,200,120,0.15); color: #50c878; border: 1px solid rgba(80,200,120,0.3); }
.badge-partial { background: rgba(255,140,50,0.15); color: #ff8c32; border: 1px solid rgba(255,140,50,0.3); }
.badge-not { background: rgba(255,80,80,0.15); color: #ff5050; border: 1px solid rgba(255,80,80,0.3); }

/* Report */
.report-container {
    max-width: 720px;
    margin: 1.5rem auto;
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 2rem 2.5rem;
}
.report-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}
.report-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.3rem;
    color: #f0ede6;
}
.report-content {
    font-size: 0.95rem;
    line-height: 1.8;
    color: #c8c5be;
    white-space: pre-wrap;
}
.report-content h1, .report-content h2, .report-content h3 {
    color: #f0ede6;
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
}

/* Error */
.error-card {
    background: rgba(255,80,80,0.08);
    border: 1px solid rgba(255,80,80,0.2);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    max-width: 720px;
    margin: 1rem auto;
    color: #ff8080;
    font-family: 'DM Mono', monospace;
    font-size: 0.85rem;
}

/* Divider */
.divider {
    width: 100%;
    max-width: 720px;
    margin: 2rem auto;
    border: none;
    border-top: 1px solid rgba(255,255,255,0.06);
    display: block;
}

/* Center columns */
[data-testid="stHorizontalBlock"] { max-width: 720px; margin: 0 auto; }
</style>
""", unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-label">// Autonomous AI System</div>
    <h1 class="hero-title">Research <em>Agent</em></h1>
    <p class="hero-subtitle">
        Ask any research question. The agent plans, searches, retrieves, 
        and synthesizes a structured report — autonomously.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Input ────────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    query = st.text_input(
        "Research Question",
        placeholder="e.g. What are the latest breakthroughs in quantum computing?",
        label_visibility="collapsed"
    )
    run = st.button("⟶  Generate Report", use_container_width=True)

# ── Research Logic ───────────────────────────────────────────────────────────
if run:
    if not query.strip():
        st.markdown('<div class="error-card">⚠ Please enter a research question.</div>', unsafe_allow_html=True)
    else:
        # Status placeholder
        status_placeholder = st.empty()
        progress_placeholder = st.empty()

        # Show running state
        status_placeholder.markdown(f"""
        <div class="status-card">
            <div class="status-label">Agent Status</div>
            <div class="status-running">
                <div class="pulse"></div>
                Researching: "{query}"
            </div>
        </div>
        """, unsafe_allow_html=True)

        start_time = time.time()

        try:
            with progress_placeholder:
                with st.spinner(""):
                    response = requests.post(
                        f"{API_URL}/research-plan",
                        json={"query": query},
                        timeout=300
                    )

            if response.status_code == 200:
                result = response.json()
                elapsed = round(time.time() - start_time, 1)

                # Clear status
                status_placeholder.empty()
                progress_placeholder.empty()

                # ── Metrics ──────────────────────────────────────────────
                grounding = result.get("grounding_check", "UNKNOWN")
                if "FULLY" in grounding or grounding == "GROUNDED":
                    badge_class = "badge-grounded"
                elif "PARTIAL" in grounding:
                    badge_class = "badge-partial"
                else:
                    badge_class = "badge-not"

                st.markdown(f"""
                <div class="metrics-row">
                    <div class="metric-card">
                        <div class="metric-value">{elapsed}s</div>
                        <div class="metric-label">Total Time</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{result.get('iterations', 0)}</div>
                        <div class="metric-label">Iterations</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{result.get('retrieved_chunks', 0)}</div>
                        <div class="metric-label">Sources</div>
                    </div>
                    <div class="metric-card" style="justify-content:center; display:flex; flex-direction:column; align-items:center;">
                        <span class="grounding-badge {badge_class}">{grounding}</span>
                        <div class="metric-label" style="margin-top:0.5rem;">Grounding</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # ── Report ───────────────────────────────────────────────
                final_report = result.get("final_report", "No report generated.")

                st.markdown(f"""
                <div class="report-container">
                    <div class="report-header">
                        <div class="report-title">📄 Research Report</div>
                    </div>
                    <div class="report-content">{final_report}</div>
                </div>
                """, unsafe_allow_html=True)

                # Download button
                col1, col2, col3 = st.columns([1, 4, 1])
                with col2:
                    st.download_button(
                        label="↓  Download Report",
                        data=final_report,
                        file_name=f"research_{query[:30].replace(' ', '_')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

            else:
                status_placeholder.empty()
                st.markdown(f'<div class="error-card">✗ API Error {response.status_code}: {response.text[:200]}</div>', unsafe_allow_html=True)

        except requests.exceptions.Timeout:
            status_placeholder.empty()
            st.markdown('<div class="error-card">✗ Request timed out. The agent is taking longer than expected. Try again.</div>', unsafe_allow_html=True)

        except Exception as e:
            status_placeholder.empty()
            st.markdown(f'<div class="error-card">✗ Connection error: {str(e)}</div>', unsafe_allow_html=True)

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown('<div style="max-width:720px; margin: 2rem auto; border-top: 1px solid rgba(255,255,255,0.06);"></div>', unsafe_allow_html=True)
st.markdown("""
<p style="text-align:center; font-family:'DM Mono',monospace; font-size:0.65rem; 
letter-spacing:0.15em; color:#333; text-transform:uppercase;">
Autonomous Research Agent // Powered by LangGraph + Groq + Qdrant
</p>
""", unsafe_allow_html=True)