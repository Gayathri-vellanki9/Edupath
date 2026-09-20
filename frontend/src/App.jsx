import { useState } from "react";
import {
  Home,
  Compass,
  Target,
  CalendarDays,
  TrendingUp,
  FileText,
  Bot,
  Sparkles,
  CheckCircle2,
  Clock3,
  BookOpen,
  ArrowRight,
  Send,
  Upload,
  Menu,
  X,
} from "lucide-react";

const API_URL = "https://edupath-2-195z.onrender.com";

const navItems = [
  { name: "Home", icon: Home },
  { name: "My Journey", icon: Compass },
  { name: "Skills", icon: Target },
  { name: "Plan", icon: CalendarDays },
  { name: "Progress", icon: TrendingUp },
  { name: "Reports", icon: FileText },
  { name: "AI Coach", icon: Bot },
];

/* =========================================================
   DEFAULT DATA
   Used before a resume is uploaded.
========================================================= */

const defaultSkills = [
  {
    name: "Product Strategy",
    current: 72,
    required: 90,
    priority: "High",
    reason:
      "Important for defining product direction, strategy and business outcomes.",
  },
  {
    name: "User Research",
    current: 55,
    required: 85,
    priority: "High",
    reason:
      "Helps understand customer needs, pain points and product opportunities.",
  },
  {
    name: "Product Analytics",
    current: 48,
    required: 80,
    priority: "Medium",
    reason:
      "Helps product managers measure product performance and make data-driven decisions.",
  },
  {
    name: "Communication",
    current: 68,
    required: 85,
    priority: "Medium",
    reason:
      "Important for communicating product decisions with cross-functional teams.",
  },
];

const activities = [
  {
    title: "Product Discovery Fundamentals",
    type: "Course",
    status: "Completed",
    time: "1h 20m",
  },
  {
    title: "User Research Case Study",
    type: "Practice",
    status: "In Progress",
    time: "45m",
  },
  {
    title: "Build an AI Resume Matcher",
    type: "Project",
    status: "Not Started",
    time: "3h",
  },
];

/* =========================================================
   API FUNCTIONS
========================================================= */

async function saveProfile(profile) {
  const response = await fetch(`${API_URL}/api/profile`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(profile),
  });

  if (!response.ok) {
    throw new Error("Profile save failed");
  }

  return response.json();
}


async function analyzeResume(file) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(
    `${API_URL}/api/analyze-document`,
    {
      method: "POST",
      body: formData,
    }
  );

  const data = await response.json();

  if (!response.ok || !data.success) {
    throw new Error(
      data.message || "Resume analysis failed"
    );
  }

  return data;
}


async function askEduPath(
  question,
  profile = {}
) {
  const response = await fetch(
    `${API_URL}/api/ask`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question,

        profile,

        progress: {},

        struggles: [],

        progress_report: {},
      }),
    }
  );

  if (!response.ok) {
    throw new Error(
      "AI Coach request failed"
    );
  }

  return response.json();
}


/* =========================================================
   MAIN APP
========================================================= */

