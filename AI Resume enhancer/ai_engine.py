import os
import json
import re
from dotenv import load_dotenv
import google.generativeai as genai

# =========================
# LOAD ENV
# =========================
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in .env")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash-lite")


# =========================
# PROMPT
# =========================
def build_prompt(resume_text, job_text):

    return f"""
You are an advanced ATS Resume Analyzer AI.

TASK:
Analyze the resume against the job description.

IMPORTANT RULES:
- Output ONLY valid JSON
- No markdown
- No HTML
- No explanations
- No extra text
- Keep everything concise and professional

RETURN EXACTLY THIS FORMAT:

{{
  "match_score": 0,
  "strengths": [],
  "missing_skills": [],
  "improvements": [],
  "cover_letter": ""
}}

SCORING:
- Give realistic ATS score from 0 to 100
- Missing skills should focus on technical + role-specific skills
- Cover letter should be professional and short

Resume:
{resume_text}

Job Description:
{job_text}
"""


# =========================
# CLEAN TEXT
# =========================
def clean_text(text):

    if not isinstance(text, str):
        return ""

    # Remove HTML tags
    text = re.sub(r"<.*?>", "", text)

    # Remove markdown symbols
    text = text.replace("*", "")
    text = text.replace("#", "")
    text = text.replace("`", "")

    return text.strip()


# =========================
# SAFE JSON PARSER
# =========================
def parse_response(text):

    if not isinstance(text, str):
        return fallback()

    try:

        start = text.find("{")
        end = text.rfind("}")

        if start == -1 or end == -1:
            return fallback()

        json_str = text[start:end + 1]

        data = json.loads(json_str)

        return {
            "match_score": min(max(int(data.get("match_score", 0)), 0), 100),

            "strengths": [
                clean_text(s)
                for s in data.get("strengths", [])[:10]
            ],

            "missing_skills": [
                clean_text(s)
                for s in data.get("missing_skills", [])[:10]
            ],

            "improvements": [
                clean_text(s)
                for s in data.get("improvements", [])[:10]
            ],

            "cover_letter": clean_text(
                str(data.get("cover_letter", ""))
            )
        }

    except Exception:
        return fallback()


# =========================
# FALLBACK
# =========================
def fallback():

    return {
        "match_score": 0,
        "strengths": ["Unable to generate response"],
        "missing_skills": [],
        "improvements": [],
        "cover_letter": "Error generating cover letter."
    }


# =========================
# MAIN FUNCTION
# =========================
def generate_response(resume_text, job_text):

    prompt = build_prompt(resume_text, job_text)

    response = model.generate_content(prompt)

    raw = response.text

    return parse_response(raw)