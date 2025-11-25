import streamlit as st
import pandas as pd
import json
from pathlib import Path
import plotly.express as px

# ─── Page Config & CSS ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="💫 Mental Health Risk Detector",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
    <style>
      header, footer {visibility: hidden;}
      .stButton>button {background-color: #4CAF50; color: white; font-size:18px; height:3em;}
  .stSlider>div[data-baseweb~="slider"] {margin-bottom:1.5em;}
    </style>
""", unsafe_allow_html=True)

# ─── Paths & Resources ───────────────────────────────────────────────────────────
ROOT      = Path(__file__).parent
DATA_PATH = ROOT / "data" / "cleaned_survey.csv"
RES_PATH  = ROOT / "resources.json"

df        = pd.read_csv(DATA_PATH)
@@ -29,46 +30,65 @@

# ─── Sidebar Pie Chart ───────────────────────────────────────────────────────────
dist = df['RiskLevel'].value_counts().reset_index()
dist.columns = ['RiskLevel', 'Count']
fig = px.pie(
    dist,
    names='RiskLevel',
    values='Count',
    color='RiskLevel',
    color_discrete_map={'Low': '#4CAF50', 'Moderate': '#FFA726', 'High': '#EF5350'},
    title="Overall Risk Distribution"
)

with st.sidebar:
    st.header("📊 Stats")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("**Top Predictors:**\n1. Family History\n2. Benefits\n3. MH Stigma\n4. Remote Work\n---")
    st.write("Data set - Mental Health in Tech Survey,from kaggle")

# ─── Header & Quote Image ────────────────────────────────────────────────────────
st.markdown(
    "<h1 style='text-align:center;color:#4CAF50;'>Mental Health Risk Detector</h1>",
    unsafe_allow_html=True
)
st.write("A quick self-assessment to estimate your risk level and get resources.")

# Insert your local quote image here:
st.image(
    "Data\\mentalhealth.jpg",
    caption="“You, yourself, as much as anybody in the entire universe, deserve your love and affection.” – Buddha",
    use_container_width=True
)
st.write("---")

# ─── User Inputs ─────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    age         = st.slider("Age (20–65)", 20, 65, 30)
    gender      = st.selectbox("Gender", ["Male", "Female"])
    # 🔁 MODIFIED: remove NaN from self-employed options
    self_emp    = st.selectbox("Self-employed?", df.self_employed.dropna().unique())
    family_hist = st.selectbox("Family history of mental illness?", df.family_history.unique())

with col2:
    benefits  = st.selectbox("Mental-health benefits offered?", df.benefits.unique())
    mh_conseq = st.selectbox(
        "Do you think discussing your mental health at work could harm your career?",
        df.mental_health_consequence.unique()
    )
    remote_wk = st.selectbox("Do you work remotely?", df.remote_work.unique())

# ─── Rule-Based Scoring ───────────────────────────────────────────────────────────
score = 0
if family_hist == "Yes":
    score += 1
if benefits == "No":
    score += 1
if mh_conseq == "Yes":
    score += 1
if remote_wk == "Yes":
    score += 1

if score == 0:
    risk = "Low"
@@ -86,29 +106,36 @@
    else:
        st.warning("⚠️ High risk detected. Please consider reaching out for professional support.")

    color = {"Low": "#4CAF50", "Moderate": "#FFA726", "High": "#EF5350"}[risk]
    st.markdown(
        f"<h2 style='text-align:center;color:{color};'>Your Risk Level: {risk}</h2>",
        unsafe_allow_html=True
    )

    st.subheader("🎁 Recommended Resources")
    for tip in resources.get(risk, []):
        st.markdown(f":sparkles: {tip}")

    st.markdown(
        "<p style='text-align:center;'>Thank you for taking the assessment! 🌟</p>",
        unsafe_allow_html=True
    )

# ─── Learn More Section ─────────────────────────────────────────────────────────
st.write("---")
st.subheader("📚 Learn More About Mental Health")

topic = st.selectbox("What would you like to learn about?", [
    "What is Mental Health?",
    "Why Is Mental Health Important?",
    "Signs of Poor Mental Health",
    "Tips for Self-Care",
    "Where to Find Help"
])

if topic == "What is Mental Health?":
    st.write("""
Mental health refers to our emotional, psychological, and social well-being.  
It affects how we think, feel, and act in daily life, and influences how we handle stress, relate to others, and make choices.
    """)
elif topic == "Why Is Mental Health Important?":
@@ -123,13 +150,14 @@
- Changes in sleeping or eating habits  
- Difficulty concentrating or making decisions  
- Increased irritability, anger, or worry  

If you notice several of these lasting more than two weeks, consider reaching out for support.
    """)
elif topic == "Tips for Self-Care":
    st.write("""
- Keep a regular sleep schedule  
- Exercise at least 3× per week  
- Practice mindfulness or meditation (5–10 minutes daily)  
- Stay connected: call a friend or family member  
- Journaling: express your thoughts on paper  
- Set small, achievable daily goals  