function App() {
  const [activePage, setActivePage] =
    useState("Home");

  const [mobileMenu, setMobileMenu] =
    useState(false);

  /*
   * IMPORTANT:
   * Resume analysis is stored here so that
   * My Journey and Skills pages can both use it.
   */

  const [resumeData, setResumeData] =
    useState(null);

  const [profile, setProfile] =
    useState({
      career_goal: "Product Manager",

      target_role:
        "APM / Product Manager",

      current_skills:
        "Product Fundamentals, Python, Problem Solving, Communication, Figma",

      experience:
        "Beginner-level Product Management experience with an interest in AI-powered products and user-focused problem solving.",

      hours_per_week: 10,

      learning_preference:
        "Practical + Visual",
    });

  const [message, setMessage] =
    useState("");

  const [chatMessages, setChatMessages] =
    useState([
      {
        role: "assistant",

        text:
          "Hi! I'm your EduPath AI Coach. Ask me about your skills, learning plan, projects, or career.",
      },
    ]);


  const goTo = (page) => {
    setActivePage(page);

    setMobileMenu(false);

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };


  const updateProfile = (
    field,
    value
  ) => {
    setProfile((previous) => ({
      ...previous,
      [field]: value,
    }));
  };


  const handleResumeAnalyzed = (
    result
  ) => {
    setResumeData(result);

    /*
     * Update profile with skills detected
     * from the uploaded resume.
     */

    const analysis =
      result.document_analysis || {};

    const detectedSkills =
      analysis.skills || [];

    const detectedExperience =
      analysis.experience || [];

    const detectedTools =
      analysis.tools || [];


    setProfile((previous) => ({
      ...previous,

      current_skills:
        detectedSkills.length > 0
          ? detectedSkills.join(", ")
          : previous.current_skills,

      experience:
        detectedExperience.length > 0
          ? detectedExperience.join("\n")
          : previous.experience,
    }));


    console.log(
      "Resume analysis:",
      result
    );

    console.log(
      "Detected skills:",
      detectedSkills
    );

    console.log(
      "Detected tools:",
      detectedTools
    );
  };


  const sendMessage = async () => {
    const trimmed =
      message.trim();

    if (!trimmed) return;


    setChatMessages(
      (previous) => [
        ...previous,

        {
          role: "user",
          text: trimmed,
        },
      ]
    );

    setMessage("");


    try {
      const data =
        await askEduPath(
          trimmed,
          profile
        );


      setChatMessages(
        (previous) => [
          ...previous,

          {
            role: "assistant",

            text:
              data.answer ||
              "I could not generate an answer right now.",
          },
        ]
      );
    } catch (error) {
      console.error(error);


      setChatMessages(
        (previous) => [
          ...previous,

          {
            role: "assistant",

            text:
              "I couldn't connect to EduPath right now. Please check the backend.",
          },
        ]
      );
    }
  };


  return (
    <div className="app-shell">

      {/* =================================================
          TOP BAR
      ================================================= */}

      <header className="topbar">

        <div
          className="brand"
          onClick={() =>
            goTo("Home")
          }
        >

          <div className="brand-mark">
            <Sparkles size={18} />
          </div>

          <div>
            <div className="brand-name">
              EduPath
            </div>

            <div className="brand-subtitle">
              Personalized learning,
              powered by AI
            </div>
          </div>

        </div>


        <nav className="desktop-nav">

          {navItems.map(
            (item) => {

              const Icon =
                item.icon;

              return (
                <button
                  key={item.name}

                  className={`nav-item ${
                    activePage ===
                    item.name
                      ? "active"
                      : ""
                  }`}

                  onClick={() =>
                    goTo(
                      item.name
                    )
                  }
                >

                  <Icon size={16} />

                  <span>
                    {item.name}
                  </span>

                </button>
              );
            }
          )}

        </nav>


        <button
          className="mobile-menu-button"

          onClick={() =>
            setMobileMenu(
              !mobileMenu
            )
          }
        >

          {mobileMenu ? (
            <X size={22} />
          ) : (
            <Menu size={22} />
          )}

        </button>

      </header>


      {/* =================================================
          MOBILE NAV
      ================================================= */}

      {mobileMenu && (
        <div className="mobile-nav">

          {navItems.map(
            (item) => {

              const Icon =
                item.icon;

              return (
                <button
                  key={item.name}

                  className={`mobile-nav-item ${
                    activePage ===
                    item.name
                      ? "active"
                      : ""
                  }`}

                  onClick={() =>
                    goTo(
                      item.name
                    )
                  }
                >

                  <Icon size={18} />

                  {item.name}

                </button>
              );
            }
          )}

        </div>
      )}


      {/* =================================================
          PAGE CONTENT
      ================================================= */}

      <main className="main-content">

        {activePage ===
          "Home" && (
          <HomePage
            goTo={goTo}
            profile={profile}
            resumeData={resumeData}
          />
        )}


        {activePage ===
          "My Journey" && (
          <JourneyPage
            profile={profile}
            setProfile={setProfile}
            onResumeAnalyzed={
              handleResumeAnalyzed
            }
          />
        )}


        {activePage ===
          "Skills" && (
          <SkillsPage
            resumeData={resumeData}
            profile={profile}
          />
        )}


        {activePage ===
          "Plan" && (
          <PlanPage
            profile={profile}
            resumeData={resumeData}
          />
        )}


        {activePage ===
          "Progress" && (
          <ProgressPage
            resumeData={resumeData}
          />
        )}


        {activePage ===
          "Reports" && (
          <ReportsPage
            resumeData={resumeData}
            profile={profile}
          />
        )}


        {activePage ===
          "AI Coach" && (
          <CoachPage
            message={message}
            setMessage={setMessage}
            chatMessages={
              chatMessages
            }
            sendMessage={
              sendMessage
            }
          />
        )}

      </main>


      {/* =================================================
          FOOTER
      ================================================= */}

      <footer className="footer">

        <div>

          <strong>
            ✦ EduPath
          </strong>

          <span>
            {" "}
            Personalized
            learning for your
            career journey.
          </span>

        </div>

        <span>
          AI-powered •
          Skill-focused •
          Personalized
        </span>

      </footer>

    </div>
  );
}


/* =========================================================
   HOME PAGE
========================================================= */

