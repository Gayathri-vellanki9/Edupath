import json
import os
import time

from google import genai
from dotenv import load_dotenv


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_document(
    document_text,
    document_type
):

    prompt = f"""
You are EduPath, an AI career learning agent.

Analyze the learner's document and extract
only information that is actually supported
by the document.

DOCUMENT TYPE:
{document_type}

DOCUMENT:
{document_text}

Extract:

1. skills
2. tools
3. projects
4. experience
5. certifications
6. evidence
7. summary

IMPORTANT RULES:

- Do not invent skills.
- Do not assume experience.
- Only include information supported
  by the document.
- Keep evidence connected to the
  information extracted.
- Return ONLY valid JSON.
- Do not use markdown.

Return exactly this structure:

{{
    "skills": [],
    "tools": [],
    "projects": [],
    "experience": [],
    "certifications": [],
    "evidence": [],
    "summary": ""
}}
"""

    max_retries = 3

    for attempt in range(max_retries):

        try:

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            text = response.text.strip()

            # Remove markdown JSON fences
            if text.startswith("```json"):
                text = text[7:]

            if text.startswith("```"):
                text = text[3:]

            if text.endswith("```"):
                text = text[:-3]

            text = text.strip()

            result = json.loads(text)

            return result

        except Exception as e:

            print(
                f"Document analyzer attempt "
                f"{attempt + 1} failed: {e}"
            )

            if attempt < max_retries - 1:

                wait_time = 2 ** attempt

                print(
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

            else:

                print(
                    "Document analysis failed "
                    "after all retries."
                )

                return {
                    "skills": [],
                    "tools": [],
                    "projects": [],
                    "experience": [],
                    "certifications": [],
                    "evidence": [],
                    "summary": "",
                    "error": str(e)
                }