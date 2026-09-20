import { useState } from "react";
import {
  Home,
  UserRound,
  Target,
  CalendarDays,
  TrendingUp,
  FileText,
  Bot,
  Menu,
  X,
  ArrowRight,
  CheckCircle2,
  Clock3,
  BookOpen,
  Sparkles,
  Upload,
  Send,
  CircleAlert,
  ChevronRight,
  Brain,
  BriefcaseBusiness,
  BarChart3,
  Lightbulb,
} from "lucide-react";

const API_URL = "http://localhost:8000";

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
    throw new Error("Failed to save profile");
  }

  return response.json();
}

async function askEduPath(question) {
  const response = await fetch(`${API_URL}/api/ask`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      question,

      profile: {
        career_goal: "Product Manager",
        target_role: "APM / Product Manager",
        current_skills:
          "Product Fundamentals, Python, Problem Solving, Communication, Figma",
        experience:
          "Beginner-level Product Management experience with an interest in AI-powered products and user-focused problem solving.",
        hours_per_week: 10,
        learning_preference: "Practical + Visual",
      },

      progress: {
        overall_progress: 62,
        completed_activities: 7,
        weekly_hours: 10,
      },

      struggles: [],

      progress_report: {
        overall_progress: 62,
      },
    }),
  });

  if (!response.ok) {
    throw new Error("AI Coach request failed");
  }

  return response.json();
}

/* =========================================================
   NAVIGATION
========================================================= */

const navItems = [
  { id: "home", label: "Home", icon: Home },
  { id: "journey", label: "My Journey", icon: UserRound },
  { id: "skills", label: "Skills", icon: Target },
  { id: "plan", label: "Plan", icon: CalendarDays },
  { id: "progress", label: "Progress", icon: TrendingUp },
  { id: "reports", label: "Reports", icon: FileText },
  { id: "coach", label: "AI Coach", icon: Bot },
];

/* =========================================================
   SAMPLE DATA
========================================================= */

const skills = [
  {
    name: "Product Management",
    current: 70,
    required: 90,
    gap: 20,
    priority: "High",
    reason: "Core skill for your target role.",
  },
  {
    name: "User Research",
    current: 45,
    required: 85,
    gap: 40,
    priority: "High",
    reason: "Important for product discovery.",
  },
  {
    name: "Data Analysis",
    current: 40,
    required: 75,
    gap: 35,
    priority: "Medium",
    reason: "Useful for product decisions.",
  },
  {
    name: "Figma / UI-UX",
    current: 55,
    required: 70,
    gap: 15,
    priority: "Medium",
    reason: "Helps communicate product ideas.",
  },
  {
    name: "Python",
    current: 60,
    required: 65,
    gap: 5,
    priority: "Low",
    reason: "Supporting technical skill.",
  },
];

const weeklyPlan = [
  {
    day: "Monday",
    topic: "User Research",
    task: "Learn primary vs secondary research",
    time: "1.5 hrs",
  },
  {
    day: "Tuesday",
    topic: "User Research",
    task: "Practice creating interview questions",
    time: "1.5 hrs",
  },
  {
    day: "Wednesday",
    topic: "Product Strategy",
    task: "Study product vision and strategy",
    time: "2 hrs",
  },
  {
    day: "Thursday",
    topic: "Case Study",
    task: "Solve a product prioritization case",
    time: "2 hrs",
  },
  {
    day: "Friday",
    topic: "Figma",
    task: "Create a simple product screen",
    time: "1.5 hrs",
  },
];

const resources = [
  {
    title: "Product Management Fundamentals",
    type: "Course",
    level: "Beginner",
    time: "3 hrs",
  },
  {
    title: "User Research Basics",
    type: "Article",
    level: "Beginner",
    time: "30 min",
  },
  {
    title: "Product Case Studies",
    type: "Practice",
    level: "Intermediate",
    time: "1 hr",
  },
];

const projects = [
  {
    title: "AI Mood-Based Smart Coffee Machine",
    description:
      "Design an AI-powered coffee machine that adapts coffee recommendations to the user's mood.",
    skills: ["User Research", "Product Thinking", "AI"],
  },
  {
    title: "AI Resume & JD Matcher",
    description:
      "Build a product that compares a resume with a job description and identifies skill gaps.",
    skills: ["AI", "Product Strategy", "Data"],
  },
];

