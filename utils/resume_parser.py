# utils/resume_parser.py

import PyPDF2
import re

def to_keyword_set(text):
    return set(
        w.lower()
        for w in re.findall(r"[a-zA-Z]{3,}", text)
    )


def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from uploaded PDF (Streamlit file uploader object)
    Returns combined text as string
    """
    text = ""

    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception:
        pass  # fail-safe

    return text.strip()

def derive_simple_features_from_text(text):
    """
    Very simple rule-based feature extraction from resume text
    Returns a dict compatible with app.py auto-fill
    """

    text_lower = text.lower()

    # --- CGPA ---
    cgpa = None
    cgpa_match = re.search(r'cgpa[:\s]*([0-9]\.?[0-9]?)', text_lower)
    if cgpa_match:
        try:
            cgpa = float(cgpa_match.group(1))
        except:
            cgpa = None

    # --- Count-based features ---
    internships = text_lower.count("intern")
    projects = text_lower.count("project")
    certifications = text_lower.count("certificat")

    # --- Skill-based rough scores (0–10 heuristic) ---
    technical_score = min(10, 3 + text_lower.count("python") + text_lower.count("java"))
    communication_score = min(10, 3 + text_lower.count("communication") + text_lower.count("presentation"))
    aptitude_score = min(10, 3 + text_lower.count("problem") + text_lower.count("algorithm"))
    overall_skills = min(10, round((technical_score + communication_score + aptitude_score) / 3))

    return {
        "cgpa": cgpa if cgpa is not None else 7.0,
        "internships": internships,
        "projects": projects,
        "certifications": certifications,
        "technical_score": technical_score,
        "communication_score": communication_score,
        "aptitude_score": aptitude_score,
        "overall_skills": overall_skills
    }
    

def extract_keywords(text):
    text = text.lower()
    words = re.findall(r"[a-zA-Z]{3,}", text)

    stopwords = {
        "the", "and", "with", "for", "from", "that", "this",
        "will", "have", "are", "you", "your", "our", "their",
        "experience", "knowledge", "skills", "ability", "using"
    }

    keywords = {w for w in words if w not in stopwords}
    return keywords


