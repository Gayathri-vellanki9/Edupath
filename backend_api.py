from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os

from agent.activity_tracker import load_activities, record_activity
from agent.learning_chat_assistant import ask_edupath

app = FastAPI(title="EduPath API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "EduPath API is running"}


@app.get("/api/health")
def health():
    return {"status": "healthy"}


@app.post("/api/profile")
def save_profile(profile: dict):
    return {
        "message": "Profile saved successfully",
        "profile": profile
    }


@app.get("/api/progress")
def get_progress():
    try:
        activities = load_activities()
        return {"activities": activities}
    except Exception as e:
        return {"activities": [], "error": str(e)}


@app.post("/api/activity")
def add_activity(activity: dict):
    result = record_activity(
        activity_type=activity.get("activity_type", ""),
        skill=activity.get("skill", ""),
        title=activity.get("title", ""),
        status=activity.get("status", "completed"),
        estimated_minutes=activity.get("estimated_minutes", 0),
        actual_minutes=activity.get("actual_minutes", 0),
        score=activity.get("score")
    )

    return {
        "success": True,
        "result": result
    }


@app.post("/api/ask")
def ask_question(data: dict):
    question = data.get("question", "")
    profile = data.get("profile", {})
    progress = data.get("progress", {})
    struggles = data.get("struggles", [])
    progress_report = data.get("progress_report", {})

    answer = ask_edupath(
        question,
        profile,
        progress,
        struggles,
        progress_report
    )

    return {"answer": answer}


# Resume upload endpoint
@app.post("/api/analyze-document")
@app.post("/api/analyze-document")
async def analyze_document(file: UploadFile = File(...)):
    allowed_extensions = [".pdf", ".docx", ".doc", ".txt"]

    filename = file.filename or ""
    extension = os.path.splitext(filename)[1].lower()

    if extension not in allowed_extensions:
        return {
            "success": False,
            "message": "Unsupported file type. Please upload PDF, DOCX, DOC, or TXT."
        }

    try:
        # Read uploaded file
        file_bytes = await file.read()

        # Create a temporary file
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension
        ) as temp_file:
            temp_file.write(file_bytes)
            temp_path = temp_file.name

        # Open the temporary file as a FILE OBJECT
        # so the existing document parser can use .name
        with open(temp_path, "rb") as document_file:

            from utils.document_parser import extract_text

            document_text = extract_text(document_file)

        # Delete temporary file
        os.remove(temp_path)

        if not document_text or not document_text.strip():
            return {
                "success": False,
                "message": "Could not extract text from the document."
            }

        return {
            "success": True,
            "filename": filename,
            "text": document_text
        }

    except Exception as e:

        if "temp_path" in locals() and os.path.exists(temp_path):
            os.remove(temp_path)

        return {
            "success": False,
            "message": str(e)
        }
async def analyze_document(file: UploadFile = File(...)):

    allowed_extensions = [".pdf", ".docx", ".doc", ".txt"]

    filename = file.filename or ""
    extension = os.path.splitext(filename)[1].lower()

    if extension not in allowed_extensions:
        return {
            "success": False,
            "message": "Unsupported file type. Please upload PDF, DOCX, DOC, or TXT."
        }

    try:
        file_bytes = await file.read()

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension
        ) as temp_file:

            temp_file.write(file_bytes)
            temp_path = temp_file.name

        # Import existing document parser
        from utils.document_parser import extract_text

        text = extract_text(temp_path)

        # Remove temporary file
        os.remove(temp_path)

        return {
            "success": True,
            "filename": filename,
            "text": text
        }

    except Exception as e:

        if "temp_path" in locals() and os.path.exists(temp_path):
            os.remove(temp_path)

        return {
            "success": False,
            "message": str(e)
        }