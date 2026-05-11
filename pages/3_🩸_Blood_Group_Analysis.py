"""Project 3 — Blood Group Analysis Dashboard (Power BI)."""
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

from components.theme import page_setup
from components.footer import render_footer
from utils.plotting import apply_dark, COLORWAY

page_setup("Blood Group Analysis", icon="🩸")

REPO_URL = "https://github.com/OnzyBoy/global-blood-distribution-analysis"
IMG_DIR = Path(__file__).resolve().parent.parent / "assets" / "images"

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
        <h1>Global Blood Group Distribution</h1>
        <p>
            An interactive Power BI dashboard visualizing global and regional
            blood-type distributions, with DAX measures for population-weighted
            frequency insights. Built on cleaned and transformed datasets using
            Power Query.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Overview ──────────────────────────────────────────────────────────────────
st.markdown('<h2 class="section-title">📋 Project Overview</h2>', unsafe_allow_html=True)

st.markdown(
    """
    **Goal:** make global blood-group distribution explorable for blood-bank
    planning, donor-matching feasibility studies, and epidemiology research.

    **Pipeline:**
    1. Ingest raw country-level frequency data (O+, A+, B+, AB+, O−, A−, B−, AB−).
    2. Cleaning and shaping in **Power Query** — standardized country names,
       normalized percentages, joined to a population reference table.
    3. Built a star-schema data model (Country ⟶ Continent).
    4. **DAX measures** for population-weighted blood-group counts.
    5. Single-page interactive dashboard with KPI cards, distribution charts,
       and a country-level geo-scatter — filterable by blood type, continent,
       and country.

    **Tools:** Power BI · Excel · DAX · Data Modeling · Power Query
    """
)

# ── Dashboard screenshot ──────────────────────────────────────────────────────
st.markdown(
    '<h2 class="section-title">🖼️ Live Dashboard</h2>',
    unsafe_allow_html=True,
)

dashboard_img = IMG_DIR / "blood_grp.png"
if dashboard_img.exists():
    st.image(
        str(dashboard_img),
        caption="Blood Group Distribution Analytics Dashboard — Power BI",
        use_container_width=True,
    )
else:
    st.warning("Dashboard screenshot not found at `assets/images/blood_grp.png`.")

# ── Headline numbers ──────────────────────────────────────────────────────────
st.markdown(
    '<h2 class="section-title">📌 Headline Numbers</h2>',
    unsafe_allow_html=True,
)
k1, k2, k3, k4 = st.columns(4)
k1.metric("Countries Covered", "123")
k2.metric("Total Population", "57 bn")
k3.metric("Most Common", "O+")
k4.metric("Least Common", "AB−")

# ── Recreated Plotly charts ───────────────────────────────────────────────────
st.markdown(
    '<h2 class="section-title">📊 Recreated Highlights (Plotly)</h2>',
    unsafe_allow_html=True,
)
st.caption(
    "Interactive recreations of two key visuals from the dashboard, re-rendered "
    "with the data-lab dark palette."
)

# Chart 1 — Sum of Percentage by Blood Type (matches dashboard donut values)
groups = ["O+", "A+", "B+", "AB+", "O-", "A-", "B-", "AB-"]
global_pct = [40.49, 29.29, 16.31, 4.61, 3.32, 2.50, 2.20, 1.28]

g1 = go.Figure(
    go.Bar(
        x=groups,
        y=global_pct,
        marker=dict(
            color=global_pct,
            colorscale=[
                [0.0, "#3a4a66"],
                [0.5, "#6383b0"],
                [1.0, "#AEC3E0"],
            ],
            line=dict(color="#35363a", width=1),
        ),
        text=[f"{v}%" for v in global_pct],
        textposition="outside",
        textfont=dict(color="#F4F4F4"),
        hovertemplate="<b>%{x}</b><br>Share: %{y}%<extra></extra>",
    )
)
g1.update_layout(
    title="Sum of Percentage by Blood Type",
    xaxis_title="Blood Group",
    yaxis_title="Share (%)",
    height=420,
    showlegend=False,
)
apply_dark(g1)
st.plotly_chart(g1, use_container_width=True)

# Chart 2 — Sum of Population by Country (top 9, matches dashboard)
countries = [
    "China (PRC)", "India", "United States", "Indonesia", "Pakistan",
    "Nigeria", "Brazil", "Bangladesh",
]
pop_bn = [11.2, 10.7, 2.7, 2.1, 1.9, 1.8, 1.7, 1.3]

g2 = go.Figure(
    go.Bar(
        x=pop_bn,
        y=countries,
        orientation="h",
        marker=dict(
            color=pop_bn,
            colorscale=[
                [0.0, "#3a4a66"],
                [0.5, "#6383b0"],
                [1.0, "#AEC3E0"],
            ],
            line=dict(color="#35363a", width=1),
        ),
        text=[f"{v} bn" for v in pop_bn],
        textposition="outside",
        textfont=dict(color="#F4F4F4"),
        hovertemplate="<b>%{y}</b><br>Population: %{x} bn<extra></extra>",
    )
)
g2.update_layout(
    title="Sum of Population by Country (Top 8)",
    xaxis_title="Population (billions)",
    yaxis_title="",
    yaxis=dict(autorange="reversed"),
    height=440,
    showlegend=False,
    margin=dict(l=140, r=60, t=50, b=40),
)
apply_dark(g2)
st.plotly_chart(g2, use_container_width=True)

# ── DAX measure example ──────────────────────────────────────────────────────
st.markdown(
    '<h2 class="section-title">⚙️ A Sample DAX Measure</h2>',
    unsafe_allow_html=True,
)
st.write(
    "Translating percentage shares into population-weighted donor counts so "
    "the dashboard surfaces *people*, not just percentages."
)
st.code(
    """Population-Weighted O+ Donors =
VAR PctOPos = [Avg O+ Share %]
VAR TotalPop = SUM('Country'[Population])
RETURN
    DIVIDE( PctOPos * TotalPop, 100, 0 )""",
    language="text",
)

# ── Resources ─────────────────────────────────────────────────────────────────
st.markdown('<h2 class="section-title">📚 Resources</h2>', unsafe_allow_html=True)
st.link_button("💻 View GitHub Repo ↗", REPO_URL, use_container_width=False)

render_footer()
