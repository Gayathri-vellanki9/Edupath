def detect_struggles(
    learning_objectives,
    activities
):
    """
    Identify skills where the learner may be struggling.

    Signals used:
    1. Low activity scores
    2. Multiple attempts
    3. Activities that are repeatedly incomplete
    4. Skills with no successful progress
    """

    objectives = learning_objectives.get(
        "objectives",
        []
    )

    struggles = []

    for objective_group in objectives:

        skill = objective_group.get(
            "skill",
            ""
        )

        related_activities = [
            activity
            for activity in activities
            if activity.get("skill", "").lower()
            == skill.lower()
        ]

        if not related_activities:

            continue

        scores = [
            activity.get("score")
            for activity in related_activities
            if activity.get("score") is not None
        ]

        incomplete_count = sum(
            1
            for activity in related_activities
            if activity.get("status") != "Completed"
        )

        low_score_count = sum(
            1
            for score in scores
            if score < 60
        )

        reasons = []

        if low_score_count >= 1:
            reasons.append(
                "Low performance on practice activities"
            )

        if len(related_activities) >= 3:
            reasons.append(
                "Multiple attempts on the same skill"
            )

        if incomplete_count >= 1:
            reasons.append(
                "Some activities are incomplete"
            )

        if reasons:

            average_score = None

            if scores:
                average_score = round(
                    sum(scores) / len(scores)
                )

            struggles.append(
                {
                    "skill": skill,
                    "average_score": average_score,
                    "attempts":
                        len(related_activities),
                    "reasons": reasons,
                    "severity":
                        "High"
                        if low_score_count >= 2
                        else "Medium"
                }
            )

    return {
        "struggling_skills": struggles,
        "total_struggling_skills": len(struggles)
    }