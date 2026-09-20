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

const navItems = [
  { name: "Home", icon: Home },
  { name: "My Journey", icon: Compass },
  { name: "Skills", icon: Target },
  { name: "Plan", icon: CalendarDays },
  { name: "Progress", icon: TrendingUp },
  { name: "Reports", icon: FileText },
  { name: "AI Coach", icon: Bot },
];

const skills = [
  {
    name: "Product Strategy",
    current: 72,
    required: 90,
    priority: "High",
  },
  {
    name: "User Research",
    current: 55,
    required: 85,
    priority: "High",
  },
  {
    name: "Product Analytics",
    current: 48,
    required: 80,
    priority: "Medium",
  },
  {
    name: "Communication",
    current: 68,
    required: 85,
    priority: "Medium",
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

const API_URL = "https://edupath-2-195z.onrender.com";

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

  const response = await fetch(`${API_URL}/api/analyze-document`, {
    method: "POST",
    body: formData,
  });

  const data = await response.json();

  if (!response.ok || !data.success) {
    throw new Error(data.message || "Resume analysis failed");
  }

  return data;
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
        current_skills: "Product Fundamentals, Python, Problem Solving, Communication, Figma",
        experience: "Beginner-level Product Management experience with an interest in AI-powered products and user-focused problem solving.",
        hours_per_week: 10,
        learning_preference: "Practical + Visual",
      },
      progress: {},
      struggles: [],
      progress_report: {},
    }),
  });

  if (!response.ok) {
    throw new Error("AI Coach request failed");
  }

  return response.json();
}


function App() {
  const [activePage, setActivePage] = useState("Home");
  const [mobileMenu, setMobileMenu] = useState(false);
  const [message, setMessage] = useState("");
  const [chatMessages, setChatMessages] = useState([
    {
      role: "assistant",
      text: "Hi! I'm your EduPath AI Coach. Ask me about your skills, learning plan, projects, or Product Management career.",
    },
  ]);

  const goTo = (page) => {
    setActivePage(page);
    setMobileMenu(false);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const sendMessage = async () => {
    const trimmed = message.trim();

    if (!trimmed) return;

    setChatMessages((previous) => [
      ...previous,
      { role: "user", text: trimmed },
    ]);
    setMessage("");

    try {
      const data = await askEduPath(trimmed);

      setChatMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          text: data.answer || "I could not generate an answer right now.",
        },
      ]);
    } catch (error) {
      console.error(error);

      setChatMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          text: "I couldn't connect to EduPath right now. Please make sure the FastAPI backend is running on port 8000.",
        },
      ]);
    }
  };

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand" onClick={() => goTo("Home")}>
          <div className="brand-mark">
            <Sparkles size={18} />
          </div>

          <div>
            <div className="brand-name">EduPath</div>
            <div className="brand-subtitle">
              Personalized learning, powered by AI
            </div>
          </div>
        </div>

        <nav className="desktop-nav">
          {navItems.map((item) => {
            const Icon = item.icon;

            return (
              <button
                key={item.name}
                className={`nav-item ${
                  activePage === item.name ? "active" : ""
                }`}
                onClick={() => goTo(item.name)}
              >
                <Icon size={16} />
                <span>{item.name}</span>
              </button>
            );
          })}
        </nav>

        <button
          className="mobile-menu-button"
          onClick={() => setMobileMenu(!mobileMenu)}
        >
          {mobileMenu ? <X size={22} /> : <Menu size={22} />}
        </button>
      </header>

      {mobileMenu && (
        <div className="mobile-nav">
          {navItems.map((item) => {
            const Icon = item.icon;

            return (
              <button
                key={item.name}
                className={`mobile-nav-item ${
                  activePage === item.name ? "active" : ""
                }`}
                onClick={() => goTo(item.name)}
              >
                <Icon size={18} />
                {item.name}
              </button>
            );
          })}
        </div>
      )}

      <main className="main-content">
        {activePage === "Home" && <HomePage goTo={goTo} />}

        {activePage === "My Journey" && <JourneyPage />}

        {activePage === "Skills" && <SkillsPage />}

        {activePage === "Plan" && <PlanPage />}

        {activePage === "Progress" && <ProgressPage />}

        {activePage === "Reports" && <ReportsPage />}

        {activePage === "AI Coach" && (
          <CoachPage
            message={message}
            setMessage={setMessage}
            chatMessages={chatMessages}
            sendMessage={sendMessage}
          />
        )}
      </main>

      <footer className="footer">
        <div>
          <strong>✦ EduPath</strong>
          <span> Personalized learning for your career journey.</span>
        </div>

        <span>AI-powered • Skill-focused • Personalized</span>
      </footer>
    </div>
  );
}

