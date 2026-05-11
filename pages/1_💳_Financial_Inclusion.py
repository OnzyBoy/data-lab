"""Project 1 — Financial Inclusion Predictor (Flagship)."""
import streamlit as st
import plotly.graph_objects as go

from components.theme import page_setup
from components.footer import render_footer
from utils.plotting import apply_dark, ACCENT, HEATMAP_SCALE

page_setup("Financial Inclusion", icon="💳")

LIVE_APP = (
    "https://financeinclusionea.streamlit.app/"
)
COLAB_URL = "https://colab.research.google.com/drive/1M60aX7rysGftwpgyINoQhiUxnl7VMLc6"
REPO_URL = "https://github.com/OnzyBoy/Financial-Inclusion-in-East-Africa"

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
        <h1>Financial Inclusion Predictor</h1>
        <p>
            A Random-Forest classifier predicting whether an individual in East Africa
            owns a bank account, trained on demographic and socioeconomic features
            from the Zindi Financial Inclusion challenge. Live, deployed, and tuned
            for recall — because in financial inclusion, missing the unbanked is the
            costly error.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Behind the Scenes ────────────────────────────────────────────────────────
st.markdown('<h2 class="section-title">🔬 Behind the Scenes</h2>', unsafe_allow_html=True)
st.write(
    "Anyone can wire a UI to a `.pkl` file. The interesting part is the math, "
    "the trade-offs, and *why* this model behaves the way it does."
)

# Metrics row
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Accuracy", "0.8164")
c2.metric("Precision", "0.4151")
c3.metric("Recall", "0.7462")
c4.metric("F1 Score", "0.5335")
c5.metric("ROC AUC", "0.8712")

st.info(
    "**Why high recall over precision?** In financial-inclusion outreach, a false "
    "negative (missing an unbanked person who could benefit from services) costs "
    "more than a false positive (extra outreach to someone already banked). "
    "The model is intentionally tuned to catch true positives, accepting some "
    "noise in exchange.",
    icon="🎯",
)

# ── Expander 1: Model Architecture ────────────────────────────────────────────
with st.expander("🧠 View Model Architecture (illustrative)", expanded=False):
    st.caption(
        "Illustrative reconstruction of the Random-Forest pipeline. "
        f"The exact code lives in the [Colab notebook ↗]({COLAB_URL})."
    )
    st.code(
        '''import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

df = pd.read_csv("Train.csv")
y = (df["bank_account"] == "Yes").astype(int)
X = df.drop(columns=["bank_account", "uniqueid", "year"])

categorical = [
    "country", "location_type", "cellphone_access", "gender_of_respondent",
    "relationship_with_head", "marital_status", "education_level", "job_type",
]
numeric = ["household_size", "age_of_respondent"]

preprocess = ColumnTransformer([
    ("num", StandardScaler(), numeric),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
])

pipe = Pipeline([
    ("prep", preprocess),
    ("clf", RandomForestClassifier(
        n_estimators=400,
        max_depth=14,
        min_samples_leaf=4,
        class_weight="balanced",   # ← tilts the model toward recall
        n_jobs=-1,
        random_state=42,
    )),
])

X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42,
)
pipe.fit(X_tr, y_tr)

proba = pipe.predict_proba(X_te)[:, 1]
pred  = (proba >= 0.35).astype(int)   # recall-leaning threshold

print("Accuracy :", accuracy_score(y_te, pred))
print("Precision:", precision_score(y_te, pred))
print("Recall   :", recall_score(y_te, pred))
print("F1       :", f1_score(y_te, pred))
print("ROC AUC  :", roc_auc_score(y_te, proba))
''',
        language="python",
    )

