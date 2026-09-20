from agent.practice_project_generator import generate_practice_and_projects


profile = {
    "target_role": "Product Manager",
    "current_skills": [
        "Product fundamentals",
        "User research basics",
        "Problem solving"
    ],
    "experience_level": "Beginner"
}


skill_gaps = {
    "target_role": "Product Manager",
    "skill_gaps": [
        {
            "skill": "Product prioritization",
            "current_level": "Beginner",
            "required_level": "Intermediate",
            "priority": "High",
            "gap": "Needs more practice applying prioritization frameworks",
            "reason": "Important for making product decisions"
        },
        {
            "skill": "Product metrics",
            "current_level": "Beginner",
            "required_level": "Intermediate",
            "priority": "High",
            "gap": "Needs practical experience defining and using product metrics",
            "reason": "PMs use metrics to evaluate product performance"
        }
    ]
}


learning_objectives = {
    "target_role": "Product Manager",
    "objectives": [
        {
            "skill": "Product prioritization",
            "priority": "High",
            "current_level": "Beginner",
            "required_level": "Intermediate",
            "learning_objectives": [
                {
                    "objective": "Apply a prioritization framework to product features",
                    "description": "Practice comparing features using a structured framework",
                    "success_criteria": [
                        "Can explain why one feature should be prioritized",
                        "Can compare multiple features consistently"
                    ]
                }
            ]
        },
        {
            "skill": "Product metrics",
            "priority": "High",
            "current_level": "Beginner",
            "required_level": "Intermediate",
            "learning_objectives": [
                {
                    "objective": "Define useful product metrics",
                    "description": "Practice selecting metrics for a product goal",
                    "success_criteria": [
                        "Can identify relevant metrics",
                        "Can explain what each metric measures"
                    ]
                }
            ]
        }
    ]
}


result = generate_practice_and_projects(
    profile,
    skill_gaps,
    learning_objectives
)


print("\n===== PRACTICE TASKS =====")

for task in result.get("practice_tasks", []):
    print("\nSkill:", task.get("skill"))
    print("Objective:", task.get("objective"))
    print("Difficulty:", task.get("difficulty"))
    print("Task:", task.get("task"))
    print("Instructions:", task.get("instructions"))
    print("Estimated Minutes:", task.get("estimated_minutes"))
    print("Expected Output:", task.get("expected_output"))
    print("Evaluation Criteria:", task.get("evaluation_criteria"))


print("\n===== PROJECT IDEAS =====")

for project in result.get("project_ideas", []):
    print("\nTitle:", project.get("title"))
    print("Skill:", project.get("skill"))
    print("Difficulty:", project.get("difficulty"))
    print("Problem Statement:", project.get("problem_statement"))
    print("Requirements:", project.get("requirements"))
    print("Deliverables:", project.get("deliverables"))
    print("Estimated Hours:", project.get("estimated_hours"))
    print("Why Relevant:", project.get("why_relevant"))