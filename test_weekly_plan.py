from agent.weekly_planner import generate_weekly_plan


profile = {
    "career_goal": "Get a Product Management internship",
    "target_role": "Product Manager",
    "current_skills": "Python, SQL, communication",
    "experience": "Student",
    "hours_per_week": 10,
    "learning_preference": "Practical learning"
}


learning_objectives = {
    "target_role": "Product Manager",
    "objectives": [
        {
            "skill": "User Research",
            "priority": "High",
            "current_level": "Beginner",
            "required_level": "Intermediate",
            "learning_objectives": [
                {
                    "objective": "Learn how to conduct user interviews",
                    "description": "Understand how to prepare and conduct useful user interviews.",
                    "success_criteria": [
                        "Create an interview guide",
                        "Conduct 5 interviews",
                        "Identify recurring pain points"
                    ]
                }
            ]
        }
    ]
}


recommended_resources = {
    "target_role": "Product Manager",
    "resources": [
        {
            "skill": "User Research",
            "objective": "Learn how to conduct user interviews",
            "resources": [
                {
                    "title": "User Interview Tutorial",
                    "type": "Tutorial",
                    "level": "Beginner",
                    "description": "Learn the basics of conducting user interviews.",
                    "why_relevant": "Directly supports the interview learning objective.",
                    "estimated_time": "60 minutes",
                    "url": ""
                }
            ]
        }
    ]
}


result = generate_weekly_plan(
    profile,
    learning_objectives,
    recommended_resources
)

print(result)