"""Project 2 — Customer Support Urgency Intelligence System."""
import plotly.graph_objects as go
import streamlit as st

from components.theme import page_setup
from components.footer import render_footer
from utils.plotting import apply_dark, COLORWAY, HEATMAP_SCALE

page_setup("Support Urgency Intelligence", icon="🎫")

COLAB_URL = "https://colab.research.google.com/drive/1dLGpQ0FWOFlspg6OW_swgoeKMlWkYwHT"

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
        <h1>Support Urgency Intelligence System</h1>
        <p>
            An NLP-based urgency-scoring engine that re-prioritized <b>5,700 backlog
            tickets</b> at <b>99.64% accuracy</b> — built by engineering a Custom Urgency
            Index from sentiment, statistical complexity, and a pivot away from
            unreliable original labels.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Key metrics ───────────────────────────────────────────────────────────────
st.markdown('<h2 class="section-title">📈 Headline Metrics</h2>', unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)
m1.metric("Overall Accuracy", "99.64%", help="Weighted across 554 test samples")
m2.metric("Macro F1", "1.00", help="Per-class average")
m3.metric("Backlog Re-prioritized", "5,700")
m4.metric("Stack", "XGBoost + S-Transformers")

# ── The business challenge ────────────────────────────────────────────────────
st.markdown('<h2 class="section-title">🎯 The Business Challenge</h2>', unsafe_allow_html=True)
st.write(
    """
    Customer support teams drown in tickets. The original `Ticket Type` labels
    in this dataset were inconsistent and noisy — classifying *type* gave low
    accuracy and no operational value. The real question wasn't *"what kind of
    ticket is this?"* but *"which ticket should an agent open **next**?"*
    """
)

# ── Methodology ───────────────────────────────────────────────────────────────
st.markdown('<h2 class="section-title">🔬 Methodology</h2>', unsafe_allow_html=True)

with st.expander("1️⃣  Exploratory Data Analysis & Cleaning", expanded=True):
    st.markdown(
        """
        - Inspected distributions, missingness, and class balance across ticket types.
        - **Discovery:** a large fraction of `Time to Resolution` values were
          **negative** — caused by inverted timestamp ordering during data export.
        - **Fix:** took the absolute difference between resolution and creation
          timestamps, which restored a clean right-skewed resolution-time
          distribution.
        - Imputed missing categorical fields with `"Unknown"` and validated
          downstream tokenization.
        """
    )

with st.expander("2️⃣  The Failed First Attempt — Predicting Ticket Type"):
    st.markdown(
        """
        Trained a baseline classifier on the original `Ticket Type` labels.
        Accuracy plateaued well below useful thresholds. Confusion matrix
        showed labels were **inconsistently applied by humans** — the same
        ticket text mapped to different types across rows. The signal wasn't
        in the labels; it had to be engineered.
        """
    )

with st.expander("3️⃣  The Pivot — Engineering a Custom Urgency Index"):
    st.markdown(
        """
        Built a composite urgency score per ticket from:

        - **Sentiment score** — negative sentiment from a Sentence-Transformer
          embedding pipeline (frustrated / angry customers float to the top).
        - **Text complexity** — statistical metrics (length, lexical diversity,
          punctuation density, all-caps ratio) capturing escalation cues.
        - **Categorical priors** — channel, customer tier, and product line as
          weak signals.

        Discretized the index into **three Urgency Levels** (Low / Medium / High)
        for a learnable target.
        """
    )
    st.code(
        '''from sentence_transformers import SentenceTransformer
import numpy as np

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def urgency_index(row):
    emb = embedder.encode(row["ticket_text"])
    sentiment = sentiment_head(emb)                      # negative-class prob
    complexity = (
        0.4 * row["caps_ratio"]
      + 0.3 * row["punct_density"]
      + 0.3 * np.log1p(row["text_length"])
    )
    return 0.6 * sentiment + 0.4 * complexity

df["urgency_score"] = df.apply(urgency_index, axis=1)
df["urgency_level"] = pd.qcut(
    df["urgency_score"], q=3,
    labels=["Low", "Medium", "High"],
)''',
        language="python",
    )

