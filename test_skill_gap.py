from agent.skill_gap_analyzer import analyze_skill_gaps


profile = {
    "career_goal": "Get a Product Management internship",
    "target_role": "Product Manager",
    "current_skills": "Python, SQL, communication",
    "experience": "Student",
    "hours_per_week": 10,
    "learning_preference": "Practical learning"
}


document_analysis = {
    "skills": ["Python", "SQL"],
    "tools": ["MySQL"],
    "projects": ["Student management project"],
    "experience": ["Student"],
    "certifications": [],
    "evidence": [
        "Built a student management project using Python and MySQL."
    ],
    "summary": "Learner has beginner Python and SQL experience."
}


result = analyze_skill_gaps(
    profile,
    document_analysis
)

print(result)