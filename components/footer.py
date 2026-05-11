"""Footer linking back to the official Vercel portfolio."""
import streamlit as st

PORTFOLIO_URL = "https://aristoayako.vercel.app/#projects"


def render_footer() -> None:
    st.markdown(
        f"""
        <div class="lab-footer">
            📍 Back to Official Portfolio:
            <a href="{PORTFOLIO_URL}" target="_blank" rel="noopener">aristoayako.vercel.app</a>
            &nbsp;·&nbsp; Built with Streamlit &amp; Plotly
        </div>
        """,
        unsafe_allow_html=True,
    )
