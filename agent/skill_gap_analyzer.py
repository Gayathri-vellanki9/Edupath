import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing.")

client = genai.Client(api_key=API_KEY)


def analyze_skill_gaps(profile, document_analysis):

    prompt = f"""
You are the Skill Gap Analysis component of EduPath,
an adaptive learning agent.

Your job is to compare the learner's existing capabilities
with the skills normally required for their target role.

LEARNER PROFILE:
{json.dumps(profile, indent=2)}

DOCUMENT ANALYSIS:
{json.dumps(document_analysis, indent=2)}

Identify the important skills required for the learner's
target role and compare them with the learner's existing skills.

Return ONLY valid JSON using this structure:

{{
    "target_role": "",
    "skill_gaps": [
        {{
            "skill": "",
            "current_level": "",
            "required_level": "",
            "gap": "",
            "priority": "",
            "reason": "",
            "evidence": []
        }}
    ]
}}

Rules:

1. Only identify realistic skills for the target role.
2. Use evidence from the learner profile and document analysis.
3. Do not invent skills the learner has.
4. current_level can be:
   "Beginner", "Intermediate", "Advanced", or "Unknown".
5. required_level can be:
   "Beginner", "Intermediate", or "Advanced".
6. gap should explain what the learner needs to develop.
7. priority should be "High", "Medium", or "Low".
8. Include evidence supporting the current-level assessment.
9. Focus on meaningful skill gaps rather than listing every possible skill.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    return json.loads(response.text)