from edupath_pipeline import run_edupath


profile = {
    "target_role": "Product Manager",

    "career_goal": (
        "Become a Product Manager "
        "with strong product thinking and "
        "user-focused decision making."
    ),

    "skills": [
        "Python",
        "SQL",
        "Product Management"
    ],

    "experience": [],

    "education": (
        "B.Tech in Artificial Intelligence "
        "and Machine Learning"
    )
}


document_text = """
B.Tech student in Artificial Intelligence
and Machine Learning.

Skills:
Python
SQL
Product Management

Projects:
AI-based student productivity application.

Certifications:
Product Management fundamentals.
"""


result = run_edupath(
    profile,
    document_text,
    "text"
)


print("\n======================================")
print("        EDUPATH PIPELINE")
print("======================================")


print("\n--- DOCUMENT ANALYSIS ---")
print(result["document_analysis"])


print("\n--- SKILL GAPS ---")
print(result["skill_gaps"])


print("\n--- LEARNING OBJECTIVES ---")
print(result["learning_objectives"])


print("\n--- RESOURCES ---")
print(result["recommended_resources"])


print("\n--- WEEKLY PLAN ---")
print(result["weekly_plan"])


print("\n--- PRACTICE & PROJECTS ---")
print(result["practice_projects"])


print("\n--- PROGRESS ---")
print(result["progress"])


print("\n--- STRUGGLES ---")
print(result["struggles"])


print("\n--- ADAPTIVE PLAN ---")
print(result["adaptive_plan"])


print("\n--- PROGRESS REPORT ---")
print(result["progress_report"])


print("\n======================================")
print("       EDUPATH PIPELINE COMPLETE")
print("======================================")