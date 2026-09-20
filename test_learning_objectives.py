from agent.learning_objective_generator import (
    generate_learning_objectives
)


skill_gap_analysis = {
    "target_role": "Product Manager",
    "skill_gaps": [
        {
            "skill": "User Research",
            "current_level": "Unknown",
            "required_level": "Intermediate",
            "gap": "Needs experience conducting user interviews and identifying user pain points.",
            "priority": "High",
            "reason": "User research is an important Product Management capability.",
            "evidence": []
        },
        {
            "skill": "Product Analytics",
            "current_level": "Beginner",
            "required_level": "Intermediate",
            "gap": "Needs stronger understanding of product metrics and data-driven decisions.",
            "priority": "Medium",
            "reason": "Product managers use metrics to evaluate product performance.",
            "evidence": []
        }
    ]
}


result = generate_learning_objectives(
    skill_gap_analysis
)

print(result)