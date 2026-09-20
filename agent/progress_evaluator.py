import json
import os


def evaluate_progress(
    profile,
    learning_objectives,
    activities
):
    """
    Evaluate learner progress based on
    learning objectives and completed activities.
    """

    target_role = profile.get("target_role", "")

    objectives = learning_objectives.get(
        "objectives",
        []
    )

    completed_activities = [
        activity
        for activity in activities
        if activity.get("status") == "Completed"
    ]

    total_objectives = len(objectives)

    skill_progress = []

    for objective_group in objectives:

        skill = objective_group.get(
            "skill",
            ""
        )

        learning_objectives_list = (
            objective_group.get(
                "learning_objectives",
                []
            )
        )

        related_activities = [
            activity
            for activity in completed_activities
            if activity.get("skill", "").lower()
            == skill.lower()
        ]

        completed_count = len(
            related_activities
        )

        objective_count = len(
            learning_objectives_list
        )

        if objective_count == 0:

            progress_percentage = 0

        else:

            progress_percentage = min(
                100,
                round(
                    (
                        completed_count
                        / objective_count
                    )
                    * 100
                )
            )

        if progress_percentage >= 100:

            status = "Acquired"

        elif progress_percentage > 0:

            status = "In Progress"

        else:

            status = "Not Started"

        skill_progress.append(
            {
                "skill": skill,
                "status": status,
                "progress_percentage":
                    progress_percentage,
                "completed_activities":
                    completed_count,
                "total_objectives":
                    objective_count
            }
        )

    acquired_skills = [
        item["skill"]
        for item in skill_progress
        if item["status"] == "Acquired"
    ]

    skills_in_progress = [
        item["skill"]
        for item in skill_progress
        if item["status"] == "In Progress"
    ]

    remaining_gaps = [
        item["skill"]
        for item in skill_progress
        if item["status"] == "Not Started"
    ]

    if total_objectives == 0:

        overall_progress = 0

    else:

        overall_progress = round(
            sum(
                item["progress_percentage"]
                for item in skill_progress
            )
            / total_objectives
        )

    return {
        "target_role": target_role,
        "overall_progress_percentage":
            overall_progress,
        "skills_acquired":
            acquired_skills,
        "skills_in_progress":
            skills_in_progress,
        "remaining_gaps":
            remaining_gaps,
        "skill_progress":
            skill_progress,
        "completed_activities":
            len(completed_activities)
    }