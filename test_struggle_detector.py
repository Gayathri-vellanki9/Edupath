from agent.struggle_detector import (
    detect_struggles
)


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
        "title": "RICE Practice 1",
        "status": "Completed",
        "score": 45
    },

    {
        "activity_type": "Practice",
        "skill": "Product prioritization",
        "title": "RICE Practice 2",
        "status": "Completed",
        "score": 50
    },

    {
        "activity_type": "Practice",
        "skill": "Product prioritization",
        "title": "RICE Practice 3",
        "status": "Completed",
        "score": 55
    },

    {
        "activity_type": "Practice",
        "skill": "Product metrics",
        "title": "Metrics Practice",
        "status": "Completed",
        "score": 85
    }
]


result = detect_struggles(
    learning_objectives,
    activities
)


print("\n===== STRUGGLE DETECTION =====")

print(
    "\nTotal struggling skills:",
    result["total_struggling_skills"]
)


for struggle in result["struggling_skills"]:

    print(
        "\nSkill:",
        struggle["skill"]
    )

    print(
        "Average Score:",
        struggle["average_score"]
    )

    print(
        "Attempts:",
        struggle["attempts"]
    )

    print(
        "Severity:",
        struggle["severity"]
    )

    print(
        "Reasons:",
        struggle["reasons"]
    )