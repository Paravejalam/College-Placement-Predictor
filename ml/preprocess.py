import numpy as np
import re
from io import BytesIO

# Optional PDF text extraction
try:
    import PyPDF2
    PDF_AVAILABLE = True
except Exception:
    PDF_AVAILABLE = False


# --------------------------------------------------
# Helper: Extract text from PDF
# --------------------------------------------------
def extract_text_from_pdf(uploaded_file):
    if not PDF_AVAILABLE:
        return ""

    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text.lower()
    except Exception:
        return ""


# --------------------------------------------------
# Helper: Auto-fill features from resume text
# (very simple keyword-based logic)
# --------------------------------------------------
def auto_fill_features(text: str):
    auto = {}

    # internships
    auto["internships"] = len(re.findall(r"intern", text))

    # projects
    auto["projects"] = len(re.findall(r"project", text))

    # certifications
    auto["certifications"] = len(re.findall(r"certificat", text))

    # basic skill heuristics
    tech_keywords = ["python", "java", "sql", "ml", "data", "numpy", "pandas"]
    tech_score = sum(1 for k in tech_keywords if k in text)

    auto["technical"] = min(10, max(3, tech_score))
    auto["communication"] = 6 if "communication" in text else 5
    auto["aptitude"] = 6 if "aptitude" in text else 5

    return auto


# --------------------------------------------------
# MAIN FUNCTION USED BY app.py
# --------------------------------------------------
def prepare_input(user_inputs: dict, uploaded_file=None):
    """
    Returns: numpy array of shape (1, 9)
    Feature order MUST match training:
    [
      cgpa,
      internships,
      projects,
      certifications,
      aptitude_score,
      technical_score,
      communication_score,
      skills,
      domain_encoded
    ]
    """

    # ------------------------------
    # Default base features
    # ------------------------------
    features = {
        "cgpa": float(user_inputs.get("cgpa", 7.0)),
        "internships": int(user_inputs.get("internships", 0)),
        "projects": int(user_inputs.get("projects", 0)),
        "certifications": int(user_inputs.get("certifications", 0)),
        "aptitude_score": int(user_inputs.get("aptitude_score", 5)),
        "technical_score": int(user_inputs.get("technical_score", 5)),
        "communication_score": int(user_inputs.get("communication_score", 5)),
        "skills": int(user_inputs.get("skills", 5)),
        "domain_encoded": int(user_inputs.get("domain_encoded", 0)),
    }

    # ------------------------------
    # Resume-based auto-fill
    # ------------------------------
    if uploaded_file is not None:
        try:
            text = extract_text_from_pdf(uploaded_file)
            auto = auto_fill_features(text)

            features["internships"] = auto.get("internships", features["internships"])
            features["projects"] = auto.get("projects", features["projects"])
            features["certifications"] = auto.get("certifications", features["certifications"])
            features["technical_score"] = auto.get("technical", features["technical_score"])
            features["communication_score"] = auto.get("communication", features["communication_score"])
            features["aptitude_score"] = auto.get("aptitude", features["aptitude_score"])

        except Exception:
            pass  # fail-safe

    # ------------------------------
    # FINAL MODEL INPUT (VERY IMPORTANT)
    # ------------------------------
    X = np.array([[
        features["cgpa"],
        features["internships"],
        features["projects"],
        features["certifications"],
        features["aptitude_score"],
        features["technical_score"],
        features["communication_score"],
        features["skills"],
        features["domain_encoded"],
    ]], dtype=float)

    return X
