import json
import os
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
# DOCUMENT ANALYZER
# =========================================================

def analyze_document(document_text, document_type):

    prompt = f"""
You are EduPath, an AI career learning agent.

Your job is to analyze the uploaded document and extract
ONLY information that is actually present in that document.

The document may belong to ANY career field.

It could be:

- Software Developer
- Data Analyst
- Data Scientist
- AI/ML Engineer
- Product Manager
- UI/UX Designer
- Cybersecurity
- Cloud/DevOps
- Business Analyst
- Student
- or another career

IMPORTANT:
Do NOT assume the document belongs to Product Management.

Do NOT add Product Management skills just because
EduPath is a career/product-management application.

The uploaded document is the ONLY source of truth.

=========================================================
DOCUMENT TYPE
=========================================================

{document_type}

=========================================================
UPLOADED DOCUMENT
=========================================================

{document_text}

=========================================================
EXTRACTION RULES
=========================================================

1. Extract skills that are explicitly mentioned or strongly
   supported by the document.

2. Extract programming languages exactly when present.

3. Extract frameworks and libraries when present.

4. Extract databases and technical technologies when present.

5. Extract tools and software separately when possible.

6. Extract skills demonstrated through projects or experience
   when the evidence clearly supports them.

7. Extract projects based only on projects actually described
   in the document.

8. Extract work/internship/experience based only on information
   actually present in the document.

9. Extract certifications only when actually mentioned.

10. Do NOT invent skills.

11. Do NOT add generic Product Management skills.

12. Do NOT add:
    Product Strategy
    User Research
    Product Analytics
    Product Roadmapping
    PRD
    Agile
    Product Discovery

    unless the uploaded document actually contains evidence
    for those skills.

13. Do NOT convert every resume into a Product Manager resume.

14. Preserve the actual career domain of the learner.

15. If the resume says Python, return Python.

16. If the resume says Java, return Java.

17. If the resume says React, return React.

18. If the resume says SQL, return SQL.

19. If the resume says Power BI, return Power BI.

20. If the resume says Figma, return Figma.

21. Do not replace actual technical skills with generic
    career skills.

=========================================================
SKILL EXTRACTION
=========================================================

The "skills" array should contain the learner's actual
skills found in the document.

Examples:

Developer resume:

[
    "Python",
    "Java",
    "JavaScript",
    "React",
    "SQL",
    "Git"
]

Data Analyst resume:

[
    "SQL",
    "Python",
    "Excel",
    "Power BI",
    "Data Analysis",
    "Data Visualization"
]

Product Manager resume:

[
    "Product Strategy",
    "User Research",
    "Product Analytics",
    "Roadmapping"
]

Only return skills supported by the actual document.

=========================================================
TOOLS
=========================================================

The "tools" array should contain tools/software/platforms
actually mentioned.

Examples:

[
    "GitHub",
    "VS Code",
    "Figma",
    "Power BI",
    "Jira"
]

Do not move every tool into skills unless the document
clearly presents it as a skill.

=========================================================
PROJECTS
=========================================================

Extract actual projects from the document.

For each project, preserve the important information
without inventing details.

=========================================================
EXPERIENCE
=========================================================

Extract actual internships, jobs, roles, or relevant
experience described in the document.

=========================================================
CERTIFICATIONS
=========================================================

Extract certifications explicitly mentioned.

=========================================================
EVIDENCE
=========================================================

Provide short evidence statements showing where the
skills came from.

Examples:

"Built a web application using React"

"Used Python for data analysis"

"Created dashboards using Power BI"

"Developed APIs using Node.js"

Never create fake evidence.

=========================================================
SUMMARY
=========================================================

Create a short factual summary of the learner based ONLY
on the uploaded document.

Do not assign a career role unless the document itself
supports it.

=========================================================
OUTPUT
=========================================================

Return ONLY valid JSON.

Do not use markdown.

Use exactly this structure:

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


    # =====================================================
    # GEMINI REQUEST
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
            # Remove markdown fences if Gemini adds them
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


            if not isinstance(result, dict):

                raise ValueError(
                    "Document analyzer returned invalid JSON."
                )


            # -------------------------------------------------
            # Ensure required fields exist
            # -------------------------------------------------

            required_fields = [

                "skills",
                "tools",
                "projects",
                "experience",
                "certifications",
                "evidence",
                "summary"

            ]


            for field in required_fields:

                if field not in result:

                    result[field] = [] if field != "summary" else ""


            # -------------------------------------------------
            # Safety: ensure arrays are actually arrays
            # -------------------------------------------------

            for field in [

                "skills",
                "tools",
                "projects",
                "experience",
                "certifications",
                "evidence"

            ]:

                if not isinstance(
                    result[field],
                    list
                ):

                    result[field] = []


            if not isinstance(
                result["summary"],
                str
            ):

                result["summary"] = str(
                    result["summary"]
                )


            # -------------------------------------------------
            # Remove duplicates while preserving order
            # -------------------------------------------------

            for field in [

                "skills",
                "tools",
                "projects",
                "experience",
                "certifications",
                "evidence"

            ]:

                cleaned = []

                seen = set()

                for item in result[field]:

                    if not isinstance(item, str):

                        item = str(item)

                    item = item.strip()

                    if not item:

                        continue

                    key = item.lower()

                    if key not in seen:

                        seen.add(key)

                        cleaned.append(item)


                result[field] = cleaned


            # -------------------------------------------------
            # Return final analysis
            # -------------------------------------------------

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