function HomePage({
  goTo,
  profile,
  resumeData,
}) {

  const hasResume =
    Boolean(resumeData);


  return (
    <>

      <section className="hero">

        <div className="hero-content">

          <div className="eyebrow">

            <Sparkles size={15} />

            Your personalized
            learning journey

          </div>


          <h1>

            Build your path to{" "}

            <span>
              {profile.target_role ||
                "your career goal"}
              . ✨
            </span>

          </h1>


          <p>

            EduPath analyzes your
            current skills, identifies
            gaps, and creates a
            personalized learning path
            to help you reach your
            career goal.

          </p>


          <div className="hero-actions">

            <button
              className="primary-button"

              onClick={() =>
                goTo("Plan")
              }
            >

              Continue Learning

              <ArrowRight
                size={17}
              />

            </button>


            <button
              className="secondary-button"

              onClick={() =>
                goTo("Skills")
              }
            >

              View Skill Gaps

            </button>

          </div>

        </div>


        <div className="hero-progress-card">

          <div className="hero-progress-top">

            <div>

              <span className="small-label">
                Overall Progress
              </span>

              <strong>
                {hasResume
                  ? "Resume analyzed"
                  : "64%"}
              </strong>

            </div>


            <div className="progress-circle">

              <span>
                {hasResume
                  ? "✓"
                  : "64%"}
              </span>

            </div>

          </div>


          <div className="progress-track large">

            <div
              className="progress-fill"
              style={{
                width:
                  hasResume
                    ? "100%"
                    : "64%",
              }}
            />

          </div>


          <div className="progress-caption">

            <span>

              {hasResume
                ? "Your resume has been analyzed."
                : "Start by uploading your resume."}

            </span>

          </div>

        </div>

      </section>


      <section className="section">

        <SectionHeading
          title="Your learning at a glance"
          subtitle="A quick overview of your current EduPath journey."
        />


        <div className="metric-grid">

          <MetricCard
            icon={<Target />}
            label="Detected Skills"
            value={
              resumeData
                ?.document_analysis
                ?.skills
                ?.length ||
              profile.current_skills
                .split(",")
                .filter(Boolean)
                .length
            }
            description="Skills identified"
          />


          <MetricCard
            icon={
              <CheckCircle2 />
            }
            label="Completed"
            value="12"
            description="Activities completed"
          />


          <MetricCard
            icon={<Clock3 />}
            label="This Week"
            value="6.5h"
            description="Learning time"
          />


          <MetricCard
            icon={<BookOpen />}
            label="Target Role"
            value={
              profile.target_role
                ?.split("/")
                [0]
                ?.trim() ||
              "Goal"
            }
            description={
              profile.career_goal
            }
          />

        </div>

      </section>


      <section className="section">

        <SectionHeading
          title="Your learning journey"
          subtitle="Move through your personalized path step by step."
        />


        <div className="roadmap">

          <RoadmapItem
            number="01"
            title="Understand your profile"
            description="Analyze your experience, skills and career goal."
            status={
              resumeData
                ? "Completed"
                : "Current"
            }
          />


          <RoadmapItem
            number="02"
            title="Identify skill gaps"
            description="Understand the capabilities you need to develop."
            status={
              resumeData
                ? "Completed"
                : "Upcoming"
            }
          />


          <RoadmapItem
            number="03"
            title="Build your learning plan"
            description="Follow resources, practice activities and projects."
            status="Current"
          />


          <RoadmapItem
            number="04"
            title="Measure your progress"
            description="Track learning and adapt your plan continuously."
            status="Upcoming"
          />

        </div>

      </section>


      <section className="two-column">

        <div className="insight-card">

          <div className="card-icon purple">

            <Sparkles
              size={20}
            />

          </div>


          <div>

            <span className="small-label">
              AI INSIGHT
            </span>

            <h3>
              Resume-based learning
            </h3>

            <p>

              {resumeData
                ? "EduPath has detected skills from your uploaded resume. Visit the Skills page to explore your personalized skill profile."
                : "Upload your resume so EduPath can identify your actual skills and personalize your learning path."}

            </p>


            <button
              className="text-button"

              onClick={() =>
                goTo("Skills")
              }
            >

              Explore skills

              <ArrowRight
                size={16}
              />

            </button>

          </div>

        </div>


        <div className="next-action-card">

          <span className="small-label">
            NEXT ACTION
          </span>

          <h3>
            Upload or review your resume
          </h3>


          <div className="action-meta">

            <span>

              <FileText
                size={15}
              />

              Resume Analysis

            </span>

          </div>


          <button
            className="primary-button full"

            onClick={() =>
              goTo(
                "My Journey"
              )
            }
          >

            Go to My Journey

            <ArrowRight
              size={16}
            />

          </button>

        </div>

      </section>

    </>
  );
}


/* =========================================================
   JOURNEY PAGE
========================================================= */

