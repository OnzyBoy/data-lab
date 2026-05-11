"""Aristo Data Lab — Executive Dashboard (Home)."""
import plotly.graph_objects as go
import streamlit as st

from components.theme import page_setup
from components.footer import render_footer
from components.project_card import render_project_card
from utils.plotting import apply_dark, ACCENT, COLORWAY

page_setup("Home", icon="📊")

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
        <h1>Aristo's Data Lab</h1>
        <h3>Proof of Competence.</h3>
        <p>
            A collection of end-to-end data products. Interactive, opinionated,
            and built with the modern data stack.
        </p>
        <div class="hero-links">
            <a href="https://aristoayako.vercel.app/" target="_blank">Official Portfolio ↗</a>
            <span class="divider">|</span>
            <a href="https://github.com/OnzyBoy" target="_blank">GitHub ↗</a>
            <span class="divider">|</span>
            <a href="https://linkedin.com/in/aristo-ayako" target="_blank">LinkedIn ↗</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Skill Distribution ────────────────────────────────────────────────────────
st.markdown('<h2 class="section-title">Skill Distribution</h2>', unsafe_allow_html=True)

skills = {
    "Python": 85,
    "SQL": 60,
    "Power BI": 80,
    "Tableau": 80,
    "Excel": 85,
    "Pandas / NumPy": 80,
    "Scikit-learn": 80,
}

radar = go.Figure()
radar.add_trace(
    go.Scatterpolar(
        r=list(skills.values()) + [list(skills.values())[0]],
        theta=list(skills.keys()) + [list(skills.keys())[0]],
        fill="toself",
        name="Proficiency",
        line=dict(color=ACCENT, width=2),
        fillcolor="rgba(149, 173, 207, 0.25)",
        marker=dict(size=7, color=ACCENT),
        hovertemplate="<b>%{theta}</b><br>Level: %{r}/100<extra></extra>",
    )
)
radar.update_layout(
    polar=dict(
        bgcolor="#23272F",
        radialaxis=dict(
            visible=True,
            range=[0, 100],
            gridcolor="#35363a",
            linecolor="#35363a",
            tickfont=dict(color="#b0b3b8", size=10),
        ),
        angularaxis=dict(
            gridcolor="#35363a",
            linecolor="#35363a",
            tickfont=dict(color="#F4F4F4", size=12),
        ),
    ),
    showlegend=False,
    height=460,
    margin=dict(l=60, r=60, t=30, b=30),
)
apply_dark(radar)
st.plotly_chart(radar, use_container_width=True)

# ── Featured Projects ─────────────────────────────────────────────────────────
st.markdown('<h2 class="section-title">Featured Projects</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    render_project_card(
        emoji="💳",
        title="Financial Inclusion Predictor",
        summary=(
            "Random-Forest classifier predicting bank-account ownership across "
            "East Africa. Live, deployed, and explainable — with metrics, "
            "confusion matrix, and feature importance laid bare."
        ),
        tags=["Python", "Scikit-learn", "Streamlit", "ML"],
        page_path="pages/1_💳_Financial_Inclusion.py",
    )

with col2:
    render_project_card(
        emoji="🎫",
        title="Support Urgency Intelligence",
        summary=(
            "NLP-based urgency scoring with Sentence-Transformers + XGBoost — "
            "re-prioritized 5,700 backlog tickets at 99.64% accuracy by "
            "engineering a Custom Urgency Index."
        ),
        tags=["NLP", "XGBoost", "Sentiment", "Python"],
        page_path="pages/2_🎫_Support_Urgency_Intelligence.py",
    )

with col3:
    render_project_card(
        emoji="🩸",
        title="Blood Group Analysis",
        summary=(
            "Power BI dashboard visualizing global and regional blood-type "
            "distributions, with DAX measures for population-weighted "
            "frequency insights."
        ),
        tags=["Power BI", "DAX", "Excel", "Modeling"],
        page_path="pages/3_🩸_Blood_Group_Analysis.py",
    )

# ── Quick stats strip ────────────────────────────────────────────────────────
st.markdown('<h2 class="section-title">At a Glance</h2>', unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)
m1.metric("Projects shipped", "5+")
m2.metric("Best model accuracy", "99.64%")
m3.metric("Stack focus", "Python · BI · ML")
m4.metric("Certificates", "4")

st.info(
    "🎓 See the **Certificates** page for verified credentials including "
    "Google Data Analytics and the Future Interns Data Science programme.",
    # icon="📜",
)

render_footer()
