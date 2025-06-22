from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile

def generate_pdf_report(resume_data, score, matched, missing, grammar_issues):
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(temp.name, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Resume Evaluation Report")

    y = height - 100
    c.setFont("Helvetica", 12)
    for key, value in resume_data.items():
        c.drawString(50, y, f"{key}: {value}")
        y -= 20

    c.drawString(50, y - 10, f"ATS Score: {score}%")
    y -= 40

    c.drawString(50, y, f"Matched Skills: {', '.join(matched)}")
    y -= 20
    c.drawString(50, y, f"Missing Skills: {', '.join(missing)}")
    y -= 40

    c.drawString(50, y, "Grammar Issues:")
    y -= 20
    for issue, snippet in grammar_issues[:5]:  # first 5
        c.drawString(60, y, f"- {issue}")
        y -= 15
        if y < 100: break

    c.save()
    return temp.name
