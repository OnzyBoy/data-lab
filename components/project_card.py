"""Reusable project card with switch-page button."""
import streamlit as st


def render_project_card(
    emoji: str,
    title: str,
    summary: str,
    tags: list[str],
    page_path: str,
    button_label: str = "Open Project →",
) -> None:
    """Render a styled project card. Card uses CSS; button uses st.button."""
    tag_html = "".join(f'<span class="tag">{t}</span>' for t in tags)
    st.markdown(
        f"""
        <div class="project-card">
            <div class="emoji">{emoji}</div>
            <h3>{title}</h3>
            <p>{summary}</p>
            <div class="tags">{tag_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    # Streamlit button below the card, styled via CSS
    if st.button(button_label, key=f"open_{title}", use_container_width=True):
        st.switch_page(page_path)
