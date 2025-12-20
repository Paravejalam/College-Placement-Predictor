# logic/ats.py
import re

def calculate_ats_score(
    jd_text: str,
    resume_text: str,
    user_inputs=None
) -> float:
    """
    Hybrid ATS score:
    - Resume ↔ JD keyword match
    - Profile strength boost from inputs
    """

    if not jd_text or not resume_text:
        return 0.0

    # -------- Resume vs JD matching --------
    jd_words = set(re.findall(r"\w+", jd_text.lower()))
    resume_words = set(re.findall(r"\w+", resume_text.lower()))

    if not jd_words:
        base_ats = 0.0
    else:
        base_ats = (len(jd_words & resume_words) / len(jd_words)) * 100

    # -------- HARD GUARD (VERY IMPORTANT) --------
    if not isinstance(user_inputs, dict):
        return round(min(base_ats, 100), 2)

    # -------- Profile boost --------
    boost = 0.0
    boost += user_inputs.get("cgpa", 0) * 2
    boost += user_inputs.get("internships", 0) * 5
    boost += user_inputs.get("projects", 0) * 3
    boost += user_inputs.get("certifications", 0) * 2

    final_ats = min(base_ats + boost, 100)
    return round(final_ats, 2)