/* =========================================================
   MAIN APP
========================================================= */

function App() {
  const [activePage, setActivePage] = useState("home");
  const [mobileMenu, setMobileMenu] = useState(false);

  const navigate = (page) => {
    setActivePage(page);
    setMobileMenu(false);

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  return (
    <div className="app-shell">
      {/* NAVBAR */}

      <header className="top-navbar">
        <div
          className="brand"
          onClick={() => navigate("home")}
        >
          <div className="brand-icon">
            <Sparkles size={18} />
          </div>

          <span>EduPath</span>
        </div>

        <nav className="desktop-nav">
          {navItems.map((item) => {
            const Icon = item.icon;

            return (
              <button
                key={item.id}
                className={`nav-item ${
                  activePage === item.id ? "active" : ""
                }`}
                onClick={() => navigate(item.id)}
              >
                <Icon size={17} />
                {item.label}
              </button>
            );
          })}
        </nav>

        <button
          className="mobile-menu-button"
          onClick={() => setMobileMenu(!mobileMenu)}
        >
          {mobileMenu ? (
            <X size={22} />
          ) : (
            <Menu size={22} />
          )}
        </button>
      </header>

      {/* MOBILE NAV */}

      {mobileMenu && (
        <div className="mobile-nav">
          {navItems.map((item) => {
            const Icon = item.icon;

            return (
              <button
                key={item.id}
                className={`mobile-nav-item ${
                  activePage === item.id ? "active" : ""
                }`}
                onClick={() => navigate(item.id)}
              >
                <Icon size={18} />
                {item.label}
              </button>
            );
          })}
        </div>
      )}

      {/* PAGE CONTENT */}

      <main className="main-content">
        {activePage === "home" && (
          <HomePage navigate={navigate} />
        )}

        {activePage === "journey" && <JourneyPage />}

        {activePage === "skills" && <SkillsPage />}

        {activePage === "plan" && <PlanPage />}

        {activePage === "progress" && <ProgressPage />}

        {activePage === "reports" && <ReportsPage />}

        {activePage === "coach" && <CoachPage />}
      </main>
    </div>
  );
}

/* =========================================================
   HOME PAGE
========================================================= */

function HomePage({ navigate }) {
  return (
    <>
      <section className="hero-section">
        <div className="hero-content">
          <div className="eyebrow">
            <Sparkles size={15} />
            Personalized learning journey
          </div>

          <h1>
            Build your path to
            <span> Product Manager.</span> ✨
          </h1>

          <p>
            EduPath analyzes your skills, identifies gaps,
            creates a learning roadmap, and adapts your
            journey as you progress.
          </p>

          <div className="hero-actions">
            <button
              className="primary-button"
              onClick={() => navigate("plan")}
            >
              Continue Learning
              <ArrowRight size={17} />
            </button>

            <button
              className="secondary-button"
              onClick={() => navigate("skills")}
            >
              View Skill Gaps
            </button>
          </div>
        </div>

        <div className="hero-card">
          <div className="hero-card-top">
            <span>Overall Progress</span>
            <span>62%</span>
          </div>

          <div className="large-progress">
            <div style={{ width: "62%" }} />
          </div>

          <div className="hero-card-bottom">
            <div>
              <strong>7</strong>
              <span>Activities</span>
            </div>

            <div>
              <strong>10h</strong>
              <span>This week</span>
            </div>

            <div>
              <strong>4</strong>
              <span>Skills improved</span>
            </div>
          </div>
        </div>
      </section>

      <section className="section">
        <SectionHeader
          title="Your learning dashboard"
          subtitle="Everything you need for your Product Management journey."
        />

        <div className="metric-grid">
          <MetricCard
            icon={TrendingUp}
            title="Overall Progress"
            value="62%"
            subtitle="+8% this week"
          />

          <MetricCard
            icon={Target}
            title="Skill Gaps"
            value="5"
            subtitle="2 high priority"
          />

          <MetricCard
            icon={CheckCircle2}
            title="Completed"
            value="7"
            subtitle="Activities"
          />

          <MetricCard
            icon={Clock3}
            title="Learning Hours"
            value="10h"
            subtitle="This week"
          />
        </div>
      </section>

      <section className="two-column-grid section">
        <div className="card">
          <SectionHeader
            title="Your roadmap"
            subtitle="Recommended learning sequence"
          />

          <RoadmapItem
            number="01"
            title="Product Fundamentals"
            status="Completed"
          />

          <RoadmapItem
            number="02"
            title="User Research"
            status="In Progress"
          />

          <RoadmapItem
            number="03"
            title="Product Case Studies"
            status="Next"
          />

          <RoadmapItem
            number="04"
            title="Figma & UI/UX"
            status="Upcoming"
          />
        </div>

        <div className="card insight-card">
          <div className="card-icon purple">
            <Brain size={20} />
          </div>

          <span className="small-label">
            AI INSIGHT
          </span>

          <h3>
            Your next focus should be User Research.
          </h3>

          <p>
            Your current skill gap suggests that improving
            user research will strengthen your product
            discovery and case-study performance.
          </p>

          <button
            className="text-button"
            onClick={() => navigate("plan")}
          >
            View recommended plan
            <ArrowRight size={16} />
          </button>
        </div>
      </section>

      <section className="next-action-card">
        <div>
          <span className="small-label">
            NEXT ACTION
          </span>

          <h2>
            Practice creating 5 user interview questions.
          </h2>

          <p>Estimated time: 30 minutes</p>
        </div>

        <button
          className="primary-button"
          onClick={() => navigate("plan")}
        >
          Start
          <ArrowRight size={17} />
        </button>
      </section>
    </>
  );
}

/* =========================================================
   MY JOURNEY
========================================================= */

function JourneyPage() {
  const [profile, setProfile] = useState({
    career_goal: "Product Manager",
    target_role: "APM / Product Manager",

    current_skills:
      "Product Fundamentals, Python, Problem Solving, Communication, Figma",

    experience:
      "Beginner-level Product Management experience with an interest in AI-powered products and user-focused problem solving.",

    hours_per_week: 10,

    learning_preference: "Practical + Visual",
  });

  const [saving, setSaving] = useState(false);

  const [saveMessage, setSaveMessage] =
    useState("");

  const [selectedFile, setSelectedFile] =
    useState(null);

  /* UPDATE PROFILE */

  const updateProfile = (field, value) => {
    setProfile((previous) => ({
      ...previous,
      [field]: value,
    }));

    setSaveMessage("");
  };

  /* SAVE PROFILE */

  const handleSaveProfile = async () => {
    try {
      setSaving(true);
      setSaveMessage("");

      await saveProfile(profile);

      setSaveMessage(
        "Profile saved successfully."
      );
    } catch (error) {
      console.error(error);

      setSaveMessage(
        "Could not save profile. Make sure the FastAPI backend is running."
      );
    } finally {
      setSaving(false);
    }
  };

  /* FILE SELECT */

  const handleFileChange = (event) => {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    setSelectedFile(file);
  };

  return (
    <>
      <PageHeader
        eyebrow="MY JOURNEY"
        title="Your learning journey"
        subtitle="Manage your profile, documents, and learning preferences."
      />

      <section className="two-column-grid">
        {/* PROFILE */}

        <div className="card">
          <div className="card-header-row">
            <div>
              <span className="small-label">
                LEARNER PROFILE
              </span>

              <h2>
                Personal learning profile
              </h2>
            </div>

            <div className="card-icon purple">
              <UserRound size={20} />
            </div>
          </div>

          <div className="form-grid">
            {/* CAREER GOAL */}

            <InputField
              label="Career Goal"
              value={profile.career_goal}
              onChange={(value) =>
                updateProfile(
                  "career_goal",
                  value
                )
              }
            />

            {/* TARGET ROLE */}

            <InputField
              label="Target Role"
              value={profile.target_role}
              onChange={(value) =>
                updateProfile(
                  "target_role",
                  value
                )
              }
            />

            {/* HOURS */}

            <InputField
              label="Learning Hours / Week"
              type="number"
              value={profile.hours_per_week}
              onChange={(value) =>
                updateProfile(
                  "hours_per_week",
                  Number(value)
                )
              }
            />

            {/* PREFERENCE */}

            <InputField
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

          {/* CURRENT SKILLS */}

          <div className="full-width-field">
            <label className="input-field">
              <span>Current Skills</span>

              <textarea
                value={
                  profile.current_skills
                }
                onChange={(e) =>
                  updateProfile(
                    "current_skills",
                    e.target.value
                  )
                }
                rows={3}
              />
            </label>
          </div>

          {/* EXPERIENCE */}

          <div className="full-width-field">
            <label className="input-field">
              <span>Experience</span>

              <textarea
                value={profile.experience}
                onChange={(e) =>
                  updateProfile(
                    "experience",
                    e.target.value
                  )
                }
                rows={4}
              />
            </label>
          </div>

          {/* SAVE */}

          <div className="save-profile-row">
            <button
              className="primary-button"
              onClick={handleSaveProfile}
              disabled={saving}
            >
              {saving
                ? "Saving..."
                : "Save Profile"}
            </button>

            {saveMessage && (
              <span
                className={`save-message ${
                  saveMessage.includes(
                    "successfully"
                  )
                    ? "success"
                    : "error"
                }`}
              >
                {saveMessage}
              </span>
            )}
          </div>
        </div>

        {/* DOCUMENTS */}

        <div className="card">
          <div className="card-header-row">
            <div>
              <span className="small-label">
                DOCUMENTS
              </span>

              <h2>Your documents</h2>
            </div>

            <div className="card-icon purple">
              <FileText size={20} />
            </div>
          </div>

          {/* REAL FILE UPLOAD */}

          <div className="upload-box">
            <div className="upload-icon">
              <Upload size={22} />
            </div>

            <h3>Upload your resume</h3>

            <p>
              Upload your resume or profile
              document so EduPath can analyze
              your current skills.
            </p>

            <label className="secondary-button file-button">
              <Upload size={16} />

              {selectedFile
                ? "Change File"
                : "Choose File"}

              <input
                type="file"
                accept=".pdf,.doc,.docx,.txt"
                onChange={handleFileChange}
                hidden
              />
            </label>

            {/* SELECTED FILE */}

            {selectedFile && (
              <div className="selected-file">
                <FileText size={18} />

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

                <CheckCircle2
                  size={18}
                  className="success-icon"
                />
              </div>
            )}
          </div>

          {!selectedFile && (
            <div className="document-info">
              <FileText size={18} />

              <div>
                <strong>
                  No document selected
                </strong>

                <span>
                  PDF, DOC, DOCX or TXT
                </span>
              </div>
            </div>
          )}
        </div>
      </section>

      {/* JOURNEY SUMMARY */}

      <section className="section">
        <div className="card journey-summary">
          <div>
            <span className="small-label">
              CURRENT GOAL
            </span>

            <h2>
              Become an APM / Product Manager
            </h2>

            <p>
              Continue building product thinking,
              user research, case-study,
              communication, and technical
              skills.
            </p>
          </div>

          <div className="journey-progress">
            <strong>62%</strong>

            <div className="progress-bar">
              <div
                style={{
                  width: "62%",
                }}
              />
            </div>

            <span>Journey progress</span>
          </div>
        </div>
      </section>
    </>
  );
}

/* =========================================================
   SKILLS PAGE
========================================================= */

function SkillsPage() {
  return (
    <>
      <PageHeader
        eyebrow="SKILLS"
        title="Your skill gaps"
        subtitle="Understand where you are today and what to improve next."
      />

      <section className="skill-summary-grid">
        <div className="card">
          <span className="small-label">
            CURRENT SKILL LEVEL
          </span>

          <strong className="summary-number">
            55%
          </strong>

          <span>
            Average across tracked skills
          </span>
        </div>

        <div className="card">
          <span className="small-label">
            REQUIRED LEVEL
          </span>

          <strong className="summary-number">
            77%
          </strong>

          <span>
            Average target level
          </span>
        </div>

        <div className="card">
          <span className="small-label">
            TOTAL GAP
          </span>

          <strong className="summary-number">
            22%
          </strong>

          <span>
            Average improvement needed
          </span>
        </div>
      </section>

      <section className="section">
        <div className="card">
          <div className="card-header-row">
            <div>
              <span className="small-label">
                SKILL ANALYSIS
              </span>

              <h2>
                Current vs required skills
              </h2>
            </div>

            <Target size={22} />
          </div>

          <div className="skills-list">
            {skills.map((skill) => (
              <SkillRow
                key={skill.name}
                skill={skill}
              />
            ))}
          </div>
        </div>
      </section>
    </>
  );
}

/* =========================================================
   PLAN PAGE
========================================================= */

function PlanPage() {
  const [tab, setTab] =
    useState("resources");

  return (
    <>
      <PageHeader
        eyebrow="LEARNING PLAN"
        title="Your personalized plan"
        subtitle="Resources, weekly learning, and practical projects."
      />

      <div className="tabs">
        <button
          className={
            tab === "resources"
              ? "active"
              : ""
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
              ? "active"
              : ""
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
              ? "active"
              : ""
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
          {resources.map((resource) => (
            <div
              className="card resource-card"
              key={resource.title}
            >
              <div className="resource-icon">
                <BookOpen size={20} />
              </div>

              <span className="resource-type">
                {resource.type}
              </span>

              <h3>{resource.title}</h3>

              <div className="resource-meta">
                <span>
                  {resource.level}
                </span>

                <span>
                  {resource.time}
                </span>
              </div>

              <button className="text-button">
                Open Resource
                <ArrowRight size={16} />
              </button>
            </div>
          ))}
        </div>
      )}

      {tab === "weekly" && (
        <div className="card">
          <div className="weekly-plan-list">
            {weeklyPlan.map((item) => (
              <div
                className="weekly-item"
                key={item.day}
              >
                <div className="day-circle">
                  {item.day.slice(0, 1)}
                </div>

                <div className="weekly-content">
                  <div className="weekly-top">
                    <strong>
                      {item.day}
                    </strong>

                    <span>
                      {item.time}
                    </span>
                  </div>

                  <span className="weekly-topic">
                    {item.topic}
                  </span>

                  <p>{item.task}</p>
                </div>

                <ChevronRight size={18} />
              </div>
            ))}
          </div>
        </div>
      )}

      {tab === "projects" && (
        <div className="project-grid">
          {projects.map((project) => (
            <div
              className="card project-card"
              key={project.title}
            >
              <div className="project-icon">
                <BriefcaseBusiness
                  size={20}
                />
              </div>

              <span className="small-label">
                PRACTICE PROJECT
              </span>

              <h3>{project.title}</h3>

              <p>
                {project.description}
              </p>

              <div className="tag-list">
                {project.skills.map(
                  (skill) => (
                    <span key={skill}>
                      {skill}
                    </span>
                  )
                )}
              </div>

              <button className="primary-button">
                Start Project
                <ArrowRight size={16} />
              </button>
            </div>
          ))}
        </div>
      )}
    </>
  );
}

