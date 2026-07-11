import os
import json
from pathlib import Path
from dotenv import load_dotenv
from google import genai

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def generate_quiz(topic, num_questions=5, difficulty="medium"):
    prompt = f"""Generate {num_questions} multiple-choice questions about "{topic}" at {difficulty} difficulty.

Return ONLY valid JSON, no other text, no markdown code fences. Format exactly like this:
{{
  "questions": [
    {{
      "question": "question text here",
      "options": ["option A", "option B", "option C", "option D"],
      "correct_index": 0,
      "explanation": "short explanation of why this is correct"
    }}
  ]
}}"""

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )
    except Exception as e:
        return None, f"API request failed: {e}"

    raw_text = response.text.strip()


    if raw_text.startswith("'''"):
        raw_text = raw_text.split("'''")[1]
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]
        raw_text = raw_text.strip()

    try:
        data = json.loads(raw_text)
        return data["questions"], None
    except (json.JSONDecodeError, KeyError) as e:
        return None, f"Couldn't parse quiz - try again. ({e})"
    
print("KEY LOADED:", os.environ.get("ANTHROPIC_API_KEY")[:15] if os.environ.get("ANTHROPIC_API_KEY") else "NOT FOUND")