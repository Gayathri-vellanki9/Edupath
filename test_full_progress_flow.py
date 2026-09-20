from agent.activity_tracker import load_activities
from agent.progress_evaluator import evaluate_progress
from agent.struggle_detector import detect_struggles
from agent.adaptive_planner import create_adaptive_plan
from agent.progress_report_generator import generate_progress_report


# ---------------------------------------
# 1. Learner profile
# ---------------------------------------

profile = {
    "target_role": "Product Manager",

    "skills": [
        "Product Management",
        "Python",
        "SQL"
    ]
}


# ---------------------------------------
# 2. Learning objectives
# ---------------------------------------

learning_objectives = {
    "target_role": "Product Manager",

    "objectives": [
        {
            "skill": "Product Prioritization",
            "priority": "High",
            "current_level": "Beginner",
            "required_level": "Intermediate",

            "learning_objectives": [
                {
                    "objective": "Understand RICE prioritization",
                    "description": (
                        "Learn how to use RICE "
                        "to prioritize product features."
                    ),
                    "success_criteria": [
                        "Can calculate RICE score",
                        "Can explain prioritization decision"
                    ]
                }
            ]
        },

        {
            "skill": "Product Metrics",
            "priority": "Medium",
            "current_level": "Beginner",
            "required_level": "Intermediate",

            "learning_objectives": [
                {
                    "objective": "Understand product KPIs",
                    "description": (
                        "Learn how product metrics "
                        "are used to measure success."
                    ),
                    "success_criteria": [
                        "Can identify relevant KPIs",
                        "Can explain metric meaning"
                    ]
                }
            ]
        }
    ]
}


# ---------------------------------------
# 3. Load learner activities
# ---------------------------------------

activities = load_activities()


# ---------------------------------------
# 4. Evaluate progress
# ---------------------------------------

progress = evaluate_progress(
    profile,
    learning_objectives,
    activities
)


# ---------------------------------------
# 5. Detect struggles
# ---------------------------------------

struggles = detect_struggles(
    learning_objectives,
    activities
)


# ---------------------------------------
# 6. Example weekly plan
# ---------------------------------------

weekly_plan = {
    "target_role": "Product Manager",

    "total_hours": 3,

    "weekly_plan": [
        {
            "day": "Day 1",

            "tasks": [
                {
                    "skill": "Product Prioritization",
                    "objective": (
                        "Understand RICE prioritization"
                    ),
                    "activity": (
                        "Practice calculating RICE scores"
                    ),
                    "resource": "RICE practice",
                    "estimated_minutes": 60,
                    "task_type": "Practice"
                },

                {
                    "skill": "Product Metrics",
                    "objective": (
                        "Understand product KPIs"
                    ),
                    "activity": (
                        "Learn important product metrics"
                    ),
                    "resource": "Product metrics lesson",
                    "estimated_minutes": 60,
                    "task_type": "Learning"
                }
            ]
        }
    ]
}


# ---------------------------------------
# 7. Create adaptive plan
# ---------------------------------------

adaptive_result = create_adaptive_plan(
    weekly_plan["weekly_plan"],
    progress,
    struggles
)


# ---------------------------------------
# 8. Generate progress report
# ---------------------------------------

report = generate_progress_report(
    profile,
    progress,
    struggles
)


# ---------------------------------------
# 9. Display results
# ---------------------------------------

print("\n================================")
print("EDUPATH FULL PROGRESS FLOW")
print("================================")


print("\n--- PROGRESS ---")
print(progress)


print("\n--- STRUGGLES ---")
print(struggles)


print("\n--- ADAPTIVE PLAN ---")
print(adaptive_result)


print("\n--- PROGRESS REPORT ---")
print(report)


print("\n================================")
print("FLOW COMPLETED")
print("================================")