from agent.progress_evaluator import (
    evaluate_progress
)


profile = {
    "target_role": "Product Manager"
}


learning_objectives = {
    "target_role": "Product Manager",
    "objectives": [
        {
            "skill": "Product prioritization",
            "learning_objectives": [
                {
                    "objective":
                        "Apply a prioritization framework"
                }
            ]
        },
        {
            "skill": "Product metrics",
            "learning_objectives": [
                {
                    "objective":
                        "Define useful product metrics"
                }
            ]
        }
    ]
}


activities = [
    {
        "activity_type": "Practice",
        "skill": "Product prioritization",
        "title":
            "Prioritize features using RICE",
        "status": "Completed",
        "estimated_minutes": 60,
        "actual_minutes": 50,
        "score": 85
    }
]


result = evaluate_progress(
    profile,
    learning_objectives,
    activities
)


print("\n===== PROGRESS REPORT =====")

print(
    "\nTarget Role:",
    result["target_role"]
)

print(
    "Overall Progress:",
    result[
        "overall_progress_percentage"
    ],
    "%"
)

print(
    "\nSkills Acquired:",
    result["skills_acquired"]
)

print(
    "Skills In Progress:",
    result["skills_in_progress"]
)

print(
    "Remaining Gaps:",
    result["remaining_gaps"]
)

print(
    "\nSkill Progress:"
)

for skill in result["skill_progress"]:
    print(skill)

print(
    "\nCompleted Activities:",
    result["completed_activities"]
)