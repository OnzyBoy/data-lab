"""Reusable certificate card with uniform image sizing."""
import base64
from pathlib import Path

import streamlit as st


_ASSETS = Path(__file__).resolve().parent.parent / "assets" / "certificates"


def _img_to_data_uri(path: Path) -> str | None:
    if not path.exists():
        return None
    try:
        data = path.read_bytes()
    except Exception:
        return None
    suffix = path.suffix.lower().lstrip(".")
    mime = {
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "gif": "image/gif",
        "webp": "image/webp",
        "svg": "image/svg+xml",
    }.get(suffix, "image/png")
    return f"data:{mime};base64,{base64.b64encode(data).decode('ascii')}"


def render_certificate_card(
    title: str,
    issuer: str,
    date: str,
    image_filename: str | None = None,
    credential_id: str | None = None,
    verify_url: str | None = None,
    pending: bool = False,
) -> None:
    """Render a certificate card. The whole card (including the image) is rendered
    as a single HTML block so the image is uniformly sized via CSS object-fit."""
    # Image / placeholder
    data_uri = None
    if image_filename:
        data_uri = _img_to_data_uri(_ASSETS / image_filename)

    if data_uri:
        thumb_html = (
            f'<div class="cert-thumb"><img src="{data_uri}" alt="{title}"/></div>'
        )
    else:
        thumb_html = (
            '<div class="cert-thumb placeholder">📜 Badge image pending</div>'
        )

    cred_html = (
        f'<div class="cred-id">ID: {credential_id}</div>' if credential_id else ""
    )

    if pending:
        action_html = '<span class="pending-badge">⏳ In Progress</span>'
    elif verify_url:
        action_html = (
            f'<a class="verify-btn" href="{verify_url}" target="_blank" '
            f'rel="noopener">✓ Verify</a>'
        )
    else:
        action_html = ''

    st.markdown(
        f"""
<div class="cert-card">
  {thumb_html}
  <h4>{title}</h4>
  <div class="issuer">{issuer} · {date}</div>
  {cred_html}
  <div class="action-wrap">{action_html}</div>
</div>
        """,
        unsafe_allow_html=True,
    )