# ── Expander 2: Confusion Matrix ──────────────────────────────────────────────
with st.expander("📊 Confusion Matrix", expanded=False):
    cm_labels = ["No Bank Account", "Has Bank Account"]
    cm_values = [
        [3347, 696],
        [168, 494],
    ]
    annotations_text = [[str(v) for v in row] for row in cm_values]

    cm_fig = go.Figure(
        data=go.Heatmap(
            z=cm_values,
            x=cm_labels,
            y=cm_labels,
            text=annotations_text,
            texttemplate="%{text}",
            textfont=dict(size=18, color="#F4F4F4"),
            colorscale=HEATMAP_SCALE,
            showscale=True,
            hovertemplate=(
                "True: <b>%{y}</b><br>Predicted: <b>%{x}</b><br>"
                "Count: %{z}<extra></extra>"
            ),
        )
    )
    cm_fig.update_layout(
        title="Confusion Matrix — Random Forest (Test Set)",
        xaxis_title="Predicted Label",
        yaxis_title="True Label",
        yaxis=dict(autorange="reversed"),
        height=460,
    )
    apply_dark(cm_fig)
    st.plotly_chart(cm_fig, use_container_width=True)

    st.markdown(
        """
        **Reading the matrix**
        - **3,347** true negatives — correctly identified people without bank accounts.
        - **494** true positives — correctly flagged people who *do* have bank accounts.
        - **168** false negatives — missed banked individuals (low, which is great for recall).
        - **696** false positives — predicted "has bank account" when they don't (the cost of recall-tuning).
        """
    )

# ── Expander 3: Feature Importance ────────────────────────────────────────────
with st.expander("⭐ Top 10 Feature Importances", expanded=True):
    features = [
        "education_level",
        "cellphone_access",
        "age_of_respondent",
        "country_Kenya",
        "job_type_Formally employed Private",
        "location_type",
        "household_size",
        "job_type_Formally employed Government",
        "gender_of_respondent",
        "relationship_with_head_Head of Household",
    ]
    importance = [0.285, 0.153, 0.098, 0.061, 0.057, 0.043, 0.039, 0.032, 0.031, 0.026]

    fi_fig = go.Figure(
        go.Bar(
            x=importance[::-1],
            y=features[::-1],
            orientation="h",
            marker=dict(
                color=importance[::-1],
                colorscale=HEATMAP_SCALE,
                line=dict(color="#35363a", width=1),
            ),
            text=[f"{v:.3f}" for v in importance[::-1]],
            textposition="outside",
            textfont=dict(color="#F4F4F4"),
            hovertemplate="<b>%{y}</b><br>Importance: %{x:.3f}<extra></extra>",
        )
    )
    fi_fig.update_layout(
        title="Top 10 Most Important Features (Random Forest)",
        xaxis_title="Importance",
        yaxis_title="",
        height=520,
        margin=dict(l=200, r=60, t=50, b=40),
    )
    apply_dark(fi_fig)
    st.plotly_chart(fi_fig, use_container_width=True)

    st.markdown(
        """
        **What the model learned**
        - **Education level** dominates (≈28.5% of total importance) — formal
          schooling is the single strongest signal of financial inclusion.
        - **Cellphone access** is second (≈15.3%) — mobile money has effectively
          merged with banking access in East Africa.
        - **Age** matters more than gender, household size, or relationship status —
          consistent with banking adoption curves across the region.
        - **Country = Kenya** carrying its own weight reflects Kenya's outsized
          M-Pesa-driven banking penetration vs. Rwanda, Tanzania, and Uganda.
        """
    )

# ── Links ─────────────────────────────────────────────────────────────────────
st.markdown('<h2 class="section-title">📚 Resources</h2>', unsafe_allow_html=True)
b1, b2, b3 = st.columns(3)
with b1:
    st.link_button("🚀 Launch Live App ↗", LIVE_APP, use_container_width=True)
with b2:
    st.link_button("📓 Open Colab Notebook ↗", COLAB_URL, use_container_width=True)
with b3:
    st.link_button("💻 View GitHub Repo ↗", REPO_URL, use_container_width=True)

render_footer()
