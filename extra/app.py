import streamlit as st
import fitz  # PyMuPDF
from utils.parser import extract_resume_data
from utils.jd_matcher import extract_jd_keywords
from utils.grammar_check import grammar_feedback
from utils.pdf_report import generate_pdf_report

# -------- Page Setup --------
st.set_page_config("AI Resume Evaluator", layout="wide")

# -------- Custom Background (Color or Image) --------
st.markdown("""
    <style>
    .main {
        background: linear-gradient(to bottom right, #e8f5e9, #ffffff);
        padding: 2rem;
    }
    .stButton > button {
        background-color: #388e3c;
        color: white;
        font-size: 16px;
        border-radius: 8px;
        padding: 10px 20px;
        margin-top: 10px;
    }
    .stDownloadButton > button {
        background-color: #1976d2;
        color: white;
        font-size: 15px;
        border-radius: 6px;
        padding: 8px 16px;
    }
    .stProgress > div > div {
        background-color: #43a047;
    }
    </style>
""", unsafe_allow_html=True)

# Optional: Use a background image instead
# st.markdown("""
# <style>
# .main {
#     background-image: url('https://www.transparenttextures.com/patterns/white-wall-3.png');
#     background-size: cover;
#     background-repeat: no-repeat;
# }
# </style>
# """, unsafe_allow_html=True)

# -------- Title --------
st.markdown("<h1 style='text-align:center; color:#2e7d32;'>🤖 AI Resume Evaluator</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>Upload your Resume or Paste LinkedIn Summary, Analyze Skills, Grammar, ATS Score & Download Report</h4>", unsafe_allow_html=True)
st.markdown("---")

# -------- Input Section --------
resume_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])
jd_input = st.text_area("📝 Paste Job Description (Optional)", height=150)
st.markdown("🔗 Or paste **LinkedIn Resume Summary** (copy from LinkedIn PDF or profile)")
linkedin_resume = st.text_area("📋 Paste LinkedIn Resume Text", height=150)

submit = st.button("🚀 Analyze Resume")

# -------- Logic --------
def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text.lower()

def score_match(resume_text, keyword_list):
    matched = [word for word in keyword_list if word in resume_text]
    missing = list(set(keyword_list) - set(matched))
    score = int((len(matched) / len(keyword_list)) * 100) if keyword_list else 0
    return matched, missing, score

if submit and (resume_file or linkedin_resume.strip()):
    resume_text = ""
    if resume_file:
        resume_text = extract_text_from_pdf(resume_file)
    if linkedin_resume.strip():
        resume_text = linkedin_resume.lower()

    st.markdown("## 👤 Resume Overview")
    resume_data = extract_resume_data(resume_text)
    st.json(resume_data)

    # Skill Matching
    if jd_input:
        st.markdown("## 🎯 JD-Based ATS Score")
        jd_keywords = extract_jd_keywords(jd_input)
        matched, missing, score = score_match(resume_text, jd_keywords)
        st.progress(score)
        st.success(f"✅ {score}% match with Job Description")
        st.markdown(f"**Matched Skills:** `{', '.join(matched)}`")
        st.markdown(f"**Missing Skills:** `{', '.join(missing)}`")
    else:
        st.markdown("## 🧠 General ATS Score")
        default_keywords = [
            'python', 'machine learning', 'deep learning', 'data analysis',
            'sql', 'nlp', 'tensorflow', 'pytorch', 'excel', 'scikit-learn',
            'communication', 'teamwork', 'git', 'pandas', 'numpy'
        ]
        matched, missing, score = score_match(resume_text, default_keywords)
        st.progress(score)
        st.info(f"Estimated ATS Score: {score}%")
        st.markdown(f"**Matched Skills:** `{', '.join(matched)}`")

    # Grammar Feedback
    st.markdown("## ✍️ Grammar Suggestions")
    grammar_count, grammar_issues = grammar_feedback(resume_text)
    st.markdown(f"**🛑 Issues Found:** {grammar_count}")
    if grammar_issues:
        for msg, snippet in grammar_issues[:5]:
            st.warning(f"💡 {msg}")
            st.code(snippet)
    else:
        st.success("✅ No major grammar issues found.")

    # PDF Report
    st.markdown("## 📥 Download PDF Report")
    if st.button("📄 Generate PDF Report"):
        pdf_path = generate_pdf_report(resume_data, score, matched, missing, grammar_issues)
        with open(pdf_path, "rb") as f:
            st.download_button("⬇️ Download Report", f, file_name="resume_report.pdf", mime="application/pdf")

elif submit:
    st.error("❗ Please upload a resume or paste LinkedIn text.")
