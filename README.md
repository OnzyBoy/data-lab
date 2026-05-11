# Aristo's Data Lab

A living portfolio of data analytics & machine-learning work, built with Streamlit.
Companion to the personal portfolio at **[aristoayako.vercel.app](https://aristoayako.vercel.app/)**.

> While Vercel tells you *what* I can do, the Data Lab *shows* you.

## ✨ Featured Projects

| | Project | Stack | Status |
|---|---|---|---|
| 💳 | **Financial Inclusion Predictor** | Python · Scikit-learn · Streamlit | Live + Embedded |
| 🎫 | **Support Urgency Intelligence** | NLP · XGBoost · Sentence-Transformers | Narrative + Code |
| 🩸 | **Blood Group Analysis** | Power BI · DAX · Excel | Screenshots + Recreations |
| 🎓 | **Certificates** | Verified credentials | Live links |

## 🚀 Run Locally

```bash
git clone https://github.com/OnzyBoy/data-lab.git
cd data-lab
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -r requirements.txt
streamlit run Home.py
```

The app opens at `http://localhost:8501`.

## 🗂️ Structure

```
data-lab/
├── .streamlit/config.toml         # Dark theme
├── assets/
│   ├── styles.css                 # Custom CSS (matches aristo-portfolio palette)
│   ├── images/                    # Project thumbnails & screenshots
│   └── certificates/              # Badge images
├── components/
│   ├── theme.py                   # CSS injector + page setup
│   ├── footer.py                  # Back-to-Vercel footer
│   ├── project_card.py            # Reusable project card
│   └── certificate_card.py        # Reusable certificate card
├── utils/
│   └── plotting.py                # Plotly dark template + colorway
├── pages/
│   ├── 1_💳_Financial_Inclusion.py
│   ├── 2_🎫_Support_Urgency_Intelligence.py
│   ├── 3_🩸_Blood_Group_Analysis.py
│   └── 4_🎓_Certificates.py
├── Home.py                        # Executive Dashboard (entry point)
└── requirements.txt
```

## 🎨 Theme

Palette mirrors the personal portfolio:

| Token | Hex |
|---|---|
| Background | `#18191A` |
| Surface | `#23272F` |
| Accent (steel blue) | `#95ADCF` |
| Text | `#F4F4F4` |
| Primary blue | `#4A90E2` |
| Secondary purple | `#7B68EE` |

Applied via `.streamlit/config.toml` plus an injected `assets/styles.css`. All
Plotly charts use a shared `datalab_dark` template registered in
`utils/plotting.py`.

## 🌐 Deployment

Hosted on **Streamlit Community Cloud**. Entry point: `Home.py`.

## 📍 Back to the Portfolio

[aristoayako.vercel.app ↗](https://aristoayako.vercel.app/#projects)