function JourneyPage({
  profile,
  setProfile,
  onResumeAnalyzed,
}) {

  const [tab, setTab] =
    useState("profile");

  const [saving, setSaving] =
    useState(false);

  const [uploading, setUploading] =
    useState(false);

  const [saveMessage, setSaveMessage] =
    useState("");

  const [selectedFile, setSelectedFile] =
    useState(null);

  const [documentResult, setDocumentResult] =
    useState(null);


  const updateProfile = (
    field,
    value
  ) => {

    setProfile(
      (previous) => ({
        ...previous,
        [field]: value,
      })
    );

    setSaveMessage("");
  };


  const handleSaveProfile =
    async () => {

      try {

        setSaving(true);

        setSaveMessage("");

        await saveProfile(
          profile
        );

        setSaveMessage(
          "Profile saved successfully."
        );

      } catch (error) {

        console.error(error);

        setSaveMessage(
          "Could not save profile."
        );

      } finally {

        setSaving(false);

      }
    };


  const handleFileChange =
    async (event) => {

      const file =
        event.target.files?.[0];

      if (!file) return;


      setSelectedFile(file);

      setDocumentResult(null);

      setSaveMessage("");

      setUploading(true);


      try {

        const result =
          await analyzeResume(
            file
          );


        setDocumentResult(
          result
        );


        /*
         * Send the result to App.
         *
         * App stores it globally so
         * SkillsPage can use it.
         */

        onResumeAnalyzed(
          result
        );


        setSaveMessage(
          "Resume analyzed successfully. Skills were detected from your resume."
        );

      } catch (error) {

        console.error(
          "Resume upload error:",
          error
        );

        setSaveMessage(
          error.message ||
            "Could not analyze resume."
        );

      } finally {

        setUploading(false);

      }
    };


  const detectedSkills =
    documentResult
      ?.document_analysis
      ?.skills || [];


  const detectedTools =
    documentResult
      ?.document_analysis
      ?.tools || [];


  return (

    <PageHeader
      eyebrow="MY JOURNEY"
      title="Know your starting point."
      description="Manage your learner profile and documents that EduPath uses to personalize your learning path."
    >

      <div className="tabs">

        <button
          className={
            tab === "profile"
              ? "tab active"
              : "tab"
          }

          onClick={() =>
            setTab("profile")
          }
        >
          Learner Profile
        </button>


        <button
          className={
            tab === "documents"
              ? "tab active"
              : "tab"
          }

          onClick={() =>
            setTab("documents")
          }
        >
          Documents
        </button>

      </div>


      {tab === "profile" ? (

        <div className="content-card">

          <div className="card-heading">

            <div>

              <span className="small-label">
                PROFILE
              </span>

              <h2>
                Your learner profile
              </h2>

            </div>

            <span className="status-badge success">
              Profile Active
            </span>

          </div>


          <div className="form-grid">

            <EditableInputField
              label="Career Goal"
              value={
                profile.career_goal
              }
              onChange={(value) =>
                updateProfile(
                  "career_goal",
                  value
                )
              }
            />


            <EditableInputField
              label="Target Role"
              value={
                profile.target_role
              }
              onChange={(value) =>
                updateProfile(
                  "target_role",
                  value
                )
              }
            />


            <EditableInputField
              label="Learning Hours / Week"
              type="number"
              value={
                profile.hours_per_week
              }
              onChange={(value) =>
                updateProfile(
                  "hours_per_week",
                  Number(value)
                )
              }
            />


            <EditableInputField
              label="Learning Preference"
              value={
                profile.learning_preference
              }
              onChange={(value) =>
                updateProfile(
                  "learning_preference",
                  value
                )
              }
            />

          </div>


          <div className="profile-section">

            <label className="input-field">

              <span>
                Current Skills
              </span>

              <textarea
                value={
                  profile.current_skills
                }

                onChange={(event) =>
                  updateProfile(
                    "current_skills",
                    event.target.value
                  )
                }

                rows={4}
              />

            </label>

          </div>


          <div className="profile-section">

            <label className="input-field">

              <span>
                Experience
              </span>

              <textarea
                value={
                  profile.experience
                }

                onChange={(event) =>
                  updateProfile(
                    "experience",
                    event.target.value
                  )
                }

                rows={4}
              />

            </label>

          </div>


          <div className="profile-section">

            <span className="small-label">
              CURRENT SKILLS
            </span>


            <div className="chip-list">

              {profile.current_skills
                .split(",")
                .map(
                  (skill) =>
                    skill.trim()
                )
                .filter(Boolean)
                .map(
                  (skill) => (
                    <span
                      className="skill-chip"
                      key={skill}
                    >
                      {skill}
                    </span>
                  )
                )}

            </div>

          </div>


          <div className="profile-actions">

            <button
              className="primary-button"
              onClick={
                handleSaveProfile
              }
              disabled={saving}
            >

              {saving
                ? "Saving..."
                : "Save Profile"}

            </button>


            {saveMessage && (
              <span className="muted-text">
                {saveMessage}
              </span>
            )}

          </div>

        </div>

      ) : (

        <div className="content-card">

          <div className="card-heading">

            <div>

              <span className="small-label">
                DOCUMENTS
              </span>

              <h2>
                Your learning documents
              </h2>

            </div>

          </div>


          <div className="upload-box">

            <div className="upload-icon">

              <Upload size={24} />

            </div>


            <h3>
              Upload your resume
            </h3>


            <p>
              Upload your resume or
              profile document so
              EduPath can analyze your
              actual skills.
            </p>


            <label className="secondary-button file-button">

              <Upload size={17} />

              {uploading
                ? "Analyzing..."
                : selectedFile
                ? "Change File"
                : "Choose File"}


              <input
                type="file"
                accept=".pdf,.doc,.docx,.txt"
                onChange={
                  handleFileChange
                }
                hidden
                disabled={
                  uploading
                }
              />

            </label>


            {selectedFile && (

              <div className="document-row">

                <div className="document-icon">

                  <FileText
                    size={20}
                  />

                </div>


                <div>

                  <strong>
                    {selectedFile.name}
                  </strong>

                  <span>
                    {(
                      selectedFile.size /
                      1024
                    ).toFixed(1)}{" "}
                    KB
                  </span>

                </div>


                {uploading ? (

                  <span className="status-badge warning">
                    Analyzing
                  </span>

                ) : documentResult?.success ? (

                  <span className="status-badge success">
                    Analyzed
                  </span>

                ) : null}

              </div>

            )}


            {saveMessage && (

              <p className="muted-text">
                {saveMessage}
              </p>

            )}

          </div>


          {documentResult?.success && (

            <div className="content-card resume-result-card">

              <div className="card-heading">

                <div>

                  <span className="small-label">
                    RESUME ANALYSIS
                  </span>

                  <h2>
                    Skills detected from your resume
                  </h2>

                </div>

              </div>


              {detectedSkills.length >
              0 ? (

                <div className="chip-list">

                  {detectedSkills.map(
                    (skill) => (

                      <span
                        className="skill-chip"
                        key={skill}
                      >
                        {skill}
                      </span>

                    )
                  )}

                </div>

              ) : (

                <p className="muted-text">
                  No specific skills were detected.
                </p>

              )}


              {detectedTools.length >
                0 && (

                <>

                  <span className="small-label">
                    TOOLS
                  </span>

                  <div className="chip-list">

                    {detectedTools.map(
                      (tool) => (

                        <span
                          className="skill-chip"
                          key={tool}
                        >
                          {tool}
                        </span>

                      )
                    )}

                  </div>

                </>

              )}

            </div>

          )}

        </div>

      )}

    </PageHeader>
  );
}


/* =========================================================
   SKILLS PAGE
========================================================= */

