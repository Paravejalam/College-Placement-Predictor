import streamlit as st
from utils.constants import DOMAIN_OPTIONS

def render_inputs(auto_data=None):
    auto_data = auto_data or {}

    cgpa = st.number_input("CGPA (0–10)", 0.0, 10.0, 7.0)
    internships = st.number_input("Internships", 0, 10, auto_data.get("internships", 0))
    projects = st.number_input("Projects", 0, 10, auto_data.get("projects", 0))
    certifications = st.number_input("Certifications", 0, 10, auto_data.get("certifications", 0))

    communication = st.slider("Communication Skills", 1, 10, auto_data.get("communication", 5))
    aptitude = st.slider("Aptitude", 1, 10, auto_data.get("aptitude", 5))
    technical = st.slider("Technical Skills", 1, 10, auto_data.get("technical", 5))
    skills = st.slider("Skills Score", 0, 10, auto_data.get("skills", 5))

    domain = st.selectbox("Preferred Domain", DOMAIN_OPTIONS)
    

    return {
        "cgpa": cgpa,
        "internships": internships,
        "projects": projects,
        "certifications": certifications,
        "communication": communication,
        "aptitude": aptitude,
        "technical": technical,
        "domain": domain
    }
