"""Plotly dark theme matching the data-lab palette."""
import plotly.graph_objects as go
import plotly.io as pio

# Palette (kept in sync with assets/styles.css)
BG = "#18191A"
SURFACE = "#23272F"
TEXT = "#F4F4F4"
TEXT_MUTED = "#b0b3b8"
ACCENT = "#95ADCF"
BORDER = "#35363a"

COLORWAY = [
    "#95ADCF",  # accent steel blue
    "#7B68EE",  # secondary purple
    "#4A90E2",  # primary blue
    "#A594F9",  # light purple
    "#6C63FF",  # accent purple
    "#AEC3E0",  # accent hover
]

# Sequential scale used for heatmaps
HEATMAP_SCALE = [
    [0.0, "#20242a"],
    [0.25, "#3a4a66"],
    [0.55, "#6383b0"],
    [0.85, "#95ADCF"],
    [1.0, "#AEC3E0"],
]


def _build_template() -> go.layout.Template:
    template = go.layout.Template()
    template.layout = go.Layout(
        paper_bgcolor=BG,
        plot_bgcolor=SURFACE,
        font=dict(color=TEXT, family="sans-serif", size=13),
        title=dict(font=dict(color=TEXT, size=16)),
        colorway=COLORWAY,
        xaxis=dict(
            gridcolor=BORDER,
            zerolinecolor=BORDER,
            linecolor=BORDER,
            tickfont=dict(color=TEXT_MUTED),
            title=dict(font=dict(color=TEXT_MUTED)),
        ),
        yaxis=dict(
            gridcolor=BORDER,
            zerolinecolor=BORDER,
            linecolor=BORDER,
            tickfont=dict(color=TEXT_MUTED),
            title=dict(font=dict(color=TEXT_MUTED)),
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=TEXT),
            bordercolor=BORDER,
        ),
        margin=dict(l=40, r=20, t=50, b=40),
    )
    return template


# Register & set as default
pio.templates["datalab_dark"] = _build_template()
pio.templates.default = "datalab_dark"


def apply_dark(fig: go.Figure) -> go.Figure:
    """Apply the datalab dark template to a figure (idempotent)."""
    fig.update_layout(template="datalab_dark")
    return fig
