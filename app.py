import streamlit as st
import numpy as np
import joblib
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from utils.resume_parser import extract_text_from_pdf, derive_simple_features_from_text
import re
from logic.what_if import what_if_simulator
from pathlib import Path
try:
    import shap
    SHAP_AVAILABLE = True
except Exception:
    SHAP_AVAILABLE = False
    
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("styles/base.css")
load_css("styles/mobile.css")

from ml.preprocess import prepare_input
from logic.ats import calculate_ats_score
from logic.suggestions import generate_suggestions
from reports.report import generate_pdf_report
# -------------------------
# MODEL METADATA
# -------------------------
MODEL_NAME = "Logistic Regression"
MODEL_VERSION = "v1"

# ===============================
# 🔒 SESSION STATE INITIALIZATION
# ===============================

DEFAULT_STATE = {
    "prediction_done": False,
    "prediction_prob": None,
    "base_prediction_prob": None,
    "model_input": None,
    "left_input_snapshot": None,
    "last_inputs_dict": None,
    "resume_autofilled": None,
    "resume_text": None,
}

for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ===============================
# 🔁 RESET FUNCTION (LEFT INPUTS ONLY)
# ===============================
def reset_results():
    if not st.session_state.get("in_what_if_mode", False):
       st.session_state.prediction_done = False
    st.session_state.prediction_prob = None
    st.session_state.base_prediction_prob = None
    st.session_state.model_input = None
    st.session_state.left_input_snapshot = None
    
# -------------------------
# RESET ON LEFT INPUT CHANGE (ONLY LEFT PANEL)
# -------------------------
def reset_on_left_input_change():
    if st.session_state.get("prediction_done", False):
        st.session_state.prediction_done = False
        st.session_state.prediction_prob = None
        st.session_state.base_prediction_prob = None    
    
# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="College Placement Predictor",
    layout="wide",
    page_icon="🎓"
)
# ----------------------------------
# HEADER
# ----------------------------------
st.markdown("""
<div style="background: linear-gradient(90deg, #1e3c72, #2a5298);
padding: 6px;
border-radius: 12px;
text-align: center;
margin-bottom: 30px;">

<h1 style="color: white;
font-size: 36px;
font-weight: 600;  
margin: 0;">
🎓 College Placement Predictor
</h1>

<p style="color: #dbe7ff;
font-size: 15px;
margin-top: 2px;
letter-spacing: 0.6px;
font-style: italic;
font-weight: 300;
opacity: 0.9;">
Predict placement chances • Understand strengths • Improve your profile
</p>
<p style="
color: rgba(255,255,255,0.75);
font-size:12px;
margin-top:6px;
letter-spacing:0.5px;">
Built using Data Analytics · Machine Learning · Streamlit
</p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# DARK MODE (FORCED)
# -------------------------------------------------
st.markdown("""
<style>
body { background-color: #0e1117; color: white; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* Reduce overall bottom padding */
.block-container {
    padding-bottom: 1rem !important;
}

/* Reduce space after last section (suggestions) */
div[data-testid="stVerticalBlock"]:last-of-type {
    margin-bottom: 0.5rem !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE INIT
# =========================
if "prediction_done" not in st.session_state:
    st.session_state.prediction_done = False

if "prediction_prob" not in st.session_state:
    st.session_state.prediction_prob = None

if "base_prediction_prob" not in st.session_state:
    st.session_state.base_prediction_prob = None

if "model_input" not in st.session_state:
    st.session_state.model_input = None

if "left_input_snapshot" not in st.session_state:
    st.session_state.left_input_snapshot = None

if "last_inputs_dict" not in st.session_state:
    st.session_state.last_inputs_dict = None
if "last_input_snapshot" not in st.session_state:
    st.session_state.last_input_snapshot = None
   

# -------------------------------------------------
# LOAD MODEL
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
model = joblib.load(BASE_DIR / "model" / "model.pkl")
# -------------------------------------------------
# Extract final model for SHAP (handles Pipeline)
# -------------------------------------------------
if hasattr(model, "named_steps"):
    clf = model.named_steps[list(model.named_steps.keys())[-1]]
else:
    clf = model

# -------------------------------------------------
# SIDEBAR (MODEL INFO — ALWAYS ON)
# -------------------------------------------------
with st.sidebar:
    st.title("⚙️ Settings")
    st.markdown("### 📊 Model Info")
    st.write("**Model:** Logistic Regression")
    st.write(f"**Version:** {MODEL_VERSION}")
    st.write("**Features:** 9")
    st.write("**Explainability:** SHAP (Waterfall)")
    st.write("**ATS Matching:** Enabled")
    
def init_inputs():
    defaults = {
        "cgpa": 0.0,
        "internships": 0,
        "projects": 0,
        "certifications": 0,
        "aptitude_score": 5,
        "technical_score": 5,
        "communication_score": 5,
        "overall_skills": 5,
        "domain": "Data Science" 
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_inputs()

# -------------------------------------------------
# MAIN LAYOUT
# -------------------------------------------------
left_col, right_col = st.columns([1.1, 1.3], gap="large")

# =================================================
# LEFT PANEL — USER INPUTS (ONLY 9 FEATURES)
# =================================================

# ---------- RESET RESULT FUNCTION ----------
def reset_results():
    # ❗ What-if mode me kabhi bhi right side reset nahi hona chahiye
    if st.session_state.get("in_what_if_mode", False):
        return

    st.session_state.prediction_done = False
    st.session_state.prediction_prob = None
    st.session_state.base_prediction_prob = None
    st.session_state.model_input = None
    
# =================================================
# LEFT PANEL — USER INPUTS (ONLY 9 FEATURES)
# =================================================
with left_col:
    st.markdown("## Upload Resume + Manual Entry")

    uploaded_file = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"],
        key="resume_upload",
        )
    # ---------------- Resume change detection (FINAL) ----------------
    if uploaded_file is not None:
        current_file_id = f"{uploaded_file.name}_{uploaded_file.size}"

        if st.session_state.get("last_uploaded_file_id") != current_file_id:
            # New resume uploaded
            st.session_state.last_uploaded_file_id = current_file_id

            # FULL RESET (because resume changed)
            st.session_state.prediction_done = False
            st.session_state.prediction_prob = None
            st.session_state.base_prediction_prob = None
            st.session_state.model_input = None
            st.session_state.left_input_snapshot = None
            st.session_state.last_input_snapshot = None

            # clear resume derived data
            st.session_state.resume_text = None
            st.session_state.resume_autofilled = None

    if "left_input_snapshot" not in st.session_state:
     st.session_state.left_input_snapshot = None

    # -------------------------
    # ---------------- AUTO-FILL FROM RESUME (ONE TIME ONLY) ----------------
    if uploaded_file is not None and st.session_state.get("resume_autofilled") is None:
        try:
            resume_text = extract_text_from_pdf(uploaded_file)
        except Exception:
            st.error("Resume parsing failed in this environment.")
            resume_text = ""

        st.session_state.resume_text = resume_text
        extracted = derive_simple_features_from_text(resume_text)

        # 🔒 Autofill ONLY ONCE
        st.session_state.cgpa = extracted.get("cgpa", st.session_state.cgpa)
        st.session_state.internships = extracted.get("internships", st.session_state.internships)
        st.session_state.projects = extracted.get("projects", st.session_state.projects)
        st.session_state.certifications = extracted.get("certifications", st.session_state.certifications)

        st.session_state.aptitude_score = extracted.get(
            "aptitude_score", st.session_state.aptitude_score
        )
        st.session_state.technical_score = extracted.get(
            "technical_score", st.session_state.technical_score
        )
        st.session_state.communication_score = extracted.get(
            "communication_score", st.session_state.communication_score
        )
        st.session_state.overall_skills = extracted.get(
            "overall_skills", st.session_state.overall_skills
        )

        # ✅ mark autofill done (THIS IS THE KEY)
        st.session_state.resume_autofilled = uploaded_file.name

    # -------------------------
    # USER INPUTS (ALWAYS VISIBLE)
    # -------------------------
    cgpa = st.number_input(
        "CGPA (0-10)",
        min_value=0.0,
        max_value=10.0,
        step=0.1,
        key="cgpa",
        on_change=reset_on_left_input_change
    )

    internships = st.number_input(
        "Internships",
        min_value=0,
        step=1,
        key="internships",
        on_change=reset_on_left_input_change
    )

    projects = st.number_input(
        "Projects",
        min_value=0,
        step=1,
        key="projects",
        on_change=reset_on_left_input_change
    )

    certifications = st.number_input(
        "Certifications",
        min_value=0,
        step=1,
        key="certifications",
        on_change=reset_on_left_input_change
    )

    aptitude = st.slider(
        "Aptitude",
        0, 10,
        key="aptitude_score",
        on_change=reset_on_left_input_change
    )

    technical = st.slider(
        "Technical",
        0, 10,
        key="technical_score",
        on_change=reset_on_left_input_change
    )

    communication = st.slider(
        "Communication",
        0, 10,
        key="communication_score",
        on_change=reset_on_left_input_change
    )

    skills = st.slider(
        "Overall Skills",
        0, 10,
        key="overall_skills",
        on_change=reset_on_left_input_change
    )

    domain = st.selectbox(
        "Preferred Domain",
        [
            "Data Science",
            "Web Development",
            "Data Analytics",
            "Data Engineer",
            "Frontend Developer",
            "Backend Developer",
            "Other"
        ],
        key="domain",
        on_change=reset_on_left_input_change
    )

    # -------------------------
    # INPUT DICT (FOR MODEL)
    # -------------------------
    # 🔒 LOCK LEFT INPUTS ONLY (RESET CONTROL)
current_left_inputs = {
    "cgpa": st.session_state.cgpa,
    "internships": st.session_state.internships,
    "projects": st.session_state.projects,
    "certifications": st.session_state.certifications,
    "aptitude": st.session_state.aptitude_score,
    "technical": st.session_state.technical_score,
    "communication": st.session_state.communication_score,
    "overall_skills": st.session_state.overall_skills,
    "domain": st.session_state.domain,
}

# 👇 RESET ONLY WHEN LEFT INPUTS CHANGE
if st.session_state.prediction_done:
    if (
        st.session_state.left_input_snapshot is not None
        and current_left_inputs != st.session_state.left_input_snapshot
    ):
        reset_results()

# =================================================
# RIGHT PANEL — TARGET JD + RESULTS
# =================================================
# ---------- READ VALUES FROM SESSION STATE (SCOPE FIX) ----------
cgpa = st.session_state.cgpa
internships = st.session_state.internships
projects = st.session_state.projects
certifications = st.session_state.certifications
aptitude = st.session_state.aptitude_score
technical = st.session_state.technical_score
communication = st.session_state.communication_score
skills = st.session_state.overall_skills
domain = st.session_state.domain
with right_col:
    st.markdown("## 🎯 Profile Summary & Results")

    # ---------- JD INPUT ----------
    jd_text = st.text_area(
    "Target Job Description (ATS)",
    placeholder="Write or paste job description here to calculate ATS match...",
    key="job_description"
    )

    # ---------- CURRENT INPUT SNAPSHOT (RESET LOGIC) ----------
    current_inputs = (
    st.session_state.cgpa,
    st.session_state.internships,
    st.session_state.projects,
    st.session_state.certifications,
    st.session_state.aptitude_score,
    st.session_state.technical_score,
    st.session_state.communication_score,
    st.session_state.overall_skills,
    st.session_state.domain,
    )

    # init session state
    if "prediction_done" not in st.session_state:
        st.session_state.prediction_done = False
    if "last_inputs" not in st.session_state:
        st.session_state.last_inputs = None
    if "prediction_result" not in st.session_state:
        st.session_state.prediction_result = None
    if "ats_done" not in st.session_state:
        st.session_state.ats_done = False


    # ---------- PREDICT BUTTON ----------
    if st.button("🚀 Predict Placement", use_container_width=True):
        with st.spinner("🔄 Analyzing profile & calculating probability..."):
            st.session_state.in_what_if_mode = False
            st.session_state.last_inputs_dict = {
                "cgpa": cgpa,
                "internships": internships,
                "projects": projects,
                "certifications": certifications,
                "aptitude": aptitude,
                "technical": technical,
                "communication": communication,
                "overall skills": skills,
                "domain": domain,
                }
        model_input = np.array(
            prepare_input(st.session_state.last_inputs_dict),
            dtype=float
        ).reshape(1, -1)
        
        prob = model.predict_proba(model_input)[0][1] * 100
        st.session_state.left_input_snapshot = current_left_inputs.copy()

        # 🔒 LOCK VALUES
        st.session_state.prediction_done = True
        st.session_state.model_input = model_input
        st.session_state.prediction_prob = prob
        st.session_state.base_prediction_prob = prob
        
    # =====================================================
    # RESULT AREA (RIGHT SIDE ONLY)
    # ---------- ATS MATCHING ----------
    if st.session_state.prediction_done:
        jd_text = st.session_state.get("job_description", "").strip()

        if jd_text:
            ats_score = calculate_ats_score(
            jd_text=jd_text,
            resume_text=st.session_state.get("resume_text", ""),
            user_inputs=st.session_state.last_inputs_dict
           )

            st.session_state.ats_done = True

            st.markdown("## 📄 ATS Match Score")
            st.progress(ats_score / 100)
            st.write(f"**ATS Match:** {ats_score:.2f}%")

        else:
            st.info("ℹ️ Enter Job Description to view ATS match.")
            
        # -------- WHAT-IF SIMULATOR --------
        if st.session_state.prediction_done:
            what_if_simulator(
                model=model,
                base_inputs=st.session_state.left_input_snapshot,
                current_prob=st.session_state.prediction_prob
            )
            st.session_state.in_what_if_mode = True
    # =====================================================
    if st.session_state.prediction_done:
        # BUILD INPUT DICT AT PREDICT TIME (MOST IMPORTANT)
        live_input_dict = {
            "cgpa": st.session_state.cgpa,
            "internships": st.session_state.internships,
            "projects": st.session_state.projects,
            "certifications": st.session_state.certifications,
            "aptitude_score": st.session_state.aptitude_score,
            "technical_score": st.session_state.technical_score,
            "communication_score": st.session_state.communication_score,
            "skills": st.session_state.overall_skills,
            "domain": st.session_state.domain,
        }


        # ---------- PREPARE INPUT ----------
        X = prepare_input(live_input_dict, None)

        # ---------- PREDICTION ----------
        prob = model.predict_proba(X)[0][1] * 100

        # ---------- RESULT BANNER ----------
        if prob >= 70:
            st.markdown(
                f"""
                <div style="
                    background: linear-gradient(135deg,#1abc9c,#2ecc71);
                    padding:30px;
                    border-radius:16px;
                    text-align:center;
                    color:black;
                    font-size:22px;
                    font-weight:700;
                ">
                🎉🎉 CONGRATULATIONS 🎉🎉 <br><br>
                ✅ Strong Placement Potential 🔥<br><br>
                🚀 Placement Probability: {prob:.2f}%<br><br>
                🚀 Your profile is well-aligned with recruiter expectations
                </div>
                """,
                unsafe_allow_html=True
            )
            st.balloons()

        elif prob >= 60:
            st.success(f"🟢 Moderate Placement Potential ({prob:.2f}%) — Profile improvement recommended")

        else:
            st.error(f"🔴 Placement Risk Detected ({prob:.2f}%)")

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob,
            number={"suffix": "%"},
            title={"text": "Placement Probability"},
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickvals": [0, 20, 40, 60, 80, 100]
                },
                "bar": {"color": "#00ff99"},
                "steps": [
                    {"range": [0, 50], "color": "#7f1d1d"},
                    {"range": [50, 80], "color": "#92400e"},
                    {"range": [80, 100], "color": "#14532d"},
                ]
            },
        ))

        st.plotly_chart(fig, width="stretch")


        # -------- SHAP --------
        if st.session_state.get("prediction_done") and SHAP_AVAILABLE:

            st.markdown("## 🧠 Why This Prediction? (SHAP)")
            model_input = st.session_state.model_input

            FEATURE_NAMES = [
                "CGPA",
                "Internships",
                "Projects",
                "Certifications",
                "Aptitude Score",
                "Technical Score",
                "Communication Score",
                "Overall Skills",
                "Preferred Domain"
            ]

            explainer = shap.LinearExplainer(
                clf,
                np.zeros((1, model_input.shape[1]))
            )

            shap_values = explainer.shap_values(model_input)

            fig, ax = plt.subplots(figsize=(9, 4))
            shap.plots.waterfall(
                shap.Explanation(
                    values=shap_values[0],
                    base_values=explainer.expected_value,
                    feature_names=FEATURE_NAMES
                ),
                show=False
            )
            st.pyplot(fig)

            # -------- Explanation in Simple Words --------
            st.markdown("### 📌 Explanation in Simple Words")

            contributions = list(zip(FEATURE_NAMES, shap_values[0]))
            contributions.sort(key=lambda x: abs(x[1]), reverse=True)

            positives = [f for f, v in contributions if v > 0][:3]
            negatives = [f for f, v in contributions if v < 0][:3]

            if positives:
                st.success(
                    "Your placement probability increased mainly due to strong performance in **"
                    + ", ".join(positives)
                    + "**."
                )

            if negatives:
                st.warning(
                    "Your placement probability was reduced mainly due to relatively weaker performance in **"
                    + ", ".join(negatives)
                    + "**."
                )

        elif st.session_state.get("prediction_done"):
            st.info("🧠 SHAP explanation temporarily unavailable in this environment.")


        # ---------- IMPROVEMENT SUGGESTIONS ----------
        if st.session_state.get("prediction_done", False):
            st.markdown("## 🛠 Improvement Suggestions")
            suggestions = generate_suggestions(live_input_dict)

        if suggestions:
            for s in suggestions:
                st.write("•", s)
        else:
            st.info("Your profile looks balanced. No major improvements required.")
    
st.markdown("""
<hr style="border: none; height: 1px; background-color: #1f2937; margin-top: 40px;">

<div style="
text-align: center;
color: rgba(255,255,255,0.65);
font-size: 12px;
letter-spacing: 0.4px;
margin-bottom: 10px;">
Built by Paravej Alam · College Placement Predictor · Data Analytics Project
</div>
""", unsafe_allow_html=True)
