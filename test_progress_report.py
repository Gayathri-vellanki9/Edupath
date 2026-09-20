from agent.progress_report_generator import (
    generate_progress_report
)


profile = {
    "target_role": "Product Manager"
}


progress = {
    "target_role": "Product Manager",

    "overall_progress_percentage": 50,

    "skills_acquired": [
        "Product Metrics"
    ],

    "skills_in_progress": [
        "Product Prioritization"
    ],

    "remaining_gaps": [
        "User Research"
    ],

    "completed_activities": 3
}


struggles = {
    "struggling_skills": [
        {
            "skill": "Product Prioritization",
            "average_score": 50,
            "attempts": 3,
            "reasons": [
                "Low performance on practice activities"
            ],
            "severity": "High"
        }
    ],

    "total_struggling_skills": 1
}


report = generate_progress_report(
    profile,
    progress,
    struggles
)


print("\n===== PROGRESS REPORT =====")
print(report)