function HomePage({ goTo }) {
  return (
    <>
      <section className="hero">
        <div className="hero-content">
          <div className="eyebrow">
            <Sparkles size={15} />
            Your personalized learning journey
          </div>

          <h1>
            Build your path to
            <span> Product Manager. ✨</span>
          </h1>

          <p>
            EduPath analyzes your current skills, identifies gaps, and creates
            a personalized learning path to help you reach your career goal.
          </p>

          <div className="hero-actions">
            <button className="primary-button" onClick={() => goTo("Plan")}>
              Continue Learning
              <ArrowRight size={17} />
            </button>

            <button
              className="secondary-button"
              onClick={() => goTo("Skills")}
            >
              View Skill Gaps
            </button>
          </div>
        </div>

        <div className="hero-progress-card">
          <div className="hero-progress-top">
            <div>
              <span className="small-label">Overall Progress</span>
              <strong>64%</strong>
            </div>

            <div className="progress-circle">
              <span>64%</span>
            </div>
          </div>

          <div className="progress-track large">
            <div className="progress-fill" style={{ width: "64%" }} />
          </div>

          <div className="progress-caption">
            <span>You're making steady progress.</span>
            <span>Keep going!</span>
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
            label="Skill Gaps"
            value="4"
            description="Skills to strengthen"
          />

          <MetricCard
            icon={<CheckCircle2 />}
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
            label="Current Goal"
            value="PM"
            description="Product Manager"
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
            status="Completed"
          />

          <RoadmapItem
            number="02"
            title="Identify skill gaps"
            description="Understand the capabilities you need to develop."
            status="Completed"
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
            <Sparkles size={20} />
          </div>

          <div>
            <span className="small-label">AI Insight</span>

            <h3>Your next opportunity</h3>

            <p>
              Your Product Strategy foundation is developing well. The next
              useful step is to strengthen User Research through interviews,
              case studies and practical exercises.
            </p>

            <button
              className="text-button"
              onClick={() => goTo("Skills")}
            >
              Explore recommendation
              <ArrowRight size={16} />
            </button>
          </div>
        </div>

        <div className="next-action-card">
          <span className="small-label">Next action</span>

          <h3>Complete a User Research case study</h3>

          <div className="action-meta">
            <span>
              <Clock3 size={15} />
              45 minutes
            </span>

            <span>
              <Target size={15} />
              User Research
            </span>
          </div>

          <button
            className="primary-button full"
            onClick={() => goTo("Plan")}
          >
            Start Activity
            <ArrowRight size={16} />
          </button>
        </div>
      </section>
    </>
  );
}

