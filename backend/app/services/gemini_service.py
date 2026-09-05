import os
import json
import logging
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GROQ_API_KEY", "").strip()

if not api_key:
    # Attempt to load without path if running in Docker / cloud env
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY", "").strip()

client = Groq(api_key=api_key) if api_key else None

CANDIDATE_MODELS = [
    "qwen/qwen3.8-27b",
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b",
]


def analyze_answer(
    concept: str,
    question: str,
    student_answer: str
) -> str:
    global client
    if not client:
        curr_key = os.getenv("GROQ_API_KEY", "").strip()
        if not curr_key:
            raise RuntimeError("GROQ_API_KEY is not configured")
        client = Groq(api_key=curr_key)

    prompt = f"""You are SAGE, an adaptive AI teacher.

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

    last_error = None
    for model_name in CANDIDATE_MODELS:
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2
            )
            raw = response.choices[0].message.content or ""
            
            # Extract JSON from response
            start = raw.find('{')
            end = raw.rfind('}')
            if start != -1 and end != -1 and end > start:
                json_str = raw[start:end+1]
                # Validate it parses
                json.loads(json_str)
                return json_str
            
            return raw
        except Exception as e:
            logger.warning(f"Model {model_name} failed: {e}")
            last_error = e
            continue

    if last_error:
        raise last_error
    raise RuntimeError("Failed to generate analysis from AI models")