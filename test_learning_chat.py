from agent.learning_chat_assistant import ask_edupath


profile = {
    "target_role": "Product Manager",

    "skills": [
        "Product Management",
        "Python",
        "SQL"
    ]
}


progress = {
    "target_role": "Product Manager",

    "overall_progress_percentage": 50,

    "skills_acquired": [
        "Product Prioritization"
    ],

    "skills_in_progress": [],

    "remaining_gaps": [
        "Product Metrics"
    ],

    "completed_activities": 3
}


struggles = {
    "struggling_skills": [
        {
            "skill": "Product Prioritization",
            "average_score": 85,
            "attempts": 3,
            "reasons": [
                "Multiple attempts on the same skill"
            ],
            "severity": "Medium"
        }
    ],

    "total_struggling_skills": 1
}


progress_report = {
    "target_role": "Product Manager",

    "overall_progress_percentage": 50,

    "summary": (
        "The learner has made moderate progress "
        "but still has important skills to develop."
    ),

    "skills_acquired": [
        "Product Prioritization"
    ],

    "skills_in_progress": [],

    "remaining_gaps": [
        "Product Metrics"
    ],

    "recommended_next_steps": [
        "Practice Product Prioritization "
        "with additional guided exercises.",

        "Start learning Product Metrics "
        "because it is still a remaining skill gap."
    ]
}


print("\n==============================")
print("        ASK EDUPATH")
print("==============================")

print("\nYou can ask questions such as:")
print("- What should I learn next?")
print("- What are my remaining skill gaps?")
print("- How much progress have I made?")
print("- Why should I learn Product Metrics?")
print("- What should I practice more?")

print("\nType 'exit' to stop.")


while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        print("\nEduPath: Good luck with your learning journey!")
        break

    if not question.strip():
        print("EduPath: Please enter a question.")
        continue

    answer = ask_edupath(
        question,
        profile,
        progress,
        struggles,
        progress_report
    )

    print("\nEduPath:")
    print(answer)