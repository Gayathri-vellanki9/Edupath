def generate_progress_report(
    profile,
    progress,
    struggles
):
    target_role = profile.get(
        "target_role",
        ""
    )

    overall_progress = progress.get(
        "overall_progress_percentage",
        0
    )

    skills_acquired = progress.get(
        "skills_acquired",
        []
    )

    skills_in_progress = progress.get(
        "skills_in_progress",
        []
    )

    remaining_gaps = progress.get(
        "remaining_gaps",
        []
    )

    struggling_skills = struggles.get(
        "struggling_skills",
        []
    )

    # -----------------------------------
    # Generate recommended next steps
    # -----------------------------------

    next_steps = []

    # Step for struggling skills
    for struggle in struggling_skills:
        skill = struggle.get(
            "skill",
            ""
        )

        if skill:
            next_steps.append(
                "Practice " + skill +
                " with additional guided exercises."
            )

    # Step for remaining gaps
    for skill in remaining_gaps:
        if skill:
            next_steps.append(
                "Start learning " + skill +
                " because it is still a remaining skill gap."
            )

    # Step for skills in progress
    for skill in skills_in_progress:
        if skill:
            next_steps.append(
                "Continue practicing " + skill +
                " until the required level is reached."
            )

    # If there are no pending tasks
    if not next_steps:
        next_steps.append(
            "Continue practicing acquired skills "
            "and work on advanced projects."
        )

    # -----------------------------------
    # Generate summary
    # -----------------------------------

    if overall_progress >= 80:
        summary = (
            "The learner has made strong progress "
            "toward the target role."
        )

    elif overall_progress >= 50:
        summary = (
            "The learner has made moderate progress "
            "but still has important skills to develop."
        )

    elif overall_progress > 0:
        summary = (
            "The learner has started making progress "
            "but needs continued learning and practice."
        )

    else:
        summary = (
            "The learner has not yet made measurable "
            "progress and should begin the learning plan."
        )

    # -----------------------------------
    # Return progress report
    # -----------------------------------

    return {
        "target_role": target_role,

        "overall_progress_percentage": (
            overall_progress
        ),

        "summary": summary,

        "skills_acquired": skills_acquired,

        "skills_in_progress": skills_in_progress,

        "remaining_gaps": remaining_gaps,

        "struggling_skills": struggling_skills,

        "completed_activities": progress.get(
            "completed_activities",
            0
        ),

        "recommended_next_steps": next_steps
    }