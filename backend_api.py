from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os
import json

from agent.activity_tracker import load_activities, record_activity
from agent.learning_chat_assistant import ask_edupath
from agent.document_analyzer import analyze_document
from agent.skill_gap_analyzer import analyze_skill_gaps


app = FastAPI(title="EduPath API")


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():

    return {
        "message": "EduPath API is running"
    }


# =========================================================
# HEALTH
# =========================================================

@app.get("/api/health")
def health():

    return {
        "status": "healthy"
    }


# =========================================================
# PROFILE
# =========================================================

@app.post("/api/profile")
def save_profile(profile: dict):

    return {
        "message": "Profile saved successfully",
        "profile": profile
    }


# =========================================================
# PROGRESS
# =========================================================

@app.get("/api/progress")
def get_progress():

    try:

        activities = load_activities()

        return {
            "activities": activities
        }

    except Exception as e:

        return {
            "activities": [],
            "error": str(e)
        }


# =========================================================
# ACTIVITY
# =========================================================

@app.post("/api/activity")
def add_activity(activity: dict):

    result = record_activity(

        activity_type=activity.get(
            "activity_type",
            ""
        ),

        skill=activity.get(
            "skill",
            ""
        ),

        title=activity.get(
            "title",
            ""
        ),

        status=activity.get(
            "status",
            "completed"
        ),

        estimated_minutes=activity.get(
            "estimated_minutes",
            0
        ),

        actual_minutes=activity.get(
            "actual_minutes",
            0
        ),

        score=activity.get(
            "score"
        )
    )

    return {
        "success": True,
        "result": result
    }


# =========================================================
# AI COACH
# =========================================================

@app.post("/api/ask")
def ask_question(data: dict):

    question = data.get(
        "question",
        ""
    )

    profile = data.get(
        "profile",
        {}
    )

    progress = data.get(
        "progress",
        {}
    )

    struggles = data.get(
        "struggles",
        []
    )

    progress_report = data.get(
        "progress_report",
        {}
    )

    answer = ask_edupath(

        question,

        profile,

        progress,

        struggles,

        progress_report

    )

    return {
        "answer": answer
    }


# =========================================================
# RESUME ANALYSIS
# =========================================================

@app.post("/api/analyze-document")
async def analyze_document_endpoint(

    file: UploadFile = File(...),

    # Optional target role.
    #
    # The current frontend does not send this yet,
    # so it is optional.
    target_role: str = Form("")
):

    allowed_extensions = [

        ".pdf",

        ".docx",

        ".doc",

        ".txt"

    ]


    filename = file.filename or ""


    extension = os.path.splitext(
        filename
    )[1].lower()


    # -----------------------------------------------------
    # Validate file
    # -----------------------------------------------------

    if extension not in allowed_extensions:

        return {

            "success": False,

            "message": (
                "Unsupported file type. "
                "Please upload PDF, DOCX, DOC, or TXT."
            )

        }


    temp_path = None


    try:

        # =================================================
        # 1. READ UPLOADED FILE
        # =================================================

        file_bytes = await file.read()


        if not file_bytes:

            return {

                "success": False,

                "message": "Uploaded file is empty."

            }


        # =================================================
        # 2. CREATE TEMPORARY FILE
        # =================================================

        with tempfile.NamedTemporaryFile(

            delete=False,

            suffix=extension

        ) as temp_file:

            temp_file.write(
                file_bytes
            )

            temp_path = temp_file.name


        # =================================================
        # 3. EXTRACT DOCUMENT TEXT
        # =================================================

        from utils.document_parser import extract_text


        with open(

            temp_path,

            "rb"

        ) as document_file:

            document_text = extract_text(
                document_file
            )


        if not document_text or not document_text.strip():

            return {

                "success": False,

                "message": (
                    "Could not extract text "
                    "from the document."
                )

            }


        # =================================================
        # 4. DOCUMENT ANALYSIS
        # =================================================

        document_analysis = analyze_document(

            document_text,

            "resume"

        )


        # Safety check in case the analyzer
        # returns something unexpected.

        if not isinstance(
            document_analysis,
            dict
        ):

            document_analysis = {

                "skills": [],

                "tools": [],

                "projects": [],

                "experience": [],

                "certifications": [],

                "evidence": [],

                "summary": ""

            }


        # =================================================
        # 5. BUILD LEARNER PROFILE
        # =================================================

        #
        # IMPORTANT:
        #
        # Previously this was:
        #
        # "target_role": "Product Manager"
        #
        # That forced every resume through
        # a Product Manager skill-gap analysis.
        #
        # Now we only use a target role if the
        # frontend/user actually provides one.
        #

        profile = {

            "target_role":
                target_role.strip()
                if target_role
                else "",


            "current_skills":
                document_analysis.get(
                    "skills",
                    []
                ),


            "tools":
                document_analysis.get(
                    "tools",
                    []
                ),


            "projects":
                document_analysis.get(
                    "projects",
                    []
                ),


            "experience":
                document_analysis.get(
                    "experience",
                    []
                ),


            "certifications":
                document_analysis.get(
                    "certifications",
                    []
                )

        }


        # =================================================
        # 6. SKILL GAP ANALYSIS
        # =================================================

        skill_gap_analysis = analyze_skill_gaps(

            profile,

            document_analysis

        )


        # Safety check

        if not isinstance(
            skill_gap_analysis,
            dict
        ):

            skill_gap_analysis = {

                "target_role":
                    profile.get(
                        "target_role",
                        ""
                    ),

                "skill_gaps": []

            }


        # =================================================
        # 7. REMOVE TEMP FILE
        # =================================================

        if (

            temp_path

            and os.path.exists(
                temp_path
            )

        ):

            os.remove(
                temp_path
            )

            temp_path = None


        # =================================================
        # 8. RETURN COMPLETE RESULT
        # =================================================

        return {

            "success": True,

            "filename": filename,

            "text": document_text,

            "document_analysis":
                document_analysis,

            "skill_gap_analysis":
                skill_gap_analysis

        }


    except Exception as e:

        # -------------------------------------------------
        # Clean temporary file if an error occurs
        # -------------------------------------------------

        if (

            temp_path

            and os.path.exists(
                temp_path
            )

        ):

            os.remove(
                temp_path
            )


        print(
            "Resume analysis error:",
            str(e)
        )


        return {

            "success": False,

            "message": str(e)

        }