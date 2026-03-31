import os
import json

import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
voice_model = genai.GenerativeModel("gemini-2.5-flash")


def _clean_json_text(text: str) -> str:
    clean = text.strip()
    if clean.startswith("```json"):
        clean = clean[7:]
    if clean.startswith("```"):
        clean = clean[3:]
    if clean.endswith("```"):
        clean = clean[:-3]
    return clean.strip()


def generate_questions(skills: str, job_role: str, experience: str):
    """
    Use Gemini to generate 5 structured interview questions.
    Returns a list of dicts: [{ "question": "..." }, ...]
    """
    prompt = f"""
You are a technical interviewer.

Generate 5 interview questions.

Skills: {skills}
Job Role: {job_role}
Experience: {experience}

Include:
* technical
* behavioral
* project
* problem solving

Return JSON:
[
  {{"question":""}},
  ...
]
"""
    try:
        response = voice_model.generate_content(prompt)
        raw = response.text or ""
        clean = _clean_json_text(raw)
        questions = json.loads(clean)
        if not isinstance(questions, list):
            return []
        normalized = []
        for q in questions:
            if isinstance(q, dict) and q.get("question"):
                normalized.append({"question": str(q["question"]).strip()})
            elif isinstance(q, str):
                normalized.append({"question": q.strip()})
        return normalized[:5]
    except Exception:
        return []


def evaluate_answer(question: str, answer: str):
    """
    Use Gemini to score and give feedback for an answer.
    Returns dict: { score:int, feedback:str, tips:str }
    """
    prompt = f"""
You are an interviewer.

Question: {question}
Answer: {answer}

Give score 0-10
Give feedback
Give improvement tips

Return JSON:
{{
  "score": 0-10,
  "feedback": "",
  "tips": ""
}}
"""
    try:
        response = voice_model.generate_content(prompt)
        raw = response.text or ""
        clean = _clean_json_text(raw)
        data = json.loads(clean)
        score = int(data.get("score", 0))
        score = max(0, min(10, score))
        return {
            "score": score,
            "feedback": str(data.get("feedback", "")).strip(),
            "tips": str(data.get("tips", "")).strip(),
        }
    except Exception:
        return {
            "score": 0,
            "feedback": "Unable to evaluate the answer due to an AI error.",
            "tips": "Try to give a clear, structured answer with examples next time.",
        }

