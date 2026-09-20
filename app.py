import streamlit as st

from utils.document_parser import extract_text

from agent.document_analyzer import analyze_document
from agent.skill_gap_analyzer import analyze_skill_gaps
from agent.learning_objective_generator import generate_learning_objectives
from agent.resource_recommender import recommend_resources
from agent.weekly_planner import generate_weekly_plan
from agent.practice_project_generator import generate_practice_and_projects

from agent.activity_tracker import (
    load_activities,
    record_activity
)
from agent.progress_evaluator import evaluate_progress
from agent.struggle_detector import detect_struggles
from agent.adaptive_planner import create_adaptive_plan
from agent.progress_report_generator import generate_progress_report
from agent.learning_chat_assistant import ask_edupath

from edupath_storage import (
    save_results,
    load_results,
    results_exist
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="EduPath",
    page_icon="🎓",
    layout="wide"
)


# =========================================================
# EDUPATH 2.0 — UI / UX DESIGN SYSTEM
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --ink: #17142d;
    --muted: #77748b;
    --purple: #6c5ce7;
    --purple-dark: #4d3fc2;
    --lavender: #f0edff;
    --surface: #ffffff;
    --bg: #f7f7fc;
    --border: #e9e7f2;
}

.stApp {
    background:
        radial-gradient(circle at 8% 5%, rgba(124,103,238,.13), transparent 24%),
        radial-gradient(circle at 92% 8%, rgba(215,197,255,.18), transparent 22%),
        #f7f7fc;
}

.block-container {
    max-width: 1320px;
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}