/* =========================================================
   PROGRESS PAGE
========================================================= */

function ProgressPage() {
  return (
    <>
      <PageHeader
        eyebrow="PROGRESS"
        title="Track your progress"
        subtitle="See how your learning journey is developing over time."
      />

      <section className="metric-grid">
        <MetricCard
          icon={TrendingUp}
          title="Overall Progress"
          value="62%"
          subtitle="+8% this week"
        />

        <MetricCard
          icon={CheckCircle2}
          title="Completed"
          value="7"
          subtitle="Activities"
        />

        <MetricCard
          icon={Clock3}
          title="Learning Time"
          value="10h"
          subtitle="This week"
        />

        <MetricCard
          icon={BarChart3}
          title="Average Score"
          value="82%"
          subtitle="Across activities"
        />
      </section>

      <section className="two-column-grid section">
        <div className="card">
          <SectionHeader
            title="Skill progress"
            subtitle="Current improvement"
          />

          {skills
            .slice(0, 4)
            .map((skill) => (
              <div
                className="progress-skill"
                key={skill.name}
              >
                <div className="progress-skill-top">
                  <span>
                    {skill.name}
                  </span>

                  <strong>
                    {skill.current}%
                  </strong>
                </div>

                <div className="progress-bar">
                  <div
                    style={{
                      width: `${skill.current}%`,
                    }}
                  />
                </div>
              </div>
            ))}
        </div>

        <div className="card">
          <SectionHeader
            title="Recent activity"
            subtitle="Your latest learning activities"
          />

          <ActivityItem
            title="Product Fundamentals Quiz"
            score="90%"
            time="Today"
          />

          <ActivityItem
            title="User Research Exercise"
            score="82%"
            time="Yesterday"
          />

          <ActivityItem
            title="Product Case Study"
            score="75%"
            time="2 days ago"
          />

          <ActivityItem
            title="Figma Practice"
            score="88%"
            time="3 days ago"
          />
        </div>
      </section>

      <section className="card adaptive-card">
        <div className="card-icon purple">
          <Brain size={20} />
        </div>

        <div>
          <span className="small-label">
            ADAPTIVE LEARNING
          </span>

          <h2>
            EduPath is adapting your plan
          </h2>

          <p>
            Based on your recent activities,
            more time is being allocated to
            User Research and Product Case
            Studies.
          </p>
        </div>
      </section>
    </>
  );
}

