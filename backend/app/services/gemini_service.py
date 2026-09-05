import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError("GROQ_API_KEY is not configured")

client = Groq(api_key=api_key)


def analyze_answer(
    concept: str,
    question: str,
    student_answer: str
):
    prompt = f"""
You are SAGE, an adaptive AI teacher.

Analyze the student's answer.

Concept: {concept}

Question:
{question}

Student Answer:
{student_answer}

Determine:
1. Whether the answer is correct.
2. The student's likely misconception, if any.
3. A short explanation suitable for a beginner.
4. What the teacher should do next.

Return ONLY valid JSON in this exact format:

{{
    "correct": true,
    "misconception": null,
    "explanation": "Short explanation",
    "teacher_action": "What SAGE should do next"
}}
"""

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content