function JourneyPage() {
  const [tab, setTab] = useState("profile");

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
  const [uploading, setUploading] = useState(false);
  const [saveMessage, setSaveMessage] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [documentResult, setDocumentResult] = useState(null);

  const updateProfile = (field, value) => {
    setProfile((previous) => ({
      ...previous,
      [field]: value,
    }));
    setSaveMessage("");
  };

  const handleSaveProfile = async () => {
    try {
      setSaving(true);
      setSaveMessage("");

      await saveProfile(profile);

      setSaveMessage("Profile saved successfully.");
    } catch (error) {
      console.error(error);
      setSaveMessage(
        "Could not save profile. Make sure the FastAPI backend is running."
      );
    } finally {
      setSaving(false);
    }
  };

  const handleFileChange = async (event) => {
    const file = event.target.files?.[0];

    if (!file) return;

    setSelectedFile(file);
    setDocumentResult(null);
    setSaveMessage("");
    setUploading(true);

    try {
      const result = await analyzeResume(file);

      setDocumentResult(result);
      setSaveMessage("Resume uploaded and analyzed successfully.");
    } catch (error) {
      console.error("Resume upload error:", error);
      setSaveMessage(
        error.message ||
          "Could not upload resume. Make sure the backend is running."
      );
    } finally {
      setUploading(false);
    }
  };

  return (
    <PageHeader
      eyebrow="MY JOURNEY"
      title="Know your starting point."
      description="Manage your learner profile and documents that EduPath uses to personalize your learning path."
    >
      <div className="tabs">
        <button
          className={tab === "profile" ? "tab active" : "tab"}
          onClick={() => setTab("profile")}
        >
          Learner Profile
        </button>

        <button
          className={tab === "documents" ? "tab active" : "tab"}
          onClick={() => setTab("documents")}
        >
          Documents
        </button>
      </div>

      {tab === "profile" ? (
        <div className="content-card">
          <div className="card-heading">
            <div>
              <span className="small-label">PROFILE</span>
              <h2>Your learner profile</h2>
            </div>

            <span className="status-badge success">Profile Active</span>
          </div>

          <div className="form-grid">
            <EditableInputField
              label="Career Goal"
              value={profile.career_goal}
              onChange={(value) => updateProfile("career_goal", value)}
            />

            <EditableInputField
              label="Target Role"
              value={profile.target_role}
              onChange={(value) => updateProfile("target_role", value)}
            />

            <EditableInputField
              label="Learning Hours / Week"
              type="number"
              value={profile.hours_per_week}
              onChange={(value) =>
                updateProfile("hours_per_week", Number(value))
              }
            />

            <EditableInputField
              label="Learning Preference"
              value={profile.learning_preference}
              onChange={(value) =>
                updateProfile("learning_preference", value)
              }
            />
          </div>

          <div className="profile-section">
            <label className="input-field">
              <span>Current Skills</span>
              <textarea
                value={profile.current_skills}
                onChange={(event) =>
                  updateProfile("current_skills", event.target.value)
                }
                rows={4}
              />
            </label>
          </div>

          <div className="profile-section">
            <label className="input-field">
              <span>Experience</span>
              <textarea
                value={profile.experience}
                onChange={(event) =>
                  updateProfile("experience", event.target.value)
                }
                rows={4}
              />
            </label>
          </div>

          <div className="profile-section">
            <span className="small-label">CURRENT SKILLS</span>

            <div className="chip-list">
              {profile.current_skills
                .split(",")
                .map((skill) => skill.trim())
                .filter(Boolean)
                .map((skill) => (
                  <span className="skill-chip" key={skill}>
                    {skill}
                  </span>
                ))}
            </div>
          </div>

          <div className="profile-actions">
            <button
              className="primary-button"
              onClick={handleSaveProfile}
              disabled={saving}
            >
              {saving ? "Saving..." : "Save Profile"}
            </button>

            {saveMessage && (
              <span className="muted-text">{saveMessage}</span>
            )}
          </div>
        </div>
      ) : (
        <div className="content-card">
          <div className="card-heading">
            <div>
              <span className="small-label">DOCUMENTS</span>
              <h2>Your learning documents</h2>
            </div>
          </div>

          <div className="upload-box">
            <div className="upload-icon">
              <Upload size={24} />
            </div>

            <h3>Upload your resume</h3>

            <p>
              Upload your resume or profile document so EduPath can analyze
              your current skills.
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
                onChange={handleFileChange}
                hidden
                disabled={uploading}
              />
            </label>

            {selectedFile && (
              <div className="document-row">
                <div className="document-icon">
                  <FileText size={20} />
                </div>

                <div>
                  <strong>{selectedFile.name}</strong>
                  <span>
                    {(selectedFile.size / 1024).toFixed(1)} KB
                  </span>
                </div>

                {uploading ? (
                  <span className="status-badge warning">Analyzing</span>
                ) : documentResult?.success ? (
                  <span className="status-badge success">Analyzed</span>
                ) : null}
              </div>
            )}

            {saveMessage && tab === "documents" && (
              <p className="muted-text">{saveMessage}</p>
            )}
          </div>

          {documentResult?.text && (
            <div className="content-card resume-result-card">
              <div className="card-heading">
                <div>
                  <span className="small-label">EXTRACTED RESUME TEXT</span>
                  <h2>Document received by EduPath</h2>
                </div>
              </div>

              <p className="muted-text">
                The resume text was successfully extracted. The next step is
                to connect this extracted content to the existing EduPath
                document-analysis and skill-gap agents.
              </p>

              <div className="resume-preview">
                {documentResult.text.slice(0, 3000)}
                {documentResult.text.length > 3000 ? "..." : ""}
              </div>
            </div>
          )}
        </div>
      )}
    </PageHeader>
  );
}