/* =========================================================
   REPORTS
========================================================= */

function ReportsPage() {
  return (
    <>
      <PageHeader
        eyebrow="REPORTS"
        title="Progress reports"
        subtitle="Review your learning performance and improvement areas."
      />

      <div className="report-grid">
        <div className="card report-card">
          <div className="report-icon">
            <TrendingUp size={21} />
          </div>

          <span className="small-label">
            OVERALL
          </span>

          <h2>62%</h2>

          <p>
            Overall learning progress
          </p>

          <button className="secondary-button">
            View Report
          </button>
        </div>

        <div className="card report-card">
          <div className="report-icon">
            <Target size={21} />
          </div>

          <span className="small-label">
            SKILL DEVELOPMENT
          </span>

          <h2>5</h2>

          <p>
            Skills currently being developed
          </p>

          <button className="secondary-button">
            View Skills
          </button>
        </div>

        <div className="card report-card">
          <div className="report-icon">
            <CircleAlert size={21} />
          </div>

          <span className="small-label">
            AREAS TO IMPROVE
          </span>

          <h2>2</h2>

          <p>
            High-priority skill gaps
          </p>

          <button className="secondary-button">
            View Gaps
          </button>
        </div>
      </div>

      <section className="section card">
        <SectionHeader
          title="Latest learning report"
          subtitle="Generated from your recent activity"
        />

        <div className="report-insight">
          <Lightbulb size={21} />

          <div>
            <strong>
              Keep building practical product
              experience.
            </strong>

            <p>
              Your learning progress is improving.
              Continue with user research and
              case-study practice to strengthen
              product thinking.
            </p>
          </div>
        </div>
      </section>
    </>
  );
}