function SkillsPage({
  resumeData,
  profile,
}) {

  const [tab, setTab] =
    useState("gaps");


  const documentAnalysis =
    resumeData
      ?.document_analysis;


  const skillGapAnalysis =
    resumeData
      ?.skill_gap_analysis;


  const detectedSkills =
    documentAnalysis
      ?.skills || [];


  const skillGaps =
    skillGapAnalysis
      ?.skill_gaps || [];


  /*
   * If a resume has been analyzed,
   * show REAL resume skills.
   *
   * Otherwise show default demo data.
   */

  const hasResume =
    detectedSkills.length >
    0;


  return (

    <PageHeader
      eyebrow="SKILLS"
      title="Turn gaps into capabilities."
      description="Understand the skills EduPath found in your resume and the capabilities relevant to your target role."
    >

      <div className="tabs">

        <button
          className={
            tab === "gaps"
              ? "tab active"
              : "tab"
          }

          onClick={() =>
            setTab("gaps")
          }
        >
          {hasResume
            ? "Resume Skills & Gaps"
            : "Skill Gaps"}
        </button>


        <button
          className={
            tab === "objectives"
              ? "tab active"
              : "tab"
          }

          onClick={() =>
            setTab("objectives")
          }
        >
          Learning Objectives
        </button>

      </div>


      {hasResume ? (

        <>

          {/* =================================================
              DETECTED RESUME SKILLS
          ================================================= */}

          <div className="content-card">

            <div className="card-heading">

              <div>

                <span className="small-label">
                  DETECTED FROM RESUME
                </span>

                <h2>
                  Your current skills
                </h2>

              </div>


              <span className="status-badge success">
                Resume Matched
              </span>

            </div>


            <p className="muted-text">

              These skills were identified
              directly from your uploaded
              resume.

            </p>


            <div className="chip-list">

              {detectedSkills.map(
                (skill) => (

                  <span
                    className="skill-chip"
                    key={skill}
                  >
                    {skill}
                  </span>

                )
              )}

            </div>

          </div>


          {/* =================================================
              SKILL GAPS
          ================================================= */}

          <div className="skill-list">

            {skillGaps.length >
            0 ? (

              skillGaps.map(
                (skill, index) => {

                  const priority =
                    skill.priority ||
                    "Medium";


                  const currentLevel =
                    skill.current_level ||
                    "Unknown";


                  const requiredLevel =
                    skill.required_level ||
                    "Intermediate";


                  return (

                    <div
                      className="skill-card"
                      key={
                        skill.skill ||
                        index
                      }
                    >

                      <div className="skill-card-header">

                        <div>

                          <h3>
                            {skill.skill}
                          </h3>

                          <span className="muted-text">

                            Gap:{" "}
                            {skill.gap ||
                              "Development needed"}

                          </span>

                        </div>


                        <span
                          className={`priority ${
                            priority ===
                            "High"
                              ? "high"
                              : "medium"
                          }`}
                        >
                          {priority} Priority
                        </span>

                      </div>


                      <div className="level-row">

                        <span>
                          Current level
                        </span>

                        <strong>
                          {currentLevel}
                        </strong>

                      </div>


                      <div className="skill-reason">

                        <strong>
                          Required level:
                        </strong>

                        <span>
                          {requiredLevel}
                        </span>

                      </div>


                      <div className="skill-reason">

                        <strong>
                          Why this matters:
                        </strong>

                        <span>
                          {skill.reason ||
                            "This skill is relevant to your target role."}
                        </span>

                      </div>


                      {skill.evidence &&
                        skill.evidence.length >
                          0 && (

                        <div className="skill-reason">

                          <strong>
                            Resume evidence:
                          </strong>

                          <span>
                            {skill.evidence.join(
                              " • "
                            )}
                          </span>

                        </div>

                      )}

                    </div>

                  );
                }
              )

            ) : (

              <div className="content-card">

                <h3>
                  No skill gaps available yet.
                </h3>

                <p className="muted-text">

                  EduPath detected your
                  resume skills, but no
                  skill-gap result was
                  returned.

                </p>

              </div>

            )}

          </div>

        </>

      ) : (

        /* =================================================
           DEFAULT DEMO SKILLS
        ================================================= */

        <div className="skill-list">

          {defaultSkills.map(
            (skill) => (

              <div
                className="skill-card"
                key={skill.name}
              >

                <div className="skill-card-header">

                  <div>

                    <h3>
                      {skill.name}
                    </h3>

                    <span className="muted-text">

                      Gap:{" "}
                      {skill.required -
                        skill.current}%

                    </span>

                  </div>


                  <span
                    className={`priority ${
                      skill.priority ===
                      "High"
                        ? "high"
                        : "medium"
                    }`}
                  >
                    {skill.priority} Priority
                  </span>

                </div>


                <div className="level-row">

                  <span>
                    Current level
                  </span>

                  <strong>
                    {skill.current}%
                  </strong>

                </div>


                <div className="progress-track">

                  <div
                    className="progress-fill"
                    style={{
                      width:
                        `${skill.current}%`,
                    }}
                  />

                </div>


                <div className="level-row">

                  <span>
                    Required level
                  </span>

                  <strong>
                    {skill.required}%
                  </strong>

                </div>


                <div className="skill-reason">

                  <strong>
                    Why this matters:
                  </strong>

                  <span>
                    {skill.reason}
                  </span>

                </div>

              </div>

            )
          )}

        </div>

      )}


      {/* =================================================
          LEARNING OBJECTIVES
      ================================================= */}

      {tab === "objectives" && (

        <div className="objective-grid">

          {hasResume &&
          skillGaps.length >
            0 ? (

            skillGaps.map(
              (skill, index) => (

                <ObjectiveCard
                  key={
                    skill.skill ||
                    index
                  }

                  title={
                    skill.gap ||
                    `Improve ${skill.skill}`
                  }

                  skill={
                    skill.skill
                  }

                  level={
                    `${skill.current_level || "Unknown"} → ${skill.required_level || "Intermediate"}`
                  }
                />

              )
            )

          ) : (

            <>
              <ObjectiveCard
                title="Conduct effective user interviews"
                skill="User Research"
                level="Beginner → Intermediate"
              />

              <ObjectiveCard
                title="Translate user needs into product decisions"
                skill="Product Strategy"
                level="Intermediate"
              />

              <ObjectiveCard
                title="Define and track product KPIs"
                skill="Product Analytics"
                level="Beginner → Intermediate"
              />

              <ObjectiveCard
                title="Communicate product decisions clearly"
                skill="Communication"
                level="Intermediate"
              />
            </>

          )}

        </div>

      )}

    </PageHeader>
  );
}


