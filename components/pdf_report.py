from fpdf import FPDF

def generate_pdf_report(result: dict) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, "College Placement Prediction Report", ln=True)
    pdf.ln(5)

    pdf.cell(0, 10, f"Placement Probability: {result['probability']}%", ln=True)
    pdf.cell(0, 10, f"ATS Match Score: {result['ats']}%", ln=True)

    # ✅ CORRECT WAY (fpdf expects bytes, not BytesIO)
    return pdf.output(dest="S").encode("latin-1")