/* =========================================================
   AI COACH
========================================================= */

function CoachPage() {
  const [question, setQuestion] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [messages, setMessages] =
    useState([
      {
        role: "assistant",
        text:
          "Hi! I'm EduPath AI Coach. Ask me anything about your learning plan, Product Management, skill gaps, or projects.",
      },
    ]);

  const sendMessage = async () => {
    const trimmed =
      question.trim();

    if (!trimmed || loading) {
      return;
    }

    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        text: trimmed,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const data =
        await askEduPath(trimmed);

      const answer =
        data.answer ||
        data.response ||
        data.message ||
        data.result ||
        "I couldn't generate a response right now.";

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          text:
            typeof answer === "string"
              ? answer
              : JSON.stringify(
                  answer,
                  null,
                  2
                ),
        },
      ]);
    } catch (error) {
      console.error(
        "AI Coach error:",
        error
      );

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          text:
            "I couldn't connect to EduPath AI right now. Please make sure the FastAPI backend is running and try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <PageHeader
        eyebrow="AI COACH"
        title="Ask EduPath"
        subtitle="Get personalized guidance throughout your learning journey."
      />

      <section className="coach-container card">
        <div className="coach-header">
          <div className="coach-avatar">
            <Bot size={22} />
          </div>

          <div>
            <strong>
              EduPath AI Coach
            </strong>

            <span>
              Personal learning assistant
            </span>
          </div>
        </div>

        <div className="chat-messages">
          {messages.map(
            (message, index) => (
              <div
                key={index}
                className={`chat-message ${
                  message.role === "user"
                    ? "user"
                    : "assistant"
                }`}
              >
                {message.text}
              </div>
            )
          )}

          {loading && (
            <div className="chat-message assistant">
              Thinking...
            </div>
          )}
        </div>

        <div className="chat-input-row">
          <input
            value={question}
            onChange={(e) =>
              setQuestion(e.target.value)
            }
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                sendMessage();
              }
            }}
            placeholder="Ask something about your learning..."
            disabled={loading}
          />

          <button
            className="primary-button send-button"
            onClick={sendMessage}
            disabled={loading}
          >
            {loading ? (
              "..."
            ) : (
              <Send size={17} />
            )}
          </button>
        </div>
      </section>
    </>
  );
}