/* =========================================================
   PLAN PAGE
========================================================= */

function PlanPage({
  profile,
  resumeData,
}) {

  const [tab, setTab] =
    useState("resources");


  return (

    <PageHeader
      eyebrow="LEARNING PLAN"
      title="Your personalized action plan."
      description="Resources, weekly activities and practical projects generated around your skill gaps."
    >

      <div className="tabs">

        <button
          className={
            tab === "resources"
              ? "tab active"
              : "tab"
          }
          onClick={() =>
            setTab("resources")
          }
        >
          Resources
        </button>


        <button
          className={
            tab === "weekly"
              ? "tab active"
              : "tab"
          }
          onClick={() =>
            setTab("weekly")
          }
        >
          Weekly Plan
        </button>


        <button
          className={
            tab === "projects"
              ? "tab active"
              : "tab"
          }
          onClick={() =>
            setTab("projects")
          }
        >
          Practice & Projects
        </button>

      </div>


      {tab === "resources" && (

        <div className="resource-grid">

          <ResourceCard
            type="COURSE"
            title={
              profile.target_role
                ? `${profile.target_role} Fundamentals`
                : "Career Fundamentals"
            }
            description="Build the core capabilities needed for your target role."
            time="3 hours"
          />


          <ResourceCard
            type="PRACTICE"
            title="Skill Gap Practice"
            description={
              resumeData
                ? "Practice the capabilities identified from your resume and skill-gap analysis."
                : "Upload your resume to generate personalized practice."
            }
            time="1 hour"
          />


          <ResourceCard
            type="PROJECT"
            title="Portfolio Project"
            description="Build a practical project that demonstrates your career skills."
            time="3 hours"
          />

        </div>

      )}


      {tab === "weekly" && (

        <div className="weekly-plan">

          <PlanDay
            day="MON"
            title="Core Skill Learning"
            time="1.5h"
            status="Done"
          />

          <PlanDay
            day="TUE"
            title="Skill Gap Practice"
            time="1.5h"
            status="Done"
          />

          <PlanDay
            day="WED"
            title="Case Study Practice"
            time="2h"
            status="Today"
          />

          <PlanDay
            day="THU"
            title="Analytics & Measurement"
            time="1h"
            status="Upcoming"
          />

          <PlanDay
            day="FRI"
            title="Portfolio Project"
            time="2h"
            status="Upcoming"
          />

        </div>

      )}


      {tab === "projects" && (

        <div className="project-grid">

          <ProjectCard
            title="AI Resume & Job Matcher"
            description="Build a product that analyzes resumes against job descriptions and identifies skill gaps."
            skills="AI • Product Thinking • UX"
          />


          <ProjectCard
            title="AI Mood-Based Coffee Machine"
            description="Design an intelligent coffee experience that adapts recommendations based on user mood."
            skills="User Research • Hardware • AI"
          />


          <ProjectCard
            title="Career Skill Gap Analyzer"
            description="Build a system that identifies skills from resumes and recommends a personalized learning path."
            skills="AI • Data • Product"
          />

        </div>

      )}

    </PageHeader>
  );
}


/* =========================================================
   PROGRESS PAGE
========================================================= */

