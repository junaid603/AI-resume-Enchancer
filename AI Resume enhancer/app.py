import streamlit as st
from ai_engine import generate_response
from PyPDF2 import PdfReader

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Resume Enhancer",
    page_icon="🚀",
    layout="wide"
)

# =========================
# SESSION STATE
# =========================
if "page" not in st.session_state:
    st.session_state.page = "landing"


def go_to_app():
    st.session_state.page = "app"


# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Dancing+Script:wght@600;700&family=Caveat:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(-45deg, #0f172a, #1e1b4b, #0b1020, #111827);
    background-size: 400% 400%;
    animation: gradientMove 12s ease infinite;
}

@keyframes gradientMove {
    0% {background-position:0% 50%;}
    50% {background-position:100% 50%;}
    100% {background-position:0% 50%;}
}

.main-title {
    text-align: center;
    font-family: 'Dancing Script', cursive;
    font-size: 72px;
    color: #60a5fa;
    text-shadow: 0 0 20px rgba(96,165,250,0.6);
}

.sub-title {
    text-align: center;
    font-size: 24px;
    color: #cbd5e1;
    margin-bottom: 40px;
}

.glass-box {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(18px);
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 20px;
}

.upload-title {
    font-family: 'Caveat', cursive;
    font-size: 32px;
    color: #60a5fa;
    margin-bottom: 15px;
}

.section-card {
    background: rgba(15,23,42,0.82);
    border-radius: 18px;
    padding: 25px;
    margin-top: 25px;
    border: 1px solid rgba(255,255,255,0.08);
}

.section-title {
    color: #60a5fa;
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 15px;
}

.result-item {
    background: rgba(255,255,255,0.05);
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 10px;
    color: #e2e8f0;
}

div.stButton > button {
    width: 240px;
    margin: auto;
    display: block;
    background: linear-gradient(135deg, #4F8BF9, #7c3aed);
    color: white;
    border-radius: 14px;
    border: none;
    font-size: 18px;
    font-weight: bold;
    padding: 12px;
}

div.stButton > button:hover {
    transform: scale(1.03);
}

</style>
""", unsafe_allow_html=True)

# =========================
# FILE READER
# =========================
def extract_text(file):

    if file is None:
        return ""

    if file.type == "application/pdf":

        pdf = PdfReader(file)

        text = ""

        for page in pdf.pages:
            text += page.extract_text() or ""

        return text

    elif file.type == "text/plain":

        return str(file.read(), "utf-8")

    return ""


# =========================
# LANDING PAGE
# =========================
if st.session_state.page == "landing":

    st.markdown(
        '<div class="main-title">🚀 AI Resume Enhancer</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">Build your future with AI-powered resume analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div style="text-align:center; color:#cbd5e1; font-size:18px;">
        ✨ Analyze your resume<br><br>
        ⚡ Match with job descriptions<br><br>
        📊 Get instant AI feedback
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.button("Continue 🚀", on_click=go_to_app)

# =========================
# MAIN APP
# =========================
else:

    st.markdown(
        '<div class="main-title">🚀 AI Resume Enhancer</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    # =========================
    # RESUME SECTION
    # =========================
    with col1:

        st.markdown("""
        <div class="glass-box">
            <div class="upload-title">
                📄 Upload Your Resume
            </div>
        </div>
        """, unsafe_allow_html=True)

        resume_text = st.text_area(
            "Paste Resume",
            height=250
        )

        resume_file = st.file_uploader(
            "Upload Resume",
            type=["pdf", "txt"]
        )

        if resume_file:
            resume_text = extract_text(resume_file)
            st.success("Resume Loaded ✔")

    # =========================
    # JOB DESCRIPTION SECTION
    # =========================
    with col2:

        st.markdown("""
        <div class="glass-box">
            <div class="upload-title">
                💼 Upload Job Description
            </div>
        </div>
        """, unsafe_allow_html=True)

        job_text = st.text_area(
            "Paste Job Description",
            height=250
        )

        job_file = st.file_uploader(
            "Upload Job Description",
            type=["pdf", "txt"],
            key="job_upload"
        )

        if job_file:
            job_text = extract_text(job_file)
            st.success("Job Description Loaded ✔")

    # =========================
    # ANALYZE BUTTON
    # =========================
    st.markdown("---")

    if st.button("⚡ Analyze Resume & Job Match"):

        if resume_text and job_text:

            with st.spinner("AI is analyzing your profile..."):

                result = generate_response(
                    resume_text,
                    job_text
                )

            # =========================
            # EXTRACT DATA
            # =========================
            match_score = result.get("match_score", 0)
            strengths = result.get("strengths", [])
            missing_skills = result.get("missing_skills", [])
            improvements = result.get("improvements", [])
            cover_letter = result.get("cover_letter", "")

            # =========================
            # SCORE SECTION
            # =========================
            st.markdown("## 📊 ATS Match Score")

            # THIS FIXES THE HTML ISSUE
            st.metric(
                label="Resume Match",
                value=f"{match_score}%"
            )

            # =========================
            # STRENGTHS
            # =========================
            st.markdown("""
            <div class="section-card">
                <div class="section-title">
                    ✅ Strengths
                </div>
            </div>
            """, unsafe_allow_html=True)

            for item in strengths:
                st.markdown(
                    f'<div class="result-item">• {item}</div>',
                    unsafe_allow_html=True
                )

            # =========================
            # MISSING SKILLS
            # =========================
            st.markdown("""
            <div class="section-card">
                <div class="section-title">
                    ⚠ Missing Skills
                </div>
            </div>
            """, unsafe_allow_html=True)

            for item in missing_skills:
                st.markdown(
                    f'<div class="result-item">• {item}</div>',
                    unsafe_allow_html=True
                )

            # =========================
            # IMPROVEMENTS
            # =========================
            st.markdown("""
            <div class="section-card">
                <div class="section-title">
                    🚀 Improvements
                </div>
            </div>
            """, unsafe_allow_html=True)

            for item in improvements:
                st.markdown(
                    f'<div class="result-item">• {item}</div>',
                    unsafe_allow_html=True
                )

            # =========================
            # COVER LETTER
            # =========================
            st.markdown("""
            <div class="section-card">
                <div class="section-title">
                    📄 AI Cover Letter
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.text_area(
                "",
                value=cover_letter,
                height=250
            )

        else:

            st.warning(
                "⚠️ Please provide both Resume and Job Description"
            )

    st.markdown("<br>")

    if st.button("⬅ Back to Home"):

        st.session_state.page = "landing"