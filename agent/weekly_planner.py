import os
import json
import time

from google import genai
from dotenv import load_dotenv


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. Add it to your .env file."
    )


# --------------------------------------------------
# Gemini client
# --------------------------------------------------

client = genai.Client(api_key=API_KEY)


# --------------------------------------------------
# Weekly Plan Generator
# --------------------------------------------------

def generate_weekly_plan(
    profile,
    learning_objectives,
    recommended_resources
):
    """
    Generate a personalized 7-day learning plan
    based on the learner's profile, learning objectives,
    and recommended resources.
    """

    prompt = f"""
You are the Personalized Weekly Planner component
of EduPath, an adaptive learning agent.

Your job is to create a realistic personalized
learning plan for the learner's next 7 days.

The plan must be based on:

1. The learner's target role
2. The learner's current experience
3. The learner's available hours per week
4. The learner's learning objectives
5. The recommended learning resources
6. The learner's existing skill gaps

--------------------------------------------------
LEARNER PROFILE
--------------------------------------------------

{json.dumps(profile, indent=2)}

--------------------------------------------------
LEARNING OBJECTIVES
--------------------------------------------------

{json.dumps(learning_objectives, indent=2)}

--------------------------------------------------
RECOMMENDED RESOURCES
--------------------------------------------------

{json.dumps(recommended_resources, indent=2)}

--------------------------------------------------
OUTPUT FORMAT
--------------------------------------------------

Return ONLY valid JSON.

Use exactly this structure:

{{
    "target_role": "",
    "total_hours": 0,
    "weekly_plan": [
        {{
            "day": "",
            "tasks": [
                {{
                    "skill": "",
                    "objective": "",
                    "activity": "",
                    "resource": "",
                    "estimated_minutes": 0,
                    "task_type": ""
                }}
            ]
        }}
    ]
}}

--------------------------------------------------
RULES
--------------------------------------------------

1. Create a plan covering all 7 days.

2. Respect the learner's available hours per week.

3. Do not exceed the learner's available weekly time.

4. Prioritize high-priority skill gaps.

5. Every activity must connect to a learning objective.

6. Use recommended resources where appropriate.

7. Include different activity types where useful:

   - Learning
   - Practice
   - Review
   - Project
   - Assessment

8. Do not create unrealistic workloads.

9. Every task must have an estimated time in minutes.

10. The total estimated time should approximately
    match the learner's available weekly hours.

11. Include lighter days when appropriate.

12. Do not assume that the learner already has skills
    that are not supported by the profile or analysis.

13. Make activities practical and suitable for the
    learner's current level.

14. Use "None" for the resource if no specific resource
    is needed.

15. Keep the plan clear and actionable.

16. Return ONLY valid JSON.
"""


    # --------------------------------------------------
    # Retry configuration
    # --------------------------------------------------

    max_retries = 4

    for attempt in range(max_retries):

        try:

            print(
                f"Generating weekly plan... "
                f"(attempt {attempt + 1}/{max_retries})"
            )

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
                config={
                    "response_mime_type": "application/json"
                }
            )

            # ------------------------------------------
            # Check response
            # ------------------------------------------

            if not response.text:
                raise ValueError(
                    "Gemini returned an empty response."
                )

            result = json.loads(response.text)

            return result

        except Exception as e:

            error_message = str(e)

            # ------------------------------------------
            # Retry temporary Gemini server errors
            # ------------------------------------------

            if (
                "503" in error_message
                or "UNAVAILABLE" in error_message
            ):

                if attempt < max_retries - 1:

                    wait_time = 5 * (2 ** attempt)

                    print(
                        f"Gemini server temporarily unavailable."
                    )

                    print(
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                else:

                    print(
                        "Gemini remained unavailable after "
                        f"{max_retries} attempts."
                    )

                    raise

            # ------------------------------------------
            # Do not retry other errors
            # ------------------------------------------

            else:
                print("Weekly plan generation failed.")
                print(error_message)
                raise


# --------------------------------------------------
# End of file
# --------------------------------------------------