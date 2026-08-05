"""
app.py — Streamlit UI for the Multi-Agent Research Assistant

Run with:
    streamlit run app.py

This file only handles UI + orchestration display. All actual agent logic
lives in pipeline.py / agents.py / tools_file.py — untouched.
"""

import streamlit as st
from pipeline import run_research_pipeline

# --------------------------------------------------------------------------- #
# Page config
# --------------------------------------------------------------------------- #

st.set_page_config(
    page_title="Multi-Agent Research Assistant",
    page_icon="🧠",
    layout="wide",
)

# --------------------------------------------------------------------------- #
# Minimal custom styling
# --------------------------------------------------------------------------- #

st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        color: #888;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .step-badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 999px;
        background-color: #6C5CE7;
        color: white;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .report-box {
        background-color: #111319;
        border: 1px solid #2a2d36;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------- #
# Session state init
# --------------------------------------------------------------------------- #

if "history" not in st.session_state:
    st.session_state.history = []   # list of {topic, state}

# --------------------------------------------------------------------------- #
# Sidebar
# --------------------------------------------------------------------------- #

with st.sidebar:
    st.markdown("### 🧠 Research Assistant")
    st.caption("Search Agent → Reader Agent → Writer → Critic")
    st.divider()

    st.markdown("**Pipeline stages**")
    st.markdown("1. 🔍 Search Agent — finds live sources\n"
                "2. 📖 Reader Agent — scrapes deep content\n"
                "3. ✍️ Writer Chain — drafts the report\n"
                "4. 🧐 Critic Chain — scores & reviews it")

    st.divider()
    st.markdown("**Past topics**")
    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history)):
            if st.button(item["topic"], key=f"hist_{i}"):
                st.session_state.selected_topic = item["topic"]
                st.session_state.selected_state = item["state"]
    else:
        st.caption("No research run yet.")

# --------------------------------------------------------------------------- #
# Header
# --------------------------------------------------------------------------- #

st.markdown('<div class="main-title">🧠 Multi-Agent Research Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Give it a topic — a team of AI agents will search, read, write, and critique a full report.</div>', unsafe_allow_html=True)

# --------------------------------------------------------------------------- #
# Input
# --------------------------------------------------------------------------- #

col1, col2 = st.columns([5, 1])
with col1:
    topic = st.text_input(
        "Research topic",
        placeholder="e.g. Impact of quantum computing on cryptography",
        label_visibility="collapsed",
    )
with col2:
    run_clicked = st.button("🚀 Run", use_container_width=True)

# --------------------------------------------------------------------------- #
# Run pipeline
# --------------------------------------------------------------------------- #

if run_clicked:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        progress = st.progress(0, text="Starting pipeline...")
        status = st.empty()

        try:
            status.info("🔍 Search Agent is finding live sources...")
            progress.progress(15)

            # run_research_pipeline runs all 4 steps internally and prints to
            # terminal; we call it once and show the final state here.
            state = run_research_pipeline(topic)

            progress.progress(100, text="Done!")
            status.success("✅ Research pipeline complete.")

            st.session_state.history.append({"topic": topic, "state": state})
            st.session_state.selected_topic = topic
            st.session_state.selected_state = state

        except Exception as e:
            progress.empty()
            status.error(f"Pipeline failed: {e}")

# --------------------------------------------------------------------------- #
# Display results
# --------------------------------------------------------------------------- #

if "selected_state" in st.session_state:
    state = st.session_state.selected_state
    topic_display = st.session_state.selected_topic

    st.divider()
    st.markdown(f"## Results for: *{topic_display}*")

    tab_report, tab_critic, tab_search, tab_scraped = st.tabs(
        ["📄 Final Report", "🧐 Critic Feedback", "🔍 Search Results", "📖 Scraped Content"]
    )

    with tab_report:
        st.markdown('<span class="step-badge">WRITER CHAIN OUTPUT</span>', unsafe_allow_html=True)
        st.markdown(f'<div class="report-box">{state.get("report", "No report generated.")}</div>', unsafe_allow_html=True)

        st.download_button(
            "⬇️ Download report (.md)",
            data=state.get("report", ""),
            file_name=f"{topic_display.replace(' ', '_')}_report.md",
            mime="text/markdown",
        )

    with tab_critic:
        st.markdown('<span class="step-badge">CRITIC CHAIN OUTPUT</span>', unsafe_allow_html=True)
        st.markdown(state.get("feedback", "No feedback generated."))

    with tab_search:
        st.markdown('<span class="step-badge">SEARCH AGENT OUTPUT</span>', unsafe_allow_html=True)
        st.text(state.get("search_results", "No search results."))

    with tab_scraped:
        st.markdown('<span class="step-badge">READER AGENT OUTPUT</span>', unsafe_allow_html=True)
        st.text(state.get("scraped_content", "No scraped content."))

else:
    st.info("👆 Enter a topic above and click **Run** to see your multi-agent team in action.")