with st.expander("4️⃣  Modeling — XGBoost on the Engineered Target"):
    st.markdown(
        """
        Trained an XGBoost classifier on the embedding-derived features +
        engineered numeric features, predicting `urgency_level`. Because the
        target is now mathematically grounded (not noisy human labels), the
        model converged to **99.64% accuracy** on a stratified hold-out split
        of 554 tickets.
        """
    )
    st.code(
        '''from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

X = df[feature_cols]
y = df["urgency_level"]

X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.1, stratify=y, random_state=42,
)

clf = XGBClassifier(
    n_estimators=600,
    max_depth=6,
    learning_rate=0.08,
    subsample=0.9,
    colsample_bytree=0.9,
    eval_metric="mlogloss",
    n_jobs=-1,
    random_state=42,
)
clf.fit(X_tr, y_tr)

print(classification_report(y_te, clf.predict(X_te)))
# Overall Accuracy: 99.64%''',
        language="python",
    )

    st.markdown("**Urgency Intelligence Report Card**")
    st.code(
        """                precision    recall  f1-score   support

   Low Urgency       0.99      0.99      0.99       140
Medium Urgency       1.00      1.00      1.00       362
  High Urgency       1.00      1.00      1.00        52

      accuracy                           1.00       554
     macro avg       1.00      1.00      1.00       554
  weighted avg       1.00      1.00      1.00       554

Overall Accuracy: 99.64%""",
        language="text",
    )

with st.expander("5️⃣  Deployment — Scoring the Open Backlog"):
    st.markdown(
        """
        Applied the trained urgency model to **5,700 open and pending tickets**.
        Output: a re-prioritized queue with `urgency_score` and `urgency_level`
        per ticket. Final prioritization summary:

        | Urgency Level | Tickets |
        |---|---:|
        | Medium | 3,767 |
        | Low | 1,494 |
        | High | 439 |

        Estimated benefit (from a sample review):

        - High-urgency tickets surfaced in the top tier previously sat
          mid-queue for hours.
        - Triage time per agent drops because the queue ordering does the
          first pass of cognitive work.
        """
    )

# ── Backlog distribution ──────────────────────────────────────────────────────
st.markdown(
    '<h2 class="section-title">📊 Backlog After Re-prioritization</h2>',
    unsafe_allow_html=True,
)
st.caption("Final urgency-level distribution across the 5,700-ticket backlog.")

levels = ["Low", "Medium", "High"]
counts = [1494, 3767, 439]
dist = go.Figure(
    go.Bar(
        x=levels,
        y=counts,
        marker=dict(
            color=COLORWAY[:3],
            line=dict(color="#35363a", width=1),
        ),
        text=counts,
        textposition="outside",
        textfont=dict(color="#F4F4F4"),
        hovertemplate="<b>%{x}</b><br>Tickets: %{y:,}<extra></extra>",
    )
)
dist.update_layout(
    xaxis_title="Urgency Level",
    yaxis_title="Tickets in Backlog",
    height=420,
    showlegend=False,
)
apply_dark(dist)
st.plotly_chart(dist, use_container_width=True)

s1, s2, s3 = st.columns(3)
s1.metric("Low priority", "1,494", help="26.2% of backlog")
s2.metric("Medium priority", "3,767", help="66.1% of backlog")
s3.metric("High priority", "439", help="7.7% of backlog — surfaced for immediate triage")

# ── Key insights ──────────────────────────────────────────────────────────────
st.markdown('<h2 class="section-title">💡 Key Insights</h2>', unsafe_allow_html=True)
st.markdown(
    """
    - **Sometimes the label is the problem.** A failed model surfaced a data
      issue more valuable than any predictor would have been.
    - **Composite engineered targets** can outperform direct prediction when
      raw labels are noisy — the index encodes operational intent, not just
      historical labeling habits.
    - **Sentence-Transformers are cheap leverage** for any text-classification
      task; a 384-dim MiniLM embedding handles most non-domain-specific signal.
    - **439 critical tickets** out of 5,700 (≈7.7%) is the actionable signal —
      a manageable queue for an agent to clear *first*, instead of grinding
      through the backlog FIFO.
    - **99.64% on engineered targets isn't magic** — it's the model rediscovering
      the deterministic-ish formula we built. The real win is the *operational*
      lift, not the metric.
    """
)

# ── Resources ─────────────────────────────────────────────────────────────────
st.markdown('<h2 class="section-title">📚 Resources</h2>', unsafe_allow_html=True)
st.link_button("📓 Open Colab Notebook ↗", COLAB_URL, use_container_width=False)
st.caption("This project lives in Colab — not currently on GitHub.")

render_footer()
