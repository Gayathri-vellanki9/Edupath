from agent.resource_recommender import recommend_resources


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


result = recommend_resources(
    profile,
    learning_objectives
)

print(result)