html, body, [class*="css"] {
    font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

#MainMenu, footer { visibility: hidden; }

/* Hide sidebar completely */
section[data-testid="stSidebar"] { display: none; }

/* Top brand */
.edu-topbar {
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding: 10px 4px 14px;
    margin-bottom: 4px;
}
.edu-logo {
    display:flex;
    align-items:center;
    gap:10px;
    color:var(--ink);
    font-size:1.55rem;
    font-weight:800;
    letter-spacing:-.05em;
}
.edu-logo-mark {
    width:38px;
    height:38px;
    display:flex;
    align-items:center;
    justify-content:center;
    border-radius:12px;
    color:white;
    background:linear-gradient(135deg,#7969ef,#4f3dc2);
    box-shadow:0 8px 22px rgba(89,70,205,.25);
}
.edu-top-caption { color:#89869a; font-size:.82rem; }

/* Navigation pills */
div[data-testid="stRadio"] > div[role="radiogroup"] {
    display:flex;
    flex-wrap:wrap;
    gap:7px;
    padding:8px;
    background:rgba(255,255,255,.78);
    border:1px solid var(--border);
    border-radius:18px;
    box-shadow:0 8px 28px rgba(42,35,83,.06);
    margin-bottom:24px;
}
div[data-testid="stRadio"] label {
    background:transparent;
    border-radius:12px;
    padding:7px 12px;
    transition:.18s ease;
}
div[data-testid="stRadio"] label:hover { background:#f0edff; }
div[data-testid="stRadio"] label:has(input:checked) {
    background:linear-gradient(135deg,#6d5de8,#5141c5);
    box-shadow:0 6px 16px rgba(81,65,197,.2);
}
div[data-testid="stRadio"] label:has(input:checked) p { color:white !important; font-weight:700; }
div[data-testid="stRadio"] label p { font-size:.84rem; font-weight:600; color:#625f73; }
div[data-testid="stRadio"] label > div:first-child { display:none; }

/* Page headings */
h1 { color:var(--ink) !important; font-size:2.35rem !important; font-weight:800 !important; letter-spacing:-.055em; }
h2 { color:#24203d !important; font-weight:750 !important; letter-spacing:-.035em; }
h3 { color:#302b4d !important; font-weight:700 !important; }
p, label, .stMarkdown { color:#67647a; }

/* Hero */
.edu-hero {
    position:relative;
    overflow:hidden;
    background:linear-gradient(135deg,#201a48 0%,#4f3fc4 55%,#806fea 100%);
    border-radius:28px;
    padding:38px 40px;
    margin:6px 0 26px;
    box-shadow:0 18px 48px rgba(62,49,154,.22);
}
.edu-hero:after {
    content:"";
    position:absolute;
    width:250px;height:250px;
    right:-70px;top:-110px;
    border-radius:50%;
    background:rgba(255,255,255,.12);
}
.edu-hero-title { color:white !important; font-size:2.15rem; font-weight:800; letter-spacing:-.05em; position:relative; z-index:1; }
.edu-hero-subtitle { color:#e9e5ff !important; font-size:1rem; line-height:1.65; max-width:760px; margin-top:8px; position:relative; z-index:1; }

/* Cards */
.edu-card {
    background:rgba(255,255,255,.94);
    border:1px solid var(--border);
    border-radius:20px;
    padding:22px;
    margin:8px 0 16px;
    box-shadow:0 10px 28px rgba(39,32,79,.055);
}
.edu-card:hover { box-shadow:0 14px 34px rgba(39,32,79,.09); }
.edu-card-title { color:#2b2745; font-size:1.05rem; font-weight:750; margin-bottom:7px; }
.edu-card-text { color:#716e81; line-height:1.6; }
.edu-small { color:#8b8899 !important; font-size:.82rem; }

/* Metrics */
div[data-testid="stMetric"] {
    background:rgba(255,255,255,.92);
    border:1px solid var(--border);
    border-radius:20px;
    padding:20px;
    box-shadow:0 9px 25px rgba(40,33,81,.05);
}
div[data-testid="stMetricLabel"] { color:#858195 !important; font-weight:600; }
div[data-testid="stMetricValue"] { color:#292441 !important; font-weight:800 !important; }

/* Buttons */
.stButton > button, .stFormSubmitButton > button {
    border:0 !important;
    border-radius:12px !important;
    min-height:44px;
    padding:.62rem 1.15rem !important;
    font-weight:700 !important;
    background:linear-gradient(135deg,#7160eb,#5241c5) !important;
    color:white !important;
    box-shadow:0 7px 18px rgba(81,65,197,.2);
    transition:.18s ease;
}
.stButton > button:hover, .stFormSubmitButton > button:hover { transform:translateY(-2px); box-shadow:0 11px 25px rgba(81,65,197,.27); }

/* Inputs */
.stTextInput input, .stTextArea textarea, .stNumberInput input,
.stSelectbox div[data-baseweb="select"] > div,
.stMultiSelect div[data-baseweb="select"] > div {
    border-radius:13px !important;
    border:1px solid #e1deeb !important;
    background:white !important;
}

/* File uploader */
section[data-testid="stFileUploaderDropzone"] {
    background:linear-gradient(180deg,#fff,#fbfaff);
    border:1.5px dashed #bdb5e8;
    border-radius:20px;
    padding:10px;
}

/* Expanders */
details {
    background:white !important;
    border:1px solid var(--border) !important;
    border-radius:16px !important;
    margin-bottom:10px;
    box-shadow:0 5px 18px rgba(39,32,79,.035);
}

/* Progress */
.stProgress > div > div > div > div { background:linear-gradient(90deg,#6e5ee8,#9a8df5); }

/* Alerts */
div[data-testid="stAlert"] { border-radius:15px; border:1px solid var(--border); }

/* Journey timeline */
.edu-step {
    background:white;
    border:1px solid var(--border);
    border-radius:18px;
    padding:17px;
    min-height:90px;
    box-shadow:0 7px 20px rgba(39,32,79,.045);
}
.edu-step-done { border-color:#d7cffb; background:linear-gradient(180deg,#fff,#f7f4ff); }
.edu-step-icon { font-size:1.35rem; }
.edu-step-title { font-weight:750; color:#302b4d; margin-top:6px; }
.edu-step-status { font-size:.78rem; color:#888497; margin-top:3px; }

/* Priority badges */
.edu-priority-high,.edu-priority-medium,.edu-priority-low {
    display:inline-block; padding:5px 10px; border-radius:999px; font-weight:700; font-size:.78rem;
}
.edu-priority-high { color:#b42318 !important; background:#fff0ee; }
.edu-priority-medium { color:#946200 !important; background:#fff8df; }
.edu-priority-low { color:#147a4b !important; background:#eaf8f0; }

.edu-footer { text-align:center; color:#9895a7 !important; font-size:.78rem; padding:30px 0 8px; }

@media (max-width: 900px) {
    .edu-hero { padding:28px 24px; }
    .edu-hero-title { font-size:1.7rem; }
    div[data-testid="stRadio"] > div[role="radiogroup"] { overflow-x:auto; flex-wrap:nowrap; }
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATE
# =========================================================

DEFAULT_STATE = {
    "profile_created": False,
    "profile": {},
    "documents": [],
    "document_analysis": None,
    "skill_gap_analysis": None,
    "learning_objectives": None,
    "recommended_resources": None,
    "weekly_plan": None,
    "practice_projects": None,
    "saved_results_loaded": False
}

for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def is_quota_error(error):
    text = str(error).lower()
    return (
        "429" in text
        or "resource_exhausted" in text
        or "quota exceeded" in text
        or "quota_exceeded" in text
    )


def show_api_error(error):
    if is_quota_error(error):
        st.error(
            "Gemini API daily quota is currently exhausted. "
            "Previously generated EduPath results can still "
            "be viewed, but new AI generation may need to wait "
            "until the quota resets or use a billed API project."
        )
    else:
        st.error(f"Something went wrong: {error}")


def get_profile():
    return st.session_state.get("profile", {})


def get_learning_objectives():
    return st.session_state.get(
        "learning_objectives"
    ) or {}


def get_weekly_plan():
    return st.session_state.get(
        "weekly_plan"
    ) or {}


def save_current_results():
    profile = get_profile()

    if not profile:
        return

    results = {
        "status": "success",
        "profile": profile,
        "document_analysis": (
            st.session_state.get("document_analysis")
            or {}
        ),
        "skill_gaps": (
            st.session_state.get("skill_gap_analysis")
            or {}
        ),
        "learning_objectives": (
            st.session_state.get("learning_objectives")
            or {}
        ),
        "recommended_resources": (
            st.session_state.get("recommended_resources")
            or {}
        ),
        "weekly_plan": (
            st.session_state.get("weekly_plan")
            or {}
        ),
        "practice_projects": (
            st.session_state.get("practice_projects")
            or {}
        ),
        "activities": load_activities()
    }

    save_results(results)


def load_saved_results_into_session():
    if not results_exist():
        return

    saved = load_results()

    # Ignore the small test data created by test_storage.py.
    if not isinstance(saved, dict):
        return

    if saved.get("status") != "success":
        return

    if "learning_objectives" not in saved:
        return

    if not saved.get("profile"):
        return

    st.session_state.profile = saved.get(
        "profile",
        {}
    )

    st.session_state.profile_created = True

    st.session_state.document_analysis = saved.get(
        "document_analysis"
    )

    st.session_state.skill_gap_analysis = saved.get(
        "skill_gaps"
    )

    st.session_state.learning_objectives = saved.get(
        "learning_objectives"
    )

    st.session_state.recommended_resources = saved.get(
        "recommended_resources"
    )

    st.session_state.weekly_plan = saved.get(
        "weekly_plan"
    )

    st.session_state.practice_projects = saved.get(
        "practice_projects"
    )

    st.session_state.saved_results_loaded = True


if not st.session_state.saved_results_loaded:
    load_saved_results_into_session()


# =========================================================
# TOP NAVIGATION
# =========================================================

st.markdown(
    """
    <div class="edu-topbar">
        <div class="edu-logo">
            <div class="edu-logo-mark">✦</div>
            <div>EduPath</div>
        </div>
        <div class="edu-top-caption">Personalized learning, powered by AI</div>
    </div>
    """,
    unsafe_allow_html=True
)

page = st.radio(
    "Navigation",
    [
        "Dashboard",
        "My Journey",
        "Learner Profile",
        "Documents",
        "Skill Gaps",
        "Learning Objectives",
        "Resources",
        "Weekly Plan",
        "Practice & Projects",
        "Progress",
        "Adaptive Learning",
        "Reports",
        "Ask EduPath"
    ],
    horizontal=True,
    label_visibility="collapsed"
)

# My Journey is a visual overview that points learners through the existing workflow.
if page == "My Journey":
    page = "Dashboard"
    journey_mode = True
else:
    journey_mode = False

PAGE_META = {
    "Dashboard": ("Your learning journey", "See where you are, what to learn next, and how EduPath is adapting your path."),
    "Learner Profile": ("Build your learner profile", "Tell EduPath about your goal, skills, experience, and learning preferences."),
    "Documents": ("Your evidence", "Upload your resume, portfolio, certificates, or project descriptions."),
    "Skill Gaps": ("Understand your skill gaps", "See the difference between your current capabilities and your target role."),
    "Learning Objectives": ("Turn gaps into objectives", "Convert each priority gap into clear, measurable learning outcomes."),
    "Resources": ("Learn with the right resources", "Get recommendations matched to your objectives and learning preferences."),
    "Weekly Plan": ("Your weekly learning plan", "Follow a practical schedule built around your available time."),
    "Practice & Projects": ("Practice and build", "Strengthen your skills through realistic tasks and portfolio-ready projects."),
    "Progress": ("Track your progress", "Record activities and see how your skills are developing."),
    "Adaptive Learning": ("Your adaptive path", "EduPath adjusts the plan based on progress and areas that need more practice."),
    "Reports": ("Progress report", "Review skills acquired, skills in progress, remaining gaps, and next steps."),
    "Ask EduPath": ("Meet your AI learning coach", "Ask questions about your learning journey and get answers using your current EduPath state.")
}

if page in PAGE_META and page != "Dashboard":
    title, subtitle = PAGE_META[page]
    st.markdown(
        f"""
        <div style='margin:2px 0 22px;'>
            <div style='font-size:2rem;font-weight:800;color:#17142d;letter-spacing:-.045em;'>{title}</div>
            <div style='font-size:.96rem;color:#77748b;margin-top:6px;line-height:1.5;'>{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# LEARNER PROFILE
# =========================================================

if page == "Learner Profile":

    st.title("🎓 EduPath")

    st.subheader(
        "Close your skill gap. Master your next career chapter."
    )

    st.write(
        "EduPath is an adaptive learning agent that creates "
        "a personalized learning journey based on your current "
        "skills and career goal."
    )

    st.divider()

    st.header("👤 Learner Profile")

    profile = get_profile()

    with st.form("learner_profile_form"):

        career_goal = st.text_input(
            "Career goal",
            value=profile.get("career_goal", ""),
            placeholder=(
                "Example: Get a Product Management internship"
            )
        )

        target_role = st.text_input(
            "Target role",
            value=profile.get("target_role", ""),
            placeholder="Example: Product Manager"
        )

        current_skills = st.text_area(
            "Current skills",
            value=profile.get("current_skills", ""),
            placeholder="Example: Python, SQL, communication"
        )

        experience = st.text_area(
            "Experience",
            value=profile.get("experience", ""),
            placeholder="Example: Student with academic projects"
        )

        hours_per_week = st.number_input(
            "Hours available per week",
            min_value=1,
            max_value=60,
            value=int(profile.get("hours_per_week", 10))
        )

        preferences = [
            "Practical learning",
            "Videos",
            "Reading",
            "Projects",
            "Mixed learning"
        ]

        old_preference = profile.get(
            "learning_preference",
            "Practical learning"
        )

        if old_preference not in preferences:
            old_preference = "Practical learning"

        learning_preference = st.selectbox(
            "Learning preference",
            preferences,
            index=preferences.index(old_preference)
        )

        submitted = st.form_submit_button(
            "Save Learner Profile"
        )

    if submitted:

        if not target_role.strip():
            st.warning("Please enter your target role.")

        elif not career_goal.strip():
            st.warning("Please enter your career goal.")

        else:

            st.session_state.profile = {
                "career_goal": career_goal,
                "target_role": target_role,
                "current_skills": current_skills,
                "experience": experience,
                "hours_per_week": hours_per_week,
                "learning_preference": learning_preference
            }

            st.session_state.profile_created = True

            # A changed profile should trigger a fresh analysis.
            st.session_state.document_analysis = None
            st.session_state.skill_gap_analysis = None
            st.session_state.learning_objectives = None
            st.session_state.recommended_resources = None
            st.session_state.weekly_plan = None
            st.session_state.practice_projects = None
            st.session_state.saved_results_loaded = False

            st.success(
                "Learner profile saved successfully!"
            )

            save_current_results()

    if st.session_state.profile_created:

        st.divider()

        st.subheader("Current Profile")

        profile = get_profile()

        col1, col2 = st.columns(2)

        with col1:
            st.write(
                f"**Career Goal:** "
                f"{profile.get('career_goal', '')}"
            )

            st.write(
                f"**Target Role:** "
                f"{profile.get('target_role', '')}"
            )

            st.write(
                f"**Experience:** "
                f"{profile.get('experience', '')}"
            )

        with col2:
            st.write(
                f"**Current Skills:** "
                f"{profile.get('current_skills', '')}"
            )

            st.write(
                f"**Hours/Week:** "
                f"{profile.get('hours_per_week', '')}"
            )

            st.write(
                f"**Learning Preference:** "
                f"{profile.get('learning_preference', '')}"
            )


# =========================================================
# DOCUMENTS
# =========================================================

elif page == "Documents":

    st.header("📄 Documents")

    st.write(
        "Upload documents so EduPath can understand your "
        "existing capabilities and evidence."
    )

    document_type = st.selectbox(
        "Document type",
        [
            "Resume",
            "Portfolio",
            "Certificate",
            "Project Description"
        ]
    )

    uploaded_file = st.file_uploader(
        f"Upload your {document_type}",
        type=["pdf", "docx", "txt"]
    )

    if uploaded_file is not None:

        st.write(
            f"Selected file: **{uploaded_file.name}**"
        )

        if st.button("🤖 Analyze Document"):

            if not st.session_state.profile_created:

                st.warning(
                    "Please complete your Learner Profile first."
                )

            else:

                with st.spinner(
                    "EduPath is analyzing your document..."
                ):

                    try:

                        document_text = extract_text(
                            uploaded_file
                        )

                        if not document_text.strip():

                            st.error(
                                "Could not extract text from this document."
                            )

                        else:

                            analysis = analyze_document(
                                document_text,
                                document_type
                            )

                            if analysis.get("error"):
                                show_api_error(
                                    analysis["error"]
                                )

                            else:

                                st.session_state.document_analysis = (
                                    analysis
                                )

                                document_info = {
                                    "name": uploaded_file.name,
                                    "type": document_type
                                }

                                # Avoid duplicate entries after reruns.
                                if document_info not in (
                                    st.session_state.documents
                                ):
                                    st.session_state.documents.append(
                                        document_info
                                    )

                                skill_gap_result = (
                                    analyze_skill_gaps(
                                        st.session_state.profile,
                                        analysis
                                    )
                                )

                                st.session_state.skill_gap_analysis = (
                                    skill_gap_result
                                )

                                st.session_state.learning_objectives = None
                                st.session_state.recommended_resources = None
                                st.session_state.weekly_plan = None
                                st.session_state.practice_projects = None

                                save_current_results()

                                st.success(
                                    "Document analyzed successfully!"
                                )

                    except Exception as e:
                        show_api_error(e)

    if st.session_state.document_analysis:

        st.divider()

        st.subheader("🔍 Document Analysis")

        analysis = st.session_state.document_analysis

        summary = analysis.get("summary", "")

        if summary:
            st.write(f"**Summary:** {summary}")

        for title, key, emoji in [
            ("Skills", "skills", "🧠"),
            ("Tools", "tools", "🛠️"),
            ("Projects", "projects", "🚀"),
            ("Experience", "experience", "💼"),
            ("Certifications", "certifications", "📜"),
            ("Evidence", "evidence", "🔎")
        ]:

            values = analysis.get(key, [])

            if values:
                st.write(f"### {emoji} {title}")

                for item in values:
                    st.write(f"- {item}")

    st.divider()

    st.subheader("📚 Uploaded Documents")

    if not st.session_state.documents:

        st.write("No documents uploaded yet.")

    else:

        for document in st.session_state.documents:

            col1, col2 = st.columns([3, 1])

            with col1:
                st.write(
                    f"📄 **{document['name']}**"
                )

            with col2:
                st.write(document["type"])


# =========================================================
# DASHBOARD
# =========================================================

elif page == "Dashboard":

    st.markdown(
        """
        <div class="edu-hero">
            <div class="edu-hero-title">Your learning journey, personalized.</div>
            <div class="edu-hero-subtitle">EduPath turns your current skills and career goal into an adaptive path toward your target role.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if journey_mode:
        st.markdown("## 🧭 Your EduPath roadmap")
        steps = [
            ("📄", "Understand", bool(st.session_state.document_analysis)),
            ("🎯", "Find gaps", bool(st.session_state.skill_gap_analysis)),
            ("🧠", "Set objectives", bool(st.session_state.learning_objectives)),
            ("📚", "Learn", bool(st.session_state.recommended_resources)),
            ("📅", "Plan", bool(st.session_state.weekly_plan)),
            ("🚀", "Practice", bool(st.session_state.practice_projects)),
            ("📈", "Improve", len(load_activities()) > 0),
        ]
        cols = st.columns(len(steps))
        for col, (icon, title, done) in zip(cols, steps):
            with col:
                st.markdown(
                    f"<div class='edu-step {'edu-step-done' if done else ''}'><div class='edu-step-icon'>{'✓' if done else icon}</div><div class='edu-step-title'>{title}</div><div class='edu-step-status'>{'Complete' if done else 'Next step'}</div></div>",
                    unsafe_allow_html=True
                )
        st.markdown("<br>", unsafe_allow_html=True)

    if not st.session_state.profile_created:

        st.info(
            "Complete your Learner Profile to get started."
        )

    else:

        profile = get_profile()

        st.subheader(
            f"Target Role: {profile.get('target_role', '')}"
        )

        activities = load_activities()

        try:
            objectives = get_learning_objectives()

            if objectives:
                progress = evaluate_progress(
                    profile,
                    objectives,
                    activities
                )
                progress_percentage = progress.get(
                    "overall_progress_percentage",
                    0
                )
            else:
                progress_percentage = 0

        except Exception:
            progress_percentage = 0

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Documents",
                len(st.session_state.documents)
            )

        with col2:

            gaps = []

            if st.session_state.skill_gap_analysis:
                gaps = st.session_state.skill_gap_analysis.get(
                    "skill_gaps",
                    []
                )

            st.metric(
                "Skill Gaps",
                len(gaps)
            )

        with col3:

            objective_areas = []

            if st.session_state.learning_objectives:
                objective_areas = (
                    st.session_state.learning_objectives.get(
                        "objectives",
                        []
                    )
                )

            st.metric(
                "Objective Areas",
                len(objective_areas)
            )

        with col4:

            st.metric(
                "Progress",
                f"{progress_percentage}%"
            )

        st.divider()

        st.subheader("Your Learning Journey")

        journey = [
            (
                "📄 Document Analysis",
                bool(st.session_state.document_analysis)
            ),
            (
                "🎯 Skill Gap Analysis",
                bool(st.session_state.skill_gap_analysis)
            ),
            (
                "📚 Learning Objectives",
                bool(st.session_state.learning_objectives)
            ),
            (
                "🔗 Recommended Resources",
                bool(st.session_state.recommended_resources)
            ),
            (
                "📅 Personalized Weekly Plan",
                bool(st.session_state.weekly_plan)
            ),
            (
                "📝 Practice & Projects",
                bool(st.session_state.practice_projects)
            ),
            (
                "📊 Progress Tracking",
                len(activities) > 0
            ),
            (
                "🔄 Adaptive Learning",
                bool(st.session_state.weekly_plan)
            )
        ]

        for name, completed in journey:
            if completed:
                st.write(f"✅ {name}")
            else:
                st.write(f"⬜ {name}")

        st.divider()

        st.subheader("🚀 Quick Start")

        st.write(
            "Use the sidebar to move through the journey. "
            "For a fresh learner journey, follow this order:"
        )

        st.info(
            "Learner Profile → Documents → Skill Gaps → "
            "Learning Objectives → Resources → Weekly Plan → "
            "Practice & Projects → Progress → Adaptive Learning → Reports"
        )


# =========================================================
# SKILL GAPS
# =========================================================

elif page == "Skill Gaps":

    st.header("🎯 Skill Gap Analysis")

    st.markdown(
        """
        <div class="edu-card">
            <div class="edu-card-title">Understand what to learn next</div>
            <div class="edu-card-text">EduPath compares the capabilities found in your profile and documents with the skills required for your target role.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not st.session_state.skill_gap_analysis:

        st.info(
            "Complete your Learner Profile and analyze "
            "a document first."
        )

    else:

        result = st.session_state.skill_gap_analysis

        st.subheader(
            f"Target Role: "
            f"{result.get('target_role', '')}"
        )

        gaps = result.get(
            "skill_gaps",
            []
        )

        if not gaps:

            st.success(
                "No major skill gaps identified."
            )

        else:

            st.write(
                f"EduPath identified **{len(gaps)} "
                f"skill gap(s)**."
            )

            for gap in gaps:

                st.markdown('<div class="edu-card">', unsafe_allow_html=True)

                st.subheader(
                    f"📌 "
                    f"{gap.get('skill', 'Unknown Skill')}"
                )

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.write(
                        f"**Current Level:** "
                        f"{gap.get('current_level', 'Unknown')}"
                    )

                with col2:
                    st.write(
                        f"**Required Level:** "
                        f"{gap.get('required_level', 'Unknown')}"
                    )

                with col3:
                    st.write(
                        f"**Priority:** "
                        f"{gap.get('priority', 'Unknown')}"
                    )

                st.write(
                    f"**Gap:** "
                    f"{gap.get('gap', '')}"
                )

                st.write(
                    f"**Why:** "
                    f"{gap.get('reason', '')}"
                )

                evidence = gap.get(
                    "evidence",
                    []
                )

                if evidence:

                    st.write("**Evidence:**")

                    for item in evidence:
                        st.write(f"- {item}")

                st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# LEARNING OBJECTIVES
# =========================================================

elif page == "Learning Objectives":

    st.header("📚 Learning Objectives")

    st.write(
        "EduPath converts your identified skill gaps "
        "into structured learning objectives."
    )

    if not st.session_state.skill_gap_analysis:

        st.info(
            "Complete your Learner Profile and "
            "Skill Gap Analysis first."
        )

    else:

        if st.button("🎯 Generate Learning Objectives"):

            with st.spinner(
                "EduPath is creating personalized learning objectives..."
            ):

                try:

                    objectives = generate_learning_objectives(
                        st.session_state.skill_gap_analysis
                    )

                    if objectives.get("error"):
                        show_api_error(
                            objectives["error"]
                        )

                    else:

                        st.session_state.learning_objectives = (
                            objectives
                        )

                        st.session_state.recommended_resources = None
                        st.session_state.weekly_plan = None
                        st.session_state.practice_projects = None

                        save_current_results()

                        st.success(
                            "Learning objectives generated!"
                        )

                except Exception as e:
                    show_api_error(e)

        if st.session_state.learning_objectives:

            result = st.session_state.learning_objectives

            st.divider()

            st.subheader(
                f"Target Role: "
                f"{result.get('target_role', '')}"
            )

            objectives = result.get(
                "objectives",
                []
            )

            if not objectives:

                st.info(
                    "No learning objectives were generated."
                )

            else:

                for item in objectives:

                    st.markdown("---")

                    st.subheader(
                        f"📌 {item.get('skill', '')}"
                    )

                    st.write(
                        f"**Priority:** "
                        f"{item.get('priority', '')}"
                    )

                    st.write(
                        f"**Current Level:** "
                        f"{item.get('current_level', '')}"
                    )

                    st.write(
                        f"**Required Level:** "
                        f"{item.get('required_level', '')}"
                    )

                    objective_list = item.get(
                        "learning_objectives",
                        []
                    )

                    for index, objective in enumerate(
                        objective_list,
                        start=1
                    ):

                        st.write(
                            f"### Objective {index}"
                        )

                        st.write(
                            f"**{objective.get('objective', '')}**"
                        )

                        description = objective.get(
                            "description",
                            ""
                        )

                        if description:
                            st.write(description)

                        criteria = objective.get(
                            "success_criteria",
                            []
                        )

                        if criteria:

                            st.write(
                                "**Success Criteria:**"
                            )

                            for criterion in criteria:
                                st.write(
                                    f"- {criterion}"
                                )


# =========================================================
# RESOURCES
# =========================================================

elif page == "Resources":

    st.header("🔗 Recommended Resources")

    st.write(
        "EduPath recommends learning resources "
        "based on your learning objectives, skill level, "
        "and available learning time."
    )

    if not st.session_state.learning_objectives:

        st.info(
            "Generate Learning Objectives first."
        )

    else:

        if st.button("🔗 Recommend Learning Resources"):

            with st.spinner(
                "EduPath is finding relevant resources..."
            ):

                try:

                    resources = recommend_resources(
                        st.session_state.profile,
                        st.session_state.learning_objectives
                    )

                    if resources.get("error"):
                        show_api_error(
                            resources["error"]
                        )

                    else:

                        st.session_state.recommended_resources = (
                            resources
                        )

                        st.session_state.weekly_plan = None
                        st.session_state.practice_projects = None

                        save_current_results()

                        st.success(
                            "Learning resources generated!"
                        )

                except Exception as e:
                    show_api_error(e)

        if st.session_state.recommended_resources:

            result = st.session_state.recommended_resources

            st.divider()

            st.subheader(
                f"Target Role: "
                f"{result.get('target_role', '')}"
            )

            resource_groups = result.get(
                "resources",
                []
            )

            if not resource_groups:

                st.info(
                    "No resources were generated."
                )

            else:

                for group in resource_groups:

                    st.markdown("---")

                    st.subheader(
                        f"📌 {group.get('skill', '')}"
                    )

                    st.write(
                        f"**Objective:** "
                        f"{group.get('objective', '')}"
                    )

                    resources = group.get(
                        "resources",
                        []
                    )

                    for resource in resources:

                        st.write(
                            f"### 📚 {resource.get('title', '')}"
                        )

                        st.write(
                            f"**Type:** "
                            f"{resource.get('type', '')}"
                        )

                        st.write(
                            f"**Level:** "
                            f"{resource.get('level', '')}"
                        )

                        st.write(
                            f"**Estimated Time:** "
                            f"{resource.get('estimated_time', '')}"
                        )

                        description = resource.get(
                            "description",
                            ""
                        )

                        if description:
                            st.write(description)

                        why_relevant = resource.get(
                            "why_relevant",
                            ""
                        )

                        if why_relevant:
                            st.write(
                                f"**Why this is relevant:** "
                                f"{why_relevant}"
                            )

                        url = resource.get(
                            "url",
                            ""
                        )

                        if url:
                            st.link_button(
                                "Open Resource",
                                url
                            )


# =========================================================
# WEEKLY PLAN
# =========================================================

elif page == "Weekly Plan":

    st.header("📅 Personalized Weekly Learning Plan")

    st.write(
        "EduPath creates a 7-day learning plan "
        "based on your objectives, resources, "
        "available time, and learning preferences."
    )

    if not st.session_state.profile_created:

        st.info(
            "Complete your Learner Profile first."
        )

    elif not st.session_state.learning_objectives:

        st.info(
            "Generate Learning Objectives first."
        )

    elif not st.session_state.recommended_resources:

        st.info(
            "Generate Recommended Resources first."
        )

    else:

        if st.button("📅 Generate My Weekly Plan"):

            with st.spinner(
                "EduPath is creating your personalized weekly plan..."
            ):

                try:

                    plan = generate_weekly_plan(
                        st.session_state.profile,
                        st.session_state.learning_objectives,
                        st.session_state.recommended_resources
                    )

                    if plan.get("error"):
                        show_api_error(
                            plan["error"]
                        )

                    else:

                        st.session_state.weekly_plan = plan

                        save_current_results()

                        st.success(
                            "Your personalized weekly plan is ready!"
                        )

                except Exception as e:
                    show_api_error(e)

        if st.session_state.weekly_plan:

            result = st.session_state.weekly_plan

            st.divider()

            st.subheader(
                f"Target Role: "
                f"{result.get('target_role', '')}"
            )

            total_hours = result.get(
                "total_hours",
                0
            )

            st.metric(
                "Planned Weekly Hours",
                f"{total_hours} hours"
            )

            weekly_plan = result.get(
                "weekly_plan",
                []
            )

            if not weekly_plan:

                st.info(
                    "No weekly plan was generated."
                )

            else:

                for day in weekly_plan:

                    st.markdown("---")

                    st.subheader(
                        f"📅 {day.get('day', '')}"
                    )

                    tasks = day.get(
                        "tasks",
                        []
                    )

                    if not tasks:

                        st.write(
                            "No tasks scheduled."
                        )

                    else:

                        for index, task in enumerate(
                            tasks,
                            start=1
                        ):

                            st.write(
                                f"### Task {index}"
                            )

                            st.write(
                                f"**Skill:** "
                                f"{task.get('skill', '')}"
                            )

                            st.write(
                                f"**Objective:** "
                                f"{task.get('objective', '')}"
                            )

                            st.write(
                                f"**Activity:** "
                                f"{task.get('activity', '')}"
                            )

                            st.write(
                                f"**Task Type:** "
                                f"{task.get('task_type', '')}"
                            )

                            st.write(
                                f"**Estimated Time:** "
                                f"{task.get('estimated_minutes', 0)} minutes"
                            )

                            resource = task.get(
                                "resource",
                                ""
                            )

                            if resource:
                                st.write(
                                    f"**Resource:** {resource}"
                                )


# =========================================================
# PRACTICE & PROJECTS
# =========================================================

elif page == "Practice & Projects":

    st.header("📝 Practice & Projects")

    st.write(
        "EduPath generates practice tasks and project ideas "
        "based on your current level and learning objectives."
    )

    if not st.session_state.profile_created:

        st.info(
            "Complete your Learner Profile first."
        )

    elif not st.session_state.skill_gap_analysis:

        st.info(
            "Complete Skill Gap Analysis first."
        )

    elif not st.session_state.learning_objectives:

        st.info(
            "Generate Learning Objectives first."
        )

    else:

        if st.button(
            "🧠 Generate Practice Tasks & Projects"
        ):

            with st.spinner(
                "EduPath is creating practice tasks and project ideas..."
            ):

                try:

                    result = generate_practice_and_projects(
                        st.session_state.profile,
                        st.session_state.skill_gap_analysis,
                        st.session_state.learning_objectives
                    )

                    if result.get("error"):
                        show_api_error(
                            result["error"]
                        )

                    else:

                        st.session_state.practice_projects = (
                            result
                        )

                        save_current_results()

                        st.success(
                            "Practice tasks and projects generated!"
                        )

                except Exception as e:
                    show_api_error(e)

        result = st.session_state.practice_projects

        if result:

            st.divider()

            st.subheader("🎯 Practice Tasks")

            practice_tasks = result.get(
                "practice_tasks",
                []
            )

            if not practice_tasks:

                st.info(
                    "No practice tasks were generated."
                )

            else:

                for index, task in enumerate(
                    practice_tasks,
                    start=1
                ):

                    with st.expander(
                        f"Task {index}: "
                        f"{task.get('task', 'Practice Task')}"
                    ):

                        st.write(
                            f"**Skill:** "
                            f"{task.get('skill', '')}"
                        )

                        st.write(
                            f"**Objective:** "
                            f"{task.get('objective', '')}"
                        )

                        st.write(
                            f"**Difficulty:** "
                            f"{task.get('difficulty', '')}"
                        )

                        instructions = task.get(
                            "instructions",
                            []
                        )

                        if instructions:

                            st.write("**Instructions:**")

                            for instruction in instructions:
                                st.write(
                                    f"- {instruction}"
                                )

                        st.write(
                            f"**Estimated Time:** "
                            f"{task.get('estimated_minutes', 0)} minutes"
                        )

                        st.write(
                            f"**Expected Output:** "
                            f"{task.get('expected_output', '')}"
                        )

                        criteria = task.get(
                            "evaluation_criteria",
                            []
                        )

                        if criteria:

                            st.write(
                                "**Evaluation Criteria:**"
                            )

                            for criterion in criteria:
                                st.write(
                                    f"- {criterion}"
                                )

            st.divider()

            st.subheader("🚀 Project Ideas")

            project_ideas = result.get(
                "project_ideas",
                []
            )

            if not project_ideas:

                st.info(
                    "No project ideas were generated."
                )

            else:

                for project in project_ideas:

                    with st.expander(
                        f"🚀 {project.get('title', 'Project')}"
                    ):

                        st.write(
                            f"**Skill:** "
                            f"{project.get('skill', '')}"
                        )

                        st.write(
                            f"**Difficulty:** "
                            f"{project.get('difficulty', '')}"
                        )

                        st.write(
                            f"**Problem Statement:** "
                            f"{project.get('problem_statement', '')}"
                        )

                        requirements = project.get(
                            "requirements",
                            []
                        )

                        if requirements:

                            st.write("**Requirements:**")

                            for requirement in requirements:
                                st.write(
                                    f"- {requirement}"
                                )

                        deliverables = project.get(
                            "deliverables",
                            []
                        )

                        if deliverables:

                            st.write("**Deliverables:**")

                            for deliverable in deliverables:
                                st.write(
                                    f"- {deliverable}"
                                )

                        st.write(
                            f"**Estimated Hours:** "
                            f"{project.get('estimated_hours', 0)}"
                        )

                        st.write(
                            f"**Why Relevant:** "
                            f"{project.get('why_relevant', '')}"
                        )


# =========================================================
# PROGRESS
# =========================================================

elif page == "Progress":

    st.header("📈 Progress")

    st.write(
        "Record completed learning activities and "
        "see how your skills are developing."
    )

    if not st.session_state.profile_created:

        st.info(
            "Complete your Learner Profile first."
        )

    elif not st.session_state.learning_objectives:

        st.info(
            "Generate Learning Objectives first."
        )

    else:

        st.subheader("➕ Record Learning Activity")

        with st.form("activity_form"):

            activity_type = st.selectbox(
                "Activity Type",
                [
                    "Learning",
                    "Practice",
                    "Project",
                    "Interview Practice",
                    "Assessment"
                ]
            )

            objective_skills = []

            for item in (
                st.session_state.learning_objectives
                .get("objectives", [])
            ):
                skill = item.get("skill", "")
                if skill and skill not in objective_skills:
                    objective_skills.append(skill)

            if not objective_skills:
                objective_skills = ["General"]

            skill = st.selectbox(
                "Skill",
                objective_skills
            )

            title = st.text_input(
                "Activity Title",
                placeholder="Example: Completed user research lesson"
            )

            status = st.selectbox(
                "Status",
                [
                    "Completed",
                    "In Progress",
                    "Incomplete"
                ]
            )

            col1, col2 = st.columns(2)

            with col1:
                estimated_minutes = st.number_input(
                    "Estimated Minutes",
                    min_value=0,
                    max_value=1000,
                    value=60
                )

            with col2:
                actual_minutes = st.number_input(
                    "Actual Minutes",
                    min_value=0,
                    max_value=1000,
                    value=60
                )

            score = st.number_input(
                "Score (optional, 0-100)",
                min_value=0,
                max_value=100,
                value=0
            )

            submitted = st.form_submit_button(
                "Save Activity"
            )

        if submitted:

            if not title.strip():

                st.warning(
                    "Please enter an activity title."
                )

            else:

                score_value = (
                    None
                    if score == 0
                    else score
                )

                record_activity(
                    activity_type=activity_type,
                    skill=skill,
                    title=title,
                    status=status,
                    estimated_minutes=estimated_minutes,
                    actual_minutes=actual_minutes,
                    score=score_value
                )

                st.success(
                    "Activity recorded successfully!"
                )

                st.rerun()

        activities = load_activities()

        try:

            progress = evaluate_progress(
                st.session_state.profile,
                st.session_state.learning_objectives,
                activities
            )

        except Exception as e:

            st.error(
                f"Could not evaluate progress: {e}"
            )
            progress = {}

        st.divider()

        st.subheader("📊 Current Progress")

        overall = progress.get(
            "overall_progress_percentage",
            0
        )

        st.metric(
            "Overall Progress",
            f"{overall}%"
        )

        st.progress(
            min(max(overall / 100, 0), 1)
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Skills Acquired",
                len(
                    progress.get(
                        "skills_acquired",
                        []
                    )
                )
            )

        with col2:
            st.metric(
                "Skills In Progress",
                len(
                    progress.get(
                        "skills_in_progress",
                        []
                    )
                )
            )

        with col3:
            st.metric(
                "Remaining Gaps",
                len(
                    progress.get(
                        "remaining_gaps",
                        []
                    )
                )
            )

        acquired = progress.get(
            "skills_acquired",
            []
        )

        if acquired:
            st.write("### ✅ Skills Acquired")
            for skill in acquired:
                st.write(f"- {skill}")

        in_progress = progress.get(
            "skills_in_progress",
            []
        )

        if in_progress:
            st.write("### 🔄 Skills In Progress")
            for skill in in_progress:
                st.write(f"- {skill}")

        remaining = progress.get(
            "remaining_gaps",
            []
        )

        if remaining:
            st.write("### 🎯 Remaining Gaps")
            for skill in remaining:
                st.write(f"- {skill}")

        st.divider()

        st.subheader("📚 Activity History")

        if not activities:

            st.info(
                "No learning activities recorded yet."
            )

        else:

            for index, activity in enumerate(
                reversed(activities),
                start=1
            ):

                with st.expander(
                    f"{index}. "
                    f"{activity.get('title', 'Activity')}"
                ):

                    st.write(
                        f"**Type:** "
                        f"{activity.get('activity_type', '')}"
                    )

                    st.write(
                        f"**Skill:** "
                        f"{activity.get('skill', '')}"
                    )

                    st.write(
                        f"**Status:** "
                        f"{activity.get('status', '')}"
                    )

                    st.write(
                        f"**Estimated:** "
                        f"{activity.get('estimated_minutes', 0)} minutes"
                    )

                    st.write(
                        f"**Actual:** "
                        f"{activity.get('actual_minutes', 0)} minutes"
                    )

                    activity_score = activity.get(
                        "score"
                    )

                    if activity_score is not None:
                        st.write(
                            f"**Score:** {activity_score}/100"
                        )


# =========================================================
# ADAPTIVE LEARNING
# =========================================================

elif page == "Adaptive Learning":

    st.header("🔄 Adaptive Learning")

    st.write(
        "EduPath automatically adjusts your learning plan "
        "based on your progress and areas where you are struggling."
    )

    profile = get_profile()
    learning_objectives = get_learning_objectives()
    weekly_plan = get_weekly_plan()

    if not profile:

        st.info(
            "Please create your Learner Profile first."
        )

    elif not learning_objectives:

        st.info(
            "Generate Learning Objectives first."
        )

    elif not weekly_plan:

        st.info(
            "Generate your Weekly Plan first."
        )

    else:

        activities = load_activities()

        try:

            progress = evaluate_progress(
                profile,
                learning_objectives,
                activities
            )

            struggles = detect_struggles(
                learning_objectives,
                activities
            )

            adaptive_plan = create_adaptive_plan(
                weekly_plan.get(
                    "weekly_plan",
                    []
                ),
                progress,
                struggles
            )

            st.success(
                "Your adaptive learning plan has been generated."
            )

            st.divider()

            st.subheader("📊 Current Learning Status")

            overall_progress = progress.get(
                "overall_progress_percentage",
                0
            )

            st.metric(
                "Overall Progress",
                f"{overall_progress}%"
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Skills Acquired",
                    len(
                        progress.get(
                            "skills_acquired",
                            []
                        )
                    )
                )

            with col2:
                st.metric(
                    "Skills In Progress",
                    len(
                        progress.get(
                            "skills_in_progress",
                            []
                        )
                    )
                )

            with col3:
                st.metric(
                    "Remaining Gaps",
                    len(
                        progress.get(
                            "remaining_gaps",
                            []
                        )
                    )
                )

            st.divider()

            st.subheader(
                "⚠️ Skills That Need More Practice"
            )

            struggling_skills = struggles.get(
                "struggling_skills",
                []
            )

            if struggling_skills:

                for struggle in struggling_skills:

                    skill = struggle.get(
                        "skill",
                        "Unknown"
                    )

                    severity = struggle.get(
                        "severity",
                        "Unknown"
                    )

                    reason = struggle.get(
                        "reason",
                        ""
                    )

                    with st.expander(
                        f"⚠️ {skill}"
                    ):

                        st.write(
                            f"**Severity:** {severity}"
                        )

                        if reason:
                            st.write(
                                f"**Reason:** {reason}"
                            )

            else:

                st.success(
                    "No significant struggling skills detected."
                )

            st.divider()

            st.subheader(
                "🧠 Updated Learning Plan"
            )

            if not adaptive_plan:

                st.info(
                    "No adaptive changes are required yet."
                )

            else:

                for day in adaptive_plan:

                    st.markdown("---")

                    st.subheader(
                        f"📅 {day.get('day', '')}"
                    )

                    tasks = day.get(
                        "tasks",
                        []
                    )

                    if not tasks:

                        st.write(
                            "No tasks scheduled."
                        )

                    else:

                        for index, task in enumerate(
                            tasks,
                            start=1
                        ):

                            st.write(
                                f"### Task {index}"
                            )

                            st.write(
                                f"**Skill:** "
                                f"{task.get('skill', '')}"
                            )

                            st.write(
                                f"**Objective:** "
                                f"{task.get('objective', '')}"
                            )

                            st.write(
                                f"**Activity:** "
                                f"{task.get('activity', '')}"
                            )

                            st.write(
                                f"**Task Type:** "
                                f"{task.get('task_type', '')}"
                            )

                            st.write(
                                f"**Estimated Time:** "
                                f"{task.get('estimated_minutes', 0)} minutes"
                            )

        except Exception as e:

            st.error(
                f"Could not create adaptive plan: {e}"
            )


# =========================================================
# REPORTS
# =========================================================

elif page == "Reports":

    st.header("📊 Progress Reports")

    st.write(
        "EduPath generates a learning progress report "
        "from your completed activities and current skill state."
    )

    profile = get_profile()
    learning_objectives = get_learning_objectives()

    if not profile:

        st.info(
            "Complete your Learner Profile first."
        )

    elif not learning_objectives:

        st.info(
            "Generate Learning Objectives first."
        )

    else:

        activities = load_activities()

        try:

            progress = evaluate_progress(
                profile,
                learning_objectives,
                activities
            )

            struggles = detect_struggles(
                learning_objectives,
                activities
            )

            report = generate_progress_report(
                profile,
                progress,
                struggles
            )

            st.success(
                "Progress report generated."
            )

            st.divider()

            st.subheader("📈 Overall Progress")

            overall = report.get(
                "overall_progress_percentage",
                progress.get(
                    "overall_progress_percentage",
                    0
                )
            )

            st.metric(
                "Overall Progress",
                f"{overall}%"
            )

            st.progress(
                min(max(overall / 100, 0), 1)
            )

            summary = report.get(
                "summary",
                ""
            )

            if summary:
                st.write("### 📝 Summary")
                st.write(summary)

            acquired = report.get(
                "skills_acquired",
                []
            )

            st.write("### ✅ Skills Acquired")

            if acquired:
                for skill in acquired:
                    st.write(f"- {skill}")
            else:
                st.write("No skills marked as acquired yet.")

            in_progress = report.get(
                "skills_in_progress",
                []
            )

            st.write("### 🔄 Skills In Progress")

            if in_progress:
                for skill in in_progress:
                    st.write(f"- {skill}")
            else:
                st.write("No skills currently marked as in progress.")

            gaps = report.get(
                "remaining_gaps",
                []
            )

            st.write("### 🎯 Remaining Gaps")

            if gaps:
                for gap in gaps:
                    st.write(f"- {gap}")
            else:
                st.write("No remaining gaps reported.")

            st.write("### ⚠️ Struggling Skills")

            report_struggles = report.get(
                "struggling_skills",
                []
            )

            if report_struggles:
                for struggle in report_struggles:
                    if isinstance(struggle, dict):
                        st.write(
                            f"- **{struggle.get('skill', 'Unknown')}**: "
                            f"{struggle.get('reason', '')}"
                        )
                    else:
                        st.write(f"- {struggle}")
            else:
                st.write("No significant struggles detected.")

            completed = report.get(
                "completed_activities",
                []
            )

            st.write("### 📚 Completed Activities")

            if completed:
                for activity in completed:
                    if isinstance(activity, dict):
                        st.write(
                            f"- {activity.get('title', 'Activity')}"
                        )
                    else:
                        st.write(f"- {activity}")
            else:
                st.write("No completed activities yet.")

            next_steps = report.get(
                "recommended_next_steps",
                []
            )

            st.write("### ➡️ Recommended Next Steps")

            if next_steps:
                for step in next_steps:
                    st.write(f"- {step}")
            else:
                st.write(
                    "Continue completing your learning activities "
                    "and update your progress."
                )

        except Exception as e:

            st.error(
                f"Could not generate progress report: {e}"
            )


# =========================================================
# ASK EDUPATH
# =========================================================

elif page == "Ask EduPath":

    st.header("💬 Ask EduPath")

    st.write(
        "Ask questions about your personalized "
        "learning journey."
    )

    profile = get_profile()
    learning_objectives = get_learning_objectives()

    if not profile:

        st.info(
            "Complete your Learner Profile first."
        )

    elif not learning_objectives:

        st.info(
            "Generate Learning Objectives first."
        )

    else:

        activities = load_activities()

        try:

            progress = evaluate_progress(
                profile,
                learning_objectives,
                activities
            )

            struggles = detect_struggles(
                learning_objectives,
                activities
            )

            progress_report = generate_progress_report(
                profile,
                progress,
                struggles
            )

        except Exception as e:

            st.error(
                f"Could not prepare your learning context: {e}"
            )

            progress = {}
            struggles = {}
            progress_report = {}

        st.subheader("💡 Example Questions")

        example_questions = [
            "What should I focus on next?",
            "Which skills am I currently struggling with?",
            "Why is this skill important for my target role?",
            "How much progress have I made?",
            "What should I practice this week?"
        ]

        for example in example_questions:
            st.write(f"- {example}")

        question = st.text_area(
            "What would you like to ask?",
            placeholder=(
                "Example: What should I focus on next?"
            )
        )

        if st.button("💬 Ask EduPath"):

            if not question.strip():

                st.warning(
                    "Please enter a question."
                )

            else:

                with st.spinner(
                    "EduPath is thinking..."
                ):

                    try:

                        answer = ask_edupath(
                            question,
                            profile,
                            progress,
                            struggles,
                            progress_report
                        )

                        if isinstance(answer, dict):
                            if answer.get("error"):
                                show_api_error(
                                    answer["error"]
                                )
                            else:
                                st.write(
                                    answer.get(
                                        "answer",
                                        str(answer)
                                    )
                                )
                        else:
                            st.write(answer)

                    except Exception as e:
                        show_api_error(e)


# =========================================================
# FOOTER
# =========================================================

st.sidebar.divider()

st.sidebar.caption(
    "EduPath • Personalized Learning & Skill Gap Agent"
)


# =========================================================
# GLOBAL FOOTER
# =========================================================

st.markdown(
    "<div class=\"edu-footer\">EduPath • Personalized learning powered by AI</div>",
    unsafe_allow_html=True
)


st.markdown("<div class='edu-footer'>✦ EduPath · Personalized learning, powered by AI</div>", unsafe_allow_html=True)
