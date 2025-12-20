import streamlit as st

def render_header():
    st.markdown("""
    <div style="
        background: linear-gradient(135deg,#1e3a8a,#0f172a);
        padding:30px;
        border-radius:16px;
        text-align:center;
        color:white;">
        <h1>🎓 College Placement Predictor — Pro</h1>
        <p>Predict placement • Explain decisions • Improve profile</p>
    </div>
    """, unsafe_allow_html=True)
