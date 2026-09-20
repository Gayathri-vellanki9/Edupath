from agent.activity_tracker import (
    record_activity,
    get_completed_activities
)


print("Recording learning activity...")


activity = record_activity(
    activity_type="Practice",
    skill="Product prioritization",
    title="Prioritize features using RICE",
    status="Completed",
    estimated_minutes=60,
    actual_minutes=50,
    score=85
)


print("\nRecorded Activity:")
print(activity)


print("\nCompleted Activities:")

completed = get_completed_activities()

for item in completed:
    print(item)