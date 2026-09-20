def create_adaptive_plan(
    weekly_plan,
    progress,
    struggles
):
    updated_plan = []

    # Get struggling skills
    struggling_skills = {
        item.get("skill", "").lower()
        for item in struggles.get("struggling_skills", [])
    }

    # Get acquired skills
    acquired_skills = {
        skill.lower()
        for skill in progress.get("skills_acquired", [])
    }

    # Go through each day
    for day in weekly_plan:

        updated_tasks = []

        # Go through each task
        for task in day.get("tasks", []):

            skill = task.get("skill", "")
            skill_lower = skill.lower()

            # -----------------------------------
            # CASE 1: Learner is struggling
            # -----------------------------------
            if skill_lower in struggling_skills:

                new_task = task.copy()

                original_minutes = task.get(
                    "estimated_minutes",
                    30
                )

                # Add 20 minutes of extra practice
                new_task["estimated_minutes"] = (
                    original_minutes + 20
                )

                # Add guided practice
                new_task["activity"] = (
                    task.get("activity", "")
                    + " + Additional guided practice"
                )

                # Explain why the plan changed
                new_task["adaptive_reason"] = (
                    "Extra practice added because "
                    "the learner is struggling with "
                    + skill
                )

                updated_tasks.append(new_task)

            # -----------------------------------
            # CASE 2: Skill already acquired
            # -----------------------------------
            elif skill_lower in acquired_skills:

                new_task = task.copy()

                original_minutes = task.get(
                    "estimated_minutes",
                    30
                )

                # Reduce practice time by 15 minutes
                # but never go below 15 minutes
                new_task["estimated_minutes"] = max(
                    15,
                    original_minutes - 15
                )

                # Explain why the plan changed
                new_task["adaptive_reason"] = (
                    "Reduced practice time because "
                    "this skill has been acquired"
                )

                updated_tasks.append(new_task)

            # -----------------------------------
            # CASE 3: Normal skill
            # -----------------------------------
            else:

                # Keep the task unchanged
                updated_tasks.append(task.copy())

        # Add updated tasks for this day
        updated_plan.append({
            "day": day.get("day"),
            "tasks": updated_tasks
        })

    # Return the adaptive learning plan
    return {
        "adaptive_plan": updated_plan,
        "adaptations": {
            "struggling_skills": list(
                struggling_skills
            ),
            "acquired_skills": list(
                acquired_skills
            )
        }
    }