import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing.")

client = genai.Client(api_key=API_KEY)


def generate_learning_objectives(skill_gap_analysis):

    prompt = f"""
You are the Learning Objective Generator component
of EduPath, an adaptive learning agent.

Your job is to convert identified skill gaps into
clear, structured and actionable learning objectives.

SKILL GAP ANALYSIS:

{json.dumps(skill_gap_analysis, indent=2)}

For every important skill gap, create learning objectives
that help the learner move from their current level toward
the required level.

Return ONLY valid JSON using this structure:

{{
    "target_role": "",
    "objectives": [
        {{
            "skill": "",
            "priority": "",
            "current_level": "",
            "required_level": "",
            "learning_objectives": [
                {{
                    "objective": "",
                    "description": "",
                    "success_criteria": []
                }}
            ]
        }}
    ]
}}

Rules:

1. Create objectives only for the identified skill gaps.
2. Objectives must be specific and actionable.
3. Do not create vague objectives such as
   "Learn Product Management."
4. Objectives should match the learner's current level.
5. Objectives should help close the identified gap.
6. Each objective should have measurable success criteria.
7. Preserve the priority from the skill gap analysis.
8. Do not invent evidence about the learner.
9. Keep the number of objectives reasonable.
10. Return ONLY valid JSON.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    return json.loads(response.text)