function ProgressPage({
  resumeData,
}) {

  const detectedSkills =
    resumeData
      ?.document_analysis
      ?.skills || [];


  const skillCount =
    detectedSkills.length;


  return (

    <PageHeader
      eyebrow="PROGRESS"
      title="See how far you've come."
      description="Track activities, skill development and the areas that need more attention."
    >

      <div className="metric-grid">

        <MetricCard
          icon={
            <TrendingUp />
          }
          label="Overall Progress"
          value="64%"
          description="Across your learning path"
        />


        <MetricCard
          icon={
            <CheckCircle2 />
          }
          label="Detected Skills"
          value={
            skillCount ||
            8
          }
          description="Skills identified"
        />


        <MetricCard
          icon={
            <Clock3 />
          }
          label="Learning Time"
          value="18.5h"
          description="Total tracked time"
        />


        <MetricCard
          icon={<Target />}
          label="Remaining Gaps"
          value={
            resumeData
              ?.skill_gap_analysis
              ?.skill_gaps
              ?.length ||
            4
          }
          description="Areas to improve"
        />

      </div>


      <div className="content-card">

        <div className="card-heading">

          <div>

            <span className="small-label">
              RESUME SKILLS
            </span>

            <h2>
              Your capabilities
            </h2>

          </div>

        </div>


        {detectedSkills.length >
        0 ? (

          <div className="chip-list">

            {detectedSkills.map(
              (skill) => (

                <span
                  className="skill-chip"
                  key={skill}
                >
                  {skill}
                </span>

              )
            )}

          </div>

        ) : (

          <div className="progress-skill-list">

            {defaultSkills.map(
              (skill) => (

                <div
                  className="progress-skill"
                  key={skill.name}
                >

                  <div>

                    <span>
                      {skill.name}
                    </span>

                    <strong>
                      {skill.current}%
                    </strong>

                  </div>


                  <div className="progress-track">

                    <div
                      className="progress-fill"
                      style={{
                        width:
                          `${skill.current}%`,
                      }}
                    />

                  </div>

                </div>

              )
            )}

          </div>

        )}

      </div>


      <div className="content-card">

        <div className="card-heading">

          <div>

            <span className="small-label">
              ACTIVITY HISTORY
            </span>

            <h2>
              Recent learning
            </h2>

          </div>

        </div>


        <div className="activity-list">

          {activities.map(
            (activity) => (

              <div
                className="activity-row"
                key={activity.title}
              >

                <div className="activity-icon">

                  <BookOpen
                    size={18}
                  />

                </div>


                <div className="activity-info">

                  <strong>
                    {activity.title}
                  </strong>

                  <span>
                    {activity.type} •{" "}
                    {activity.time}
                  </span>

                </div>


                <span
                  className={`status-badge ${
                    activity.status ===
                    "Completed"
                      ? "success"
                      : activity.status ===
                        "In Progress"
                      ? "warning"
                      : "neutral"
                  }`}
                >
                  {activity.status}
                </span>

              </div>

            )
          )}

        </div>

      </div>


      <div className="adaptive-card">

        <div className="card-icon purple">

          <Sparkles
            size={20}
          />

        </div>


        <div>

          <span className="small-label">
            ADAPTIVE LEARNING
          </span>

          <h2>
            Your plan can evolve with you.
          </h2>

          <p>
            EduPath can detect
            struggling areas and
            adjust your upcoming
            activities based on your
            progress.
          </p>

        </div>


        <button className="primary-button">

          View Adaptive Plan

          <ArrowRight
            size={16}
          />

        </button>

      </div>

    </PageHeader>
  );
}


/* =========================================================
   REPORTS PAGE
========================================================= */

function ReportsPage({
  resumeData,
  profile,
}) {

  const detectedSkills =
    resumeData
      ?.document_analysis
      ?.skills || [];


  const skillGaps =
    resumeData
      ?.skill_gap_analysis
      ?.skill_gaps || [];


  return (

    <PageHeader
      eyebrow="REPORTS"
      title="Your learning report."
      description="A clear snapshot of your resume skills, development areas and learning journey."
    >

      <div className="report-hero">

        <div>

          <span className="small-label">
            TARGET ROLE
          </span>

          <div className="report-score">
            {profile.target_role}
          </div>

          <p>

            {detectedSkills.length > 0
              ? `EduPath identified ${detectedSkills.length} skills from your resume.`
              : "Upload your resume to generate a personalized report."}

          </p>

        </div>


        <div className="report-circle">
          {detectedSkills.length ||
            0}
        </div>

      </div>


      <div className="report-grid">

        <ReportCard
          title="Resume Skills"
          count={
            detectedSkills.length ||
            0
          }
          items={
            detectedSkills.slice(
              0,
              5
            )
          }
        />


        <ReportCard
          title="Skill Gaps"
          count={
            skillGaps.length ||
            0
          }
          items={
            skillGaps
              .slice(0, 5)
              .map(
                (item) =>
                  item.skill
              )
          }
        />


        <ReportCard
          title="Tools"
          count={
            resumeData
              ?.document_analysis
              ?.tools
              ?.length ||
            0
          }
          items={
            resumeData
              ?.document_analysis
              ?.tools
              ?.slice(
                0,
                5
              ) || []
          }
        />

      </div>


      <div className="content-card">

        <div className="card-heading">

          <div>

            <span className="small-label">
              NEXT STEPS
            </span>

            <h2>
              Recommended focus
            </h2>

          </div>

        </div>


        <div className="next-step-list">

          {skillGaps.length >
          0 ? (

            skillGaps
              .slice(0, 3)
              .map(
                (item, index) => (

                  <NextStep
                    key={
                      item.skill
                    }
                    number={`0${
                      index + 1
                    }`}
                    title={
                      item.gap ||
                      `Improve ${item.skill}`
                    }
                  />

                )
              )

          ) : (

            <>
              <NextStep
                number="01"
                title="Upload your resume"
              />

              <NextStep
                number="02"
                title="Review your detected skills"
              />

              <NextStep
                number="03"
                title="Start your personalized learning plan"
              />
            </>

          )}

        </div>

      </div>

    </PageHeader>
  );
}


/* =========================================================
   AI COACH
========================================================= */