/* =========================================================
   REUSABLE COMPONENTS
========================================================= */

function PageHeader({
  eyebrow,
  title,
  subtitle,
}) {
  return (
    <div className="page-header">
      <span className="small-label">
        {eyebrow}
      </span>

      <h1>{title}</h1>

      <p>{subtitle}</p>
    </div>
  );
}

function SectionHeader({
  title,
  subtitle,
}) {
  return (
    <div className="section-header">
      <div>
        <h2>{title}</h2>

        {subtitle && (
          <p>{subtitle}</p>
        )}
      </div>
    </div>
  );
}

function MetricCard({
  icon: Icon,
  title,
  value,
  subtitle,
}) {
  return (
    <div className="metric-card">
      <div className="metric-icon">
        <Icon size={20} />
      </div>

      <span>{title}</span>

      <strong>{value}</strong>

      <small>{subtitle}</small>
    </div>
  );
}

function RoadmapItem({
  number,
  title,
  status,
}) {
  return (
    <div className="roadmap-item">
      <div className="roadmap-number">
        {number}
      </div>

      <div className="roadmap-content">
        <strong>{title}</strong>

        <span>{status}</span>
      </div>

      <ChevronRight size={18} />
    </div>
  );
}

/* =========================================================
   EDITABLE INPUT
========================================================= */

