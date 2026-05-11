"""Certificates & Evidence — verified credentials."""
import streamlit as st

from components.theme import page_setup
from components.footer import render_footer
from components.certificate_card import render_certificate_card

page_setup("Certificates", icon="🎓")

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
        <h1> Certificates &amp; Evidence</h1>
        <p>
            Verified credentials and programme completions. Every card with a
            <b>Verify</b> button links to the issuer's official verification page —
            cards without one are either pending the badge image or pending
            issuance.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Professional Certificates ─────────────────────────────────────────────────
st.markdown(
    '<h2 class="section-title">📜 Professional Certificates</h2>',
    unsafe_allow_html=True,
)

c1, c2, c3 = st.columns(3, gap="medium")

with c1:
    render_certificate_card(
        title="Google Data Analytics Professional Certificate",
        issuer="Coursera · Google",
        date="2024",
        image_filename="google_data_analytics.png",
        credential_id="ZSZYDF2QIC7B",
        verify_url="https://coursera.org/share/9463dde4b1aeb6e500d61c5a0f1b7697",
    )

with c2:
    render_certificate_card(
        title="Data Science & Analytics Internship",
        issuer="Future Interns",
        date="December 2025",
        image_filename="future_interns.png",
        credential_id="FIT/DEC25/DS10048",
        verify_url="https://futureinterns.com/verification/?cin=FIT/DEC25/DS10048",
    )

with c3:
    render_certificate_card(
        title="Data Analytics & Visualization",
        issuer="Strathmore University · @LabAfrica",
        date="July – September 2025",
        image_filename="strathmore.png",
        credential_id=None,
        verify_url=None,
    )

# ── Programmes in Progress ────────────────────────────────────────────────────
st.markdown(
    '<h2 class="section-title">⏳ In Progress</h2>',
    unsafe_allow_html=True,
)

p1, p2, p3 = st.columns(3, gap="medium")

with p1:
    render_certificate_card(
        title="Data Science Bootcamp",
        issuer="GOMYCODE",
        date="Pending issuance",
        image_filename="gomycode.png",
        credential_id=None,
        verify_url=None,
        pending=True,
    )

render_footer()