function CoachPage({
  message,
  setMessage,
  chatMessages,
  sendMessage,
}) {

  return (

    <PageHeader
      eyebrow="AI COACH"
      title="Your personal learning coach."
      description="Ask questions about your learning path, skills, projects, case studies or career."
    >

      <div className="coach-layout">

        <div className="coach-sidebar">

          <div className="coach-profile">

            <div className="coach-avatar">

              <Bot size={24} />

            </div>


            <div>

              <strong>
                EduPath Coach
              </strong>

              <span>
                AI Learning Assistant
              </span>

            </div>

          </div>


          <div className="coach-suggestion">

            <span>
              TRY ASKING
            </span>

            <button>
              What should I learn this week?
            </button>

            <button>
              What skills are important for my target role?
            </button>

            <button>
              Give me a case study.
            </button>

            <button>
              Review my learning progress.
            </button>

          </div>

        </div>


        <div className="chat-card">

          <div className="chat-header">

            <div>

              <strong>
                Ask EduPath
              </strong>

              <span>
                Your learning context is available to the coach.
              </span>

            </div>


            <span className="online-dot">
              Online
            </span>

          </div>


          <div className="chat-messages">

            {chatMessages.map(
              (chat, index) => (

                <div
                  className={`chat-row ${
                    chat.role ===
                    "user"
                      ? "user"
                      : "assistant"
                  }`}
                  key={index}
                >

                  <div className="chat-bubble">
                    {chat.text}
                  </div>

                </div>

              )
            )}

          </div>


          <div className="chat-input">

            <input
              value={message}
              onChange={(
                event
              ) =>
                setMessage(
                  event.target.value
                )
              }

              onKeyDown={(
                event
              ) => {

                if (
                  event.key ===
                  "Enter"
                ) {
                  sendMessage();
                }

              }}

              placeholder="Ask your learning coach..."
            />


            <button
              onClick={
                sendMessage
              }
            >

              <Send size={18} />

            </button>

          </div>

        </div>

      </div>

    </PageHeader>
  );
}


/* =========================================================
   SHARED COMPONENTS
========================================================= */

function PageHeader({
  eyebrow,
  title,
  description,
  children,
}) {

  return (

    <section className="page">

      <div className="page-header">

        <span className="eyebrow">
          {eyebrow}
        </span>

        <h1>
          {title}
        </h1>

        <p>
          {description}
        </p>

      </div>


      {children}

    </section>
  );
}


function SectionHeading({
  title,
  subtitle,
}) {

  return (

    <div className="section-heading">

      <div>

        <h2>
          {title}
        </h2>

        <p>
          {subtitle}
        </p>

      </div>

    </div>
  );
}


function MetricCard({
  icon,
  label,
  value,
  description,
}) {

  return (

    <div className="metric-card">

      <div className="metric-icon">
        {icon}
      </div>

      <span className="small-label">
        {label}
      </span>

      <strong className="metric-value">
        {value}
      </strong>

      <span className="muted-text">
        {description}
      </span>

    </div>
  );
}


function RoadmapItem({
  number,
  title,
  description,
  status,
}) {

  return (

    <div
      className={`roadmap-item ${status.toLowerCase()}`}
    >

      <div className="roadmap-number">
        {number}
      </div>


      <div className="roadmap-content">

        <div className="roadmap-title-row">

          <h3>
            {title}
          </h3>

          <span className="status-badge">
            {status}
          </span>

        </div>


        <p>
          {description}
        </p>

      </div>

    </div>
  );
}


function EditableInputField({
  label,
  value,
  onChange,
  type = "text",
}) {

  return (

    <label className="input-field">

      <span>
        {label}
      </span>

      <input
        type={type}
        value={value}
        onChange={(event) =>
          onChange(
            event.target.value
          )
        }
      />

    </label>
  );
}


function ObjectiveCard({
  title,
  skill,
  level,
}) {

  return (

    <div className="objective-card">

      <div className="objective-icon">

        <Target size={20} />

      </div>


      <span className="small-label">
        {skill}
      </span>


      <h3>
        {title}
      </h3>


      <span className="level-badge">
        {level}
      </span>

    </div>
  );
}


function ResourceCard({
  type,
  title,
  description,
  time,
}) {

  return (

    <div className="resource-card">

      <div className="resource-top">

        <span className="type-badge">
          {type}
        </span>


        <span className="time">

          <Clock3 size={14} />

          {time}

        </span>

      </div>


      <h3>
        {title}
      </h3>


      <p>
        {description}
      </p>


      <button className="text-button">

        Open resource

        <ArrowRight
          size={16}
        />

      </button>

    </div>
  );
}


function PlanDay({
  day,
  title,
  time,
  status,
}) {

  return (

    <div className="plan-day">

      <div className="day-label">
        {day}
      </div>


      <div className="day-content">

        <strong>
          {title}
        </strong>

        <span>

          <Clock3 size={14} />

          {time}

        </span>

      </div>


      <span
        className={`status-badge ${
          status === "Done"
            ? "success"
            : status === "Today"
            ? "warning"
            : "neutral"
        }`}
      >
        {status}
      </span>

    </div>
  );
}


function ProjectCard({
  title,
  description,
  skills,
}) {

  return (

    <div className="project-card">

      <div className="project-icon">

        <Sparkles
          size={20}
        />

      </div>


      <span className="small-label">
        PRACTICAL PROJECT
      </span>


      <h3>
        {title}
      </h3>


      <p>
        {description}
      </p>


      <span className="project-skills">
        {skills}
      </span>


      <button className="primary-button full">

        Start Project

        <ArrowRight
          size={16}
        />

      </button>

    </div>
  );
}


function ReportCard({
  title,
  count,
  items = [],
}) {

  return (

    <div className="report-card">

      <div className="report-card-top">

        <span className="small-label">
          {title}
        </span>

        <strong>
          {count}
        </strong>

      </div>


      <div className="report-items">

        {items.length > 0 ? (

          items.map(
            (item) => (

              <div key={item}>

                <CheckCircle2
                  size={15}
                />

                <span>
                  {item}
                </span>

              </div>

            )
          )

        ) : (

          <span className="muted-text">
            No data available yet.
          </span>

        )}

      </div>

    </div>
  );
}


function NextStep({
  number,
  title,
}) {

  return (

    <div className="next-step">

      <span className="next-step-number">
        {number}
      </span>


      <strong>
        {title}
      </strong>


      <ArrowRight
        size={17}
      />

    </div>
  );
}


export default App;