import os
import json
import time

from google import genai
from dotenv import load_dotenv


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing.")

client = genai.Client(
    api_key=API_KEY
)


# =========================================================
# SKILL GAP ANALYZER
# =========================================================

def analyze_skill_gaps(profile, document_analysis):

    # -----------------------------------------------------
    # Get explicitly provided target role
    # -----------------------------------------------------

    provided_role = (
        profile.get("target_role", "")
        if isinstance(profile, dict)
        else ""
    )

    provided_role = (
        provided_role.strip()
        if isinstance(provided_role, str)
        else ""
    )


    # -----------------------------------------------------
    # Determine whether role must be inferred
    # -----------------------------------------------------

    if provided_role:

        role_instruction = f"""
The learner has explicitly selected this target role:

{provided_role}

IMPORTANT:
Use this target role.
Do NOT replace it with another role.
"""

    else:

        role_instruction = """
The learner has NOT explicitly provided a target role.

You MUST infer the most likely target role from the
resume evidence.

Use ONLY evidence from:
- skills
- tools
- projects
- experience
- certifications
- summary

Do NOT assume Product Manager.

For example:

If the resume contains evidence such as:
Python, Java, C++, JavaScript, React, Node.js,
APIs, Git, software development projects,
data structures, algorithms, backend development
→ a Software Developer / Software Engineer role
may be appropriate.

If the resume contains:
SQL, Excel, Power BI, Tableau, Python,
data visualization, dashboards, analytics
→ a Data Analyst role may be appropriate.

If the resume contains:
machine learning, deep learning, TensorFlow,
PyTorch, NLP, computer vision, model development
→ an ML/AI Engineer role may be appropriate.

If the resume contains:
product strategy, user research, product discovery,
roadmaps, PRDs, product analytics
→ a Product Manager role may be appropriate.

If the resume contains:
Figma, wireframes, prototypes, usability testing,
user experience, interaction design
→ a UI/UX Designer role may be appropriate.

Choose the role that is best supported by the
actual resume evidence.

Never default to Product Manager simply because
EduPath is a product-management project.
"""


    # -----------------------------------------------------
    # Build prompt
    # -----------------------------------------------------

    prompt = f"""
You are the Skill Gap Analysis component of EduPath,
an adaptive career learning agent.

Your task is to analyze a learner's resume and identify
the meaningful skills they need to develop for their
most relevant target career role.

=========================================================
ROLE DETERMINATION
=========================================================

{role_instruction}

=========================================================
LEARNER PROFILE
=========================================================

{json.dumps(profile, indent=2)}

=========================================================
DOCUMENT ANALYSIS
=========================================================

{json.dumps(document_analysis, indent=2)}

=========================================================
IMPORTANT RESUME-GROUNDING RULES
=========================================================

1. The uploaded resume is the primary source of truth.

2. Do NOT assume the learner is a Product Manager.

3. Do NOT use generic Product Management skills unless
   the resume/target role actually indicates Product
   Management.

4. Do NOT invent skills that are not supported by the
   resume.

5. Existing skills must come from the document analysis.

6. Projects and experience can be used as evidence
   when determining current skill level.

7. If the resume contains software-development evidence,
   generate software-development-related skill gaps.

8. If the resume contains data-analysis evidence,
   generate data-analysis-related skill gaps.

9. If the resume contains AI/ML evidence, generate
   AI/ML-related skill gaps.

10. If the resume contains UX/design evidence, generate
    UX/design-related skill gaps.

11. Skill gaps must be relevant to the inferred or
    explicitly selected target role.

12. Do not create gaps simply to make the list longer.

=========================================================
CURRENT LEVEL
=========================================================

Use only:

"Beginner"
"Intermediate"
"Advanced"
"Unknown"

Estimate the current level using evidence from the
resume.

For example:

If Python appears in multiple projects and experience,
the learner may be Intermediate rather than Beginner.

If a skill is not supported by the resume, use
"Unknown" rather than pretending the learner has it.

=========================================================
REQUIRED LEVEL
=========================================================

Use only:

"Beginner"
"Intermediate"
"Advanced"

Choose a realistic level for the target role.

=========================================================
GAP
=========================================================

The "gap" field should describe what the learner needs
to improve.

Example:

"Needs stronger backend API development"

NOT:

"18%"

=========================================================
PRIORITY
=========================================================

Use only:

"High"
"Medium"
"Low"

=========================================================
EVIDENCE
=========================================================

Evidence must come from the resume.

Examples:

"Built a React web application"
"Used Python for data analysis"
"Worked with SQL databases"

Do NOT create fake evidence.

=========================================================
NUMBER OF GAPS
=========================================================

Return approximately 3 to 6 meaningful skill gaps.

Do not list every possible skill required by the role.

Focus on the most important development areas.

=========================================================
OUTPUT
=========================================================

Return ONLY valid JSON.

Use exactly this structure:

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
"""


    # =====================================================
    # GEMINI REQUEST WITH RETRIES
    # =====================================================

    max_retries = 3

    for attempt in range(max_retries):

        try:

            response = client.models.generate_content(

                model="gemini-3.6-flash",

                contents=prompt,

                config={
                    "response_mime_type": "application/json"
                }

            )


            text = response.text.strip()


            # -------------------------------------------------
            # Remove accidental markdown fences
            # -------------------------------------------------

            if text.startswith("```json"):

                text = text[7:]


            elif text.startswith("```"):

                text = text[3:]


            if text.endswith("```"):

                text = text[:-3]


            text = text.strip()


            # -------------------------------------------------
            # Parse JSON
            # -------------------------------------------------

            result = json.loads(text)


            # -------------------------------------------------
            # Safety validation
            # -------------------------------------------------

            if not isinstance(result, dict):

                raise ValueError(
                    "Skill gap analyzer returned invalid JSON."
                )


            if "target_role" not in result:

                result["target_role"] = (
                    provided_role
                    if provided_role
                    else "Unknown"
                )


            if "skill_gaps" not in result:

                result["skill_gaps"] = []


            if not isinstance(
                result["skill_gaps"],
                list
            ):

                result["skill_gaps"] = []


            return result


        except Exception as e:

            print(
                f"Skill gap analyzer attempt "
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
                    "Skill gap analysis failed "
                    "after all retries."
                )


                return {

                    "target_role": (
                        provided_role
                        if provided_role
                        else "Unknown"
                    ),

                    "skill_gaps": [],

                    "error": str(e)

                }