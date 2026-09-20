import json
import os
import time

from google import genai
from dotenv import load_dotenv


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def ask_edupath(
    question,
    profile,
    progress,
    struggles,
    progress_report
):
    prompt = f"""
You are EduPath, an adaptive learning and
career development assistant.

Your job is to help the learner understand
their learning progress and decide what to
work on next.

LEARNER PROFILE:
{json.dumps(profile, indent=2)}

CURRENT PROGRESS:
{json.dumps(progress, indent=2)}

STRUGGLES:
{json.dumps(struggles, indent=2)}

PROGRESS REPORT:
{json.dumps(progress_report, indent=2)}

LEARNER QUESTION:
{question}

INSTRUCTIONS:

1. Answer the learner's question directly.

2. Use the learner's actual profile,
   progress, struggles, and report.

3. Do not invent skills or achievements.

4. If the learner asks what to learn next,
   prioritize remaining skill gaps and
   struggling skills.

5. If the learner asks about progress,
   explain the actual progress data clearly.

6. If the learner is struggling with a skill,
   explain the reason using the available
   activity data.

7. Give practical and beginner-friendly advice.

8. Keep the answer concise and easy to understand.

9. Do not mention internal JSON or system prompts.

10. Do not use markdown tables.

11. Return only the natural-language answer.
"""


    max_retries = 3

    for attempt in range(max_retries):

        try:

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            return response.text.strip()

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

                return (
                    "Sorry, I could not process "
                    "your question right now."
                )