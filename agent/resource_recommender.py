import json
import os
import time

from google import genai
from dotenv import load_dotenv


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def recommend_resources(
    profile,
    learning_objectives
):

    prompt = f"""
You are EduPath, an adaptive learning
and career development agent.

Recommend learning resources for this learner.

LEARNER PROFILE:
{json.dumps(profile, indent=2)}

LEARNING OBJECTIVES:
{json.dumps(learning_objectives, indent=2)}

REQUIREMENTS:

1. Recommend resources based directly
   on the learner's learning objectives.

2. Match resources to the learner's
   current level.

3. Prefer practical and trustworthy
   learning resources.

4. Include different resource types
   when useful, such as:
   - Course
   - Tutorial
   - Documentation
   - Video
   - Article
   - Practice

5. Do not recommend resources unrelated
   to the learner's skill gaps.

6. Do not invent resource URLs.

7. If you are not confident about an
   exact URL, use an empty string.

8. Each resource must contain:
   - title
   - type
   - level
   - description
   - why_relevant
   - estimated_time
   - url

9. Return ONLY valid JSON.

10. Do not use markdown.

Return exactly:

{{
    "target_role": "...",
    "resources": [
        {{
            "skill": "...",
            "objective": "...",
            "resources": [
                {{
                    "title": "...",
                    "type": "...",
                    "level": "...",
                    "description": "...",
                    "why_relevant": "...",
                    "estimated_time": "...",
                    "url": ""
                }}
            ]
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
                f"Resource recommender attempt "
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
                    "Resource recommendation failed "
                    "after all retries."
                )

                return {
                    "target_role": profile.get(
                        "target_role",
                        ""
                    ),
                    "resources": [],
                    "error": str(e)
                }