import json
import os
import time

from google import genai
from dotenv import load_dotenv


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_practice_and_projects(
    profile,
    skill_gaps,
    learning_objectives
):
    """
    Generate practice tasks and project ideas
    based on the learner's profile, skill gaps,
    and learning objectives.
    """

    prompt = f"""
You are EduPath, an adaptive learning and career development agent.

Create practice tasks and project ideas for this learner.

LEARNER PROFILE:
{json.dumps(profile, indent=2)}

SKILL GAPS:
{json.dumps(skill_gaps, indent=2)}

LEARNING OBJECTIVES:
{json.dumps(learning_objectives, indent=2)}

REQUIREMENTS:

1. Create practice tasks based directly on the learner's
   actual skill gaps and learning objectives.

2. Match difficulty to the learner's current level.

3. Do not assume unsupported skills.

4. Each practice task must contain:
   - skill
   - objective
   - difficulty
   - task
   - instructions
   - estimated_minutes
   - expected_output
   - evaluation_criteria

5. Tasks must be practical and realistic.

6. Create project ideas directly related to the
   learner's target role and skill gaps.

7. Avoid unnecessarily complex projects.

8. Each project must contain:
   - title
   - skill
   - difficulty
   - problem_statement
   - requirements
   - deliverables
   - estimated_hours
   - why_relevant

9. Projects should be appropriate for the learner's
   current level.

10. Return ONLY valid JSON.

11. Do not use markdown.

Return exactly:

{{
  "target_role": "...",
  "practice_tasks": [
    {{
      "skill": "...",
      "objective": "...",
      "difficulty": "...",
      "task": "...",
      "instructions": [],
      "estimated_minutes": 0,
      "expected_output": "...",
      "evaluation_criteria": []
    }}
  ],
  "project_ideas": [
    {{
      "title": "...",
      "skill": "...",
      "difficulty": "...",
      "problem_statement": "...",
      "requirements": [],
      "deliverables": [],
      "estimated_hours": 0,
      "why_relevant": "..."
    }}
  ]
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

            # Remove markdown code fences if Gemini adds them
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
                f"Attempt {attempt + 1} failed: {e}"
            )

            if attempt < max_retries - 1:

                wait_time = 2 ** attempt

                print(
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

            else:

                return {
                    "target_role": profile.get(
                        "target_role", ""
                    ),
                    "practice_tasks": [],
                    "project_ideas": [],
                    "error": str(e)
                }