import json
import os


ACTIVITY_FILE = "activity_log.json"


def load_activities():
    """Load previously recorded learning activities."""

    if not os.path.exists(ACTIVITY_FILE):
        return []

    try:
        with open(ACTIVITY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return []


def record_activity(
    activity_type,
    skill,
    title,
    status="Completed",
    estimated_minutes=0,
    actual_minutes=0,
    score=None
):
    """
    Record one learning activity.
    """

    activities = load_activities()

    activity = {
        "activity_type": activity_type,
        "skill": skill,
        "title": title,
        "status": status,
        "estimated_minutes": estimated_minutes,
        "actual_minutes": actual_minutes,
        "score": score
    }

    activities.append(activity)

    with open(
        ACTIVITY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            activities,
            file,
            indent=2
        )

    return activity


def get_completed_activities():
    """Return all completed learning activities."""

    activities = load_activities()

    return [
        activity
        for activity in activities
        if activity.get("status") == "Completed"
    ]