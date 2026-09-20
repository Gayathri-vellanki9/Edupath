from agent.document_analyzer import analyze_document
from agent.skill_gap_analyzer import analyze_skill_gaps
from agent.learning_objective_generator import generate_learning_objectives
from agent.resource_recommender import recommend_resources
from agent.weekly_planner import generate_weekly_plan
from agent.practice_project_generator import generate_practice_and_projects

from agent.activity_tracker import load_activities
from agent.progress_evaluator import evaluate_progress
from agent.struggle_detector import detect_struggles
from agent.adaptive_planner import create_adaptive_plan
from agent.progress_report_generator import generate_progress_report

from edupath_storage import (
    save_results,
    load_results,
    results_exist
)


def is_quota_error(error):
    """
    Check whether an error is caused by
    Gemini API quota exhaustion.
    """

    error_text = str(error).lower()

    return (
        "429" in error_text
        or "resource_exhausted" in error_text
        or "quota exceeded" in error_text
        or "quota_exceeded" in error_text
    )


def create_quota_error_result(error):
    """
    Create a clean result when Gemini quota
    has been exhausted.
    """

    return {
        "status": "quota_exceeded",
        "message": (
            "Gemini API daily quota has been exhausted. "
            "Previously saved EduPath results can still "
            "be used."
        ),
        "error": str(error)
    }


def run_edupath(
    profile,
    document_text="",
    document_type="text",
    use_saved_results=False
):
    """
    Run the complete EduPath learning pipeline.

    If use_saved_results=True and saved results
    exist, load them instead of calling Gemini.
    """

    # ==========================================
    # LOAD SAVED RESULTS
    # ==========================================

    if use_saved_results and results_exist():

        saved_results = load_results()

        if saved_results is not None:

            print(
                "Loaded previously saved "
                "EduPath results."
            )

            return saved_results

    # ==========================================
    # 1. DOCUMENT ANALYSIS
    # ==========================================

    if document_text.strip():

        document_analysis = analyze_document(
            document_text,
            document_type
        )

        if "error" in document_analysis:

            if is_quota_error(
                document_analysis["error"]
            ):
                return create_quota_error_result(
                    document_analysis["error"]
                )

    else:

        document_analysis = {
            "skills": [],
            "tools": [],
            "projects": [],
            "experience": [],
            "certifications": [],
            "evidence": [],
            "summary": ""
        }

    # ==========================================
    # 2. SKILL GAP ANALYSIS
    # ==========================================

    try:

        skill_gaps = analyze_skill_gaps(
            profile,
            document_analysis
        )

    except Exception as error:

        if is_quota_error(error):
            return create_quota_error_result(error)

        raise

    # ==========================================
    # 3. LEARNING OBJECTIVES
    # ==========================================

    try:

        learning_objectives = (
            generate_learning_objectives(
                skill_gaps
            )
        )

    except Exception as error:

        if is_quota_error(error):
            return create_quota_error_result(error)

        raise

    # ==========================================
    # 4. RESOURCE RECOMMENDATIONS
    # ==========================================

    recommended_resources = recommend_resources(
        profile,
        learning_objectives
    )

    if "error" in recommended_resources:

        if is_quota_error(
            recommended_resources["error"]
        ):
            return create_quota_error_result(
                recommended_resources["error"]
            )

    # ==========================================
    # 5. WEEKLY PLAN
    # ==========================================

    try:

        weekly_plan = generate_weekly_plan(
            profile,
            learning_objectives,
            recommended_resources
        )

    except Exception as error:

        if is_quota_error(error):
            return create_quota_error_result(error)

        raise

    # ==========================================
    # 6. PRACTICE & PROJECTS
    # ==========================================

    try:

        practice_projects = (
            generate_practice_and_projects(
                profile,
                skill_gaps,
                learning_objectives
            )
        )

    except Exception as error:

        if is_quota_error(error):
            return create_quota_error_result(error)

        raise

    # ==========================================
    # 7. LOAD ACTIVITIES
    # ==========================================

    activities = load_activities()

    # ==========================================
    # 8. PROGRESS
    # ==========================================

    progress = evaluate_progress(
        profile,
        learning_objectives,
        activities
    )

    # ==========================================
    # 9. STRUGGLES
    # ==========================================

    struggles = detect_struggles(
        learning_objectives,
        activities
    )

    # ==========================================
    # 10. ADAPTIVE PLAN
    # ==========================================

    adaptive_plan = create_adaptive_plan(
        weekly_plan.get(
            "weekly_plan",
            []
        ),
        progress,
        struggles
    )

    # ==========================================
    # 11. PROGRESS REPORT
    # ==========================================

    progress_report = generate_progress_report(
        profile,
        progress,
        struggles
    )

    # ==========================================
    # 12. FINAL RESULT
    # ==========================================

    result = {
        "status": "success",
        "profile": profile,
        "document_analysis": document_analysis,
        "skill_gaps": skill_gaps,
        "learning_objectives": learning_objectives,
        "recommended_resources": recommended_resources,
        "weekly_plan": weekly_plan,
        "practice_projects": practice_projects,
        "activities": activities,
        "progress": progress,
        "struggles": struggles,
        "adaptive_plan": adaptive_plan,
        "progress_report": progress_report
    }

    # ==========================================
    # 13. SAVE RESULTS
    # ==========================================

    save_results(result)

    return result