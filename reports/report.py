# reports/report.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_pdf_report(input_dict, probability, ats_score, suggestions):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "College Placement Prediction Report")

    y -= 40
    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Placement Probability: {probability:.2f}%")

    y -= 25
    c.drawString(50, y, f"ATS Match Score: {ats_score}%")

    y -= 30
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Improvement Suggestions:")

    y -= 20
    c.setFont("Helvetica", 11)
    for s in suggestions:
        c.drawString(60, y, f"- {s}")
        y -= 15

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer.getvalue()