function InputField({
  label,
  value,
  onChange,
  type = "text",
}) {
  return (
    <label className="input-field">
      <span>{label}</span>

      <input
        type={type}
        value={value}
        onChange={(e) =>
          onChange(e.target.value)
        }
      />
    </label>
  );
}

function SkillRow({ skill }) {
  return (
    <div className="skill-row">
      <div className="skill-main">
        <div className="skill-title-row">
          <strong>{skill.name}</strong>

          <span
            className={`priority ${skill.priority.toLowerCase()}`}
          >
            {skill.priority}
          </span>
        </div>

        <p>{skill.reason}</p>

        <div className="skill-bars">
          <div>
            <span>Current</span>

            <div className="progress-bar">
              <div
                style={{
                  width: `${skill.current}%`,
                }}
              />
            </div>
          </div>

          <div>
            <span>Required</span>

            <div className="required-bar">
              <div
                style={{
                  width: `${skill.required}%`,
                }}
              />
            </div>
          </div>
        </div>
      </div>

      <div className="skill-gap">
        <strong>
          {skill.gap}%
        </strong>

        <span>gap</span>
      </div>
    </div>
  );
}

function ActivityItem({
  title,
  score,
  time,
}) {
  return (
    <div className="activity-item">
      <div className="activity-check">
        <CheckCircle2 size={18} />
      </div>

      <div className="activity-content">
        <strong>{title}</strong>

        <span>{time}</span>
      </div>

      <strong className="activity-score">
        {score}
      </strong>
    </div>
  );
}

export default App;