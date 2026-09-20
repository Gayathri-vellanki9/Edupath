from agent.adaptive_planner import (
    create_adaptive_plan
)


weekly_plan = {
    "target_role": "Product Manager",
    "total_hours": 3,
    "weekly_plan": [
        {
            "day": "Day 1",
            "tasks": [
                {
                    "skill": "Product prioritization",
                    "objective":
                        "Apply a prioritization framework",
                    "activity":
                        "Practice RICE prioritization",
                    "resource":
                        "PM prioritization lesson",
                    "estimated_minutes": 60,
                    "task_type": "Practice"
                },
                {
                    "skill": "Product metrics",
                    "objective":
                        "Define product metrics",
                    "activity":
                        "Study product metrics",
                    "resource":
                        "Product metrics lesson",
                    "estimated_minutes": 60,
                    "task_type": "Learning"
                }
            ]
        }
    ]
}


progress = {
    "skills_acquired": [
        "Product metrics"
    ],
    "skills_in_progress": [
        "Product prioritization"
    ],
    "remaining_gaps": []
}


struggles = {
    "struggling_skills": [
        {
            "skill": "Product prioritization",
            "average_score": 50,
            "attempts": 3,
            "severity": "High",
            "reasons": [
                "Low performance on practice activities"
            ]
        }
    ]
}


result = create_adaptive_plan(
    weekly_plan["weekly_plan"],
    progress,
    struggles
)


print("\n===== ADAPTIVE PLAN =====")


for day in result["adaptive_plan"]:

    print("\n", day["day"])

    for task in day["tasks"]:

        print(
            "\nSkill:",
            task["skill"]
        )

        print(
            "Activity:",
            task["activity"]
        )

        print(
            "Estimated Minutes:",
            task["estimated_minutes"]
        )

        print(
            "Reason:",
            task.get(
                "adaptive_reason",
                "No adaptation"
            )
        )


print(
    "\n===== ADAPTATIONS ====="
)

print(
    result["adaptations"]
)