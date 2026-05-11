"""Theme injector — applies palette matching aristo-portfolio dark theme."""
from pathlib import Path
import streamlit as st


import base64
from pathlib import Path
import streamlit as st

_CSS_PATH = Path(__file__).resolve().parent.parent / "assets" / "styles.css"
_LOGO_PATH = Path(__file__).resolve().parent.parent / "assets" / "images" / "AA-logo.png"

def inject_css() -> None:
    """Inject custom CSS once per page."""
    try:
        css = _CSS_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        return
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    
def page_setup(title: str, icon: str = "📊") -> None:
    """Standard per-page setup: config + css."""
    st.set_page_config(
        page_title=f"{title} · Aristo Data Lab",
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    # Native Streamlit logo at top-left of sidebar
    if _LOGO_PATH.exists():
        st.logo(str(_LOGO_PATH))
        
    inject_css()