function EditableInputField({ label, value, onChange, type = "text" }) {
  return (
    <label className="input-field">
      <span>{label}</span>
      <input
        type={type}
        value={value}
        onChange={(event) => onChange(event.target.value)}
      />
    </label>
  );
}

function SkillsPage() {
  const [tab, setTab] = useState("gaps");

  return (
    <PageHeader
      eyebrow="SKILLS"
      title="Turn gaps into capabilities."
      description="Understand where you are today, where you need to be, and what EduPath recommends next."
    >
      <div className="tabs">
        <button
          className={tab === "gaps" ? "tab active" : "tab"}
          onClick={() => setTab("gaps")}
        >
          Skill Gaps
        </button>

        <button
          className={tab === "objectives" ? "tab active" : "tab"}
          onClick={() => setTab("objectives")}
        >
          Learning Objectives
        </button>
      </div>

      {tab === "gaps" ? (
        <div className="skill-list">
          {skills.map((skill) => (
            <div className="skill-card" key={skill.name}>
              <div className="skill-card-header">
                <div>
                  <h3>{skill.name}</h3>
                  <span className="muted-text">
                    Gap: {skill.required - skill.current}%
                  </span>
                </div>

                <span
                  className={`priority ${
                    skill.priority === "High" ? "high" : "medium"
                  }`}
                >
                  {skill.priority} Priority
                </span>
              </div>

              <div className="level-row">
                <span>Current level</span>
                <strong>{skill.current}%</strong>
              </div>

              <div className="progress-track">
                <div
                  className="progress-fill"
                  style={{ width: `${skill.current}%` }}
                />
              </div>

              <div className="level-row">
                <span>Required level</span>
                <strong>{skill.required}%</strong>
              </div>

              <div className="skill-reason">
                <strong>Why this matters:</strong>
                <span>
                  This capability is important for succeeding in Product
                  Management roles.
                </span>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="objective-grid">
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
        </div>
      )}
    </PageHeader>
  );
}

function PlanPage() {
  const [tab, setTab] = useState("resources");

  return (
    <PageHeader
      eyebrow="LEARNING PLAN"
      title="Your personalized action plan."
      description="Resources, weekly activities and practical projects generated around your skill gaps."
    >
      <div className="tabs">
        <button
          className={tab === "resources" ? "tab active" : "tab"}
          onClick={() => setTab("resources")}
        >
          Resources
        </button>

        <button
          className={tab === "weekly" ? "tab active" : "tab"}
          onClick={() => setTab("weekly")}
        >
          Weekly Plan
        </button>

        <button
          className={tab === "projects" ? "tab active" : "tab"}
          onClick={() => setTab("projects")}
        >
          Practice & Projects
        </button>
      </div>

      {tab === "resources" && (
        <div className="resource-grid">
          <ResourceCard
            type="COURSE"
            title="Product Management Fundamentals"
            description="Build a strong foundation in product discovery, strategy and execution."
            time="3 hours"
          />

          <ResourceCard
            type="VIDEO"
            title="User Research for Product Managers"
            description="Learn interviews, surveys, personas and pain-point discovery."
            time="1 hour"
          />

          <ResourceCard
            type="ARTICLE"
            title="Understanding Product Metrics"
            description="Learn how PMs use metrics to evaluate product performance."
            time="30 minutes"
          />
        </div>
      )}

      {tab === "weekly" && (
        <div className="weekly-plan">
          <PlanDay day="MON" title="Product Strategy" time="1.5h" status="Done" />
          <PlanDay day="TUE" title="User Research" time="1.5h" status="Done" />
          <PlanDay
            day="WED"
            title="Case Study Practice"
            time="2h"
            status="Today"
          />
          <PlanDay day="THU" title="Product Metrics" time="1h" status="Upcoming" />
          <PlanDay day="FRI" title="Project Work" time="2h" status="Upcoming" />
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
            title="Student Productivity App"
            description="Identify student pain points and design a product solution using PM case-study thinking."
            skills="Discovery • Prioritization • UX"
          />
        </div>
      )}
    </PageHeader>
  );
}

function ProgressPage() {
  return (
    <PageHeader
      eyebrow="PROGRESS"
      title="See how far you've come."
      description="Track activities, skill development and the areas that need more attention."
    >
      <div className="metric-grid">
        <MetricCard
          icon={<TrendingUp />}
          label="Overall Progress"
          value="64%"
          description="Across your learning path"
        />

        <MetricCard
          icon={<CheckCircle2 />}
          label="Skills Acquired"
          value="8"
          description="Skills strengthened"
        />

        <MetricCard
          icon={<Clock3 />}
          label="Learning Time"
          value="18.5h"
          description="Total tracked time"
        />

        <MetricCard
          icon={<Target />}
          label="Remaining Gaps"
          value="4"
          description="Areas to improve"
        />
      </div>

      <div className="content-card">
        <div className="card-heading">
          <div>
            <span className="small-label">SKILL PROGRESS</span>
            <h2>Your capabilities</h2>
          </div>
        </div>

        <div className="progress-skill-list">
          {skills.map((skill) => (
            <div className="progress-skill" key={skill.name}>
              <div>
                <span>{skill.name}</span>
                <strong>{skill.current}%</strong>
              </div>

              <div className="progress-track">
                <div
                  className="progress-fill"
                  style={{ width: `${skill.current}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="content-card">
        <div className="card-heading">
          <div>
            <span className="small-label">ACTIVITY HISTORY</span>
            <h2>Recent learning</h2>
          </div>
        </div>

        <div className="activity-list">
          {activities.map((activity) => (
            <div className="activity-row" key={activity.title}>
              <div className="activity-icon">
                <BookOpen size={18} />
              </div>

              <div className="activity-info">
                <strong>{activity.title}</strong>
                <span>
                  {activity.type} • {activity.time}
                </span>
              </div>

              <span
                className={`status-badge ${
                  activity.status === "Completed"
                    ? "success"
                    : activity.status === "In Progress"
                    ? "warning"
                    : "neutral"
                }`}
              >
                {activity.status}
              </span>
            </div>
          ))}
        </div>
      </div>

      <div className="adaptive-card">
        <div className="card-icon purple">
          <Sparkles size={20} />
        </div>

        <div>
          <span className="small-label">ADAPTIVE LEARNING</span>
          <h2>Your plan can evolve with you.</h2>
          <p>
            EduPath can detect struggling areas and adjust your upcoming
            activities based on your progress.
          </p>
        </div>

        <button className="primary-button">
          View Adaptive Plan
          <ArrowRight size={16} />
        </button>
      </div>
    </PageHeader>
  );
}

function ReportsPage() {
  return (
    <PageHeader
      eyebrow="REPORTS"
      title="Your learning report."
      description="A clear snapshot of your progress, acquired skills and remaining development areas."
    >
      <div className="report-hero">
        <div>
          <span className="small-label">OVERALL PROGRESS</span>
          <div className="report-score">64%</div>
          <p>
            You have made consistent progress toward your Product Manager
            learning goal.
          </p>
        </div>

        <div className="report-circle">64%</div>
      </div>

      <div className="report-grid">
        <ReportCard
          title="Skills Acquired"
          count="8"
          items={[
            "Product Fundamentals",
            "Problem Discovery",
            "MVP Thinking",
          ]}
        />

        <ReportCard
          title="In Progress"
          count="4"
          items={[
            "Product Strategy",
            "User Research",
            "Communication",
          ]}
        />

        <ReportCard
          title="Remaining Gaps"
          count="4"
          items={[
            "Product Analytics",
            "Advanced Research",
            "Prioritization",
          ]}
        />
      </div>

      <div className="content-card">
        <div className="card-heading">
          <div>
            <span className="small-label">NEXT STEPS</span>
            <h2>Recommended focus</h2>
          </div>
        </div>

        <div className="next-step-list">
          <NextStep
            number="01"
            title="Complete a user research case study"
          />

          <NextStep
            number="02"
            title="Practice product prioritization frameworks"
          />

          <NextStep
            number="03"
            title="Build one portfolio-ready PM project"
          />
        </div>
      </div>
    </PageHeader>
  );
}

function CoachPage({
  message,
  setMessage,
  chatMessages,
  sendMessage,
}) {
  return (
    <PageHeader
      eyebrow="AI COACH"
      title="Your personal PM learning coach."
      description="Ask questions about your learning path, skills, projects, case studies or Product Management."
    >
      <div className="coach-layout">
        <div className="coach-sidebar">
          <div className="coach-profile">
            <div className="coach-avatar">
              <Bot size={24} />
            </div>

            <div>
              <strong>EduPath Coach</strong>
              <span>AI Learning Assistant</span>
            </div>
          </div>

          <div className="coach-suggestion">
            <span>TRY ASKING</span>

            <button>What should I learn this week?</button>
            <button>How can I improve user research?</button>
            <button>Give me a PM case study.</button>
            <button>Review my learning progress.</button>
          </div>
        </div>

        <div className="chat-card">
          <div className="chat-header">
            <div>
              <strong>Ask EduPath</strong>
              <span>Your learning context is available to the coach.</span>
            </div>

            <span className="online-dot">Online</span>
          </div>

          <div className="chat-messages">
            {chatMessages.map((chat, index) => (
              <div
                className={`chat-row ${
                  chat.role === "user" ? "user" : "assistant"
                }`}
                key={index}
              >
                <div className="chat-bubble">{chat.text}</div>
              </div>
            ))}
          </div>

          <div className="chat-input">
            <input
              value={message}
              onChange={(event) => setMessage(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter") sendMessage();
              }}
              placeholder="Ask your learning coach..."
            />

            <button onClick={sendMessage}>
              <Send size={18} />
            </button>
          </div>
        </div>
      </div>
    </PageHeader>
  );
}

function PageHeader({ eyebrow, title, description, children }) {
  return (
    <section className="page">
      <div className="page-header">
        <span className="eyebrow">{eyebrow}</span>
        <h1>{title}</h1>
        <p>{description}</p>
      </div>

      {children}
    </section>
  );
}

function SectionHeading({ title, subtitle }) {
  return (
    <div className="section-heading">
      <div>
        <h2>{title}</h2>
        <p>{subtitle}</p>
      </div>
    </div>
  );
}

function MetricCard({ icon, label, value, description }) {
  return (
    <div className="metric-card">
      <div className="metric-icon">{icon}</div>

      <span className="small-label">{label}</span>

      <strong className="metric-value">{value}</strong>

      <span className="muted-text">{description}</span>
    </div>
  );
}

function RoadmapItem({ number, title, description, status }) {
  return (
    <div className={`roadmap-item ${status.toLowerCase()}`}>
      <div className="roadmap-number">{number}</div>

      <div className="roadmap-content">
        <div className="roadmap-title-row">
          <h3>{title}</h3>

          <span className="status-badge">{status}</span>
        </div>

        <p>{description}</p>
      </div>
    </div>
  );
}

function InputField({ label, value }) {
  return (
    <label className="input-field">
      <span>{label}</span>
      <input value={value} readOnly />
    </label>
  );
}

function ObjectiveCard({ title, skill, level }) {
  return (
    <div className="objective-card">
      <div className="objective-icon">
        <Target size={20} />
      </div>

      <span className="small-label">{skill}</span>

      <h3>{title}</h3>

      <span className="level-badge">{level}</span>
    </div>
  );
}

function ResourceCard({ type, title, description, time }) {
  return (
    <div className="resource-card">
      <div className="resource-top">
        <span className="type-badge">{type}</span>

        <span className="time">
          <Clock3 size={14} />
          {time}
        </span>
      </div>

      <h3>{title}</h3>

      <p>{description}</p>

      <button className="text-button">
        Open resource
        <ArrowRight size={16} />
      </button>
    </div>
  );
}

function PlanDay({ day, title, time, status }) {
  return (
    <div className="plan-day">
      <div className="day-label">{day}</div>

      <div className="day-content">
        <strong>{title}</strong>

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

function ProjectCard({ title, description, skills }) {
  return (
    <div className="project-card">
      <div className="project-icon">
        <Sparkles size={20} />
      </div>

      <span className="small-label">PRACTICAL PROJECT</span>

      <h3>{title}</h3>

      <p>{description}</p>

      <span className="project-skills">{skills}</span>

      <button className="primary-button full">
        Start Project
        <ArrowRight size={16} />
      </button>
    </div>
  );
}

function ReportCard({ title, count, items }) {
  return (
    <div className="report-card">
      <div className="report-card-top">
        <span className="small-label">{title}</span>
        <strong>{count}</strong>
      </div>

      <div className="report-items">
        {items.map((item) => (
          <div key={item}>
            <CheckCircle2 size={15} />
            <span>{item}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function NextStep({ number, title }) {
  return (
    <div className="next-step">
      <span className="next-step-number">{number}</span>

      <strong>{title}</strong>

      <ArrowRight size={17} />
    </div>
  );
}

export default App;