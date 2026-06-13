import { useState } from "react";
import "./App.css";

const API_BASE_URL = "http://127.0.0.1:8000";

const sampleResume = `Data Science Intern, ABC Startup
- Made dashboard for sales team
- Used Python to clean data
- Helped model customer churn`;

const targetPositionGroups = {
  "AI / Machine Learning": [
    "Machine Learning Engineer",
    "Machine Learning Engineer Intern",
    "AI Engineer",
    "Applied AI Engineer",
    "Applied Machine Learning Engineer",
    "Deep Learning Engineer",
    "Computer Vision Engineer",
    "NLP Engineer",
    "LLM Engineer",
    "Generative AI Engineer",
    "MLOps Engineer",
    "AI Infrastructure Engineer",
    "AI Research Engineer",
    "Prompt Engineer",
    "RAG Engineer"
  ],
  "Data": [
    "Data Scientist",
    "Data Scientist Intern",
    "Junior Data Scientist",
    "Applied Data Scientist",
    "Product Data Scientist",
    "Marketing Data Scientist",
    "Data Analyst",
    "Business Intelligence Analyst",
    "BI Developer",
    "Data Engineer",
    "Analytics Engineer",
    "Machine Learning Data Engineer",
    "Data Platform Engineer"
  ],
  "Software Engineering": [
    "Software Engineer",
    "Software Engineer Intern",
    "Backend Engineer",
    "Frontend Engineer",
    "Full Stack Engineer",
    "Mobile App Developer",
    "iOS Developer",
    "Android Developer",
    "Platform Engineer",
    "Systems Engineer",
    "Distributed Systems Engineer",
    "Site Reliability Engineer",
    "API Engineer"
  ],
  "Cloud / DevOps": [
    "Cloud Engineer",
    "DevOps Engineer",
    "Infrastructure Engineer",
    "Kubernetes Engineer",
    "Docker Engineer",
    "Cloud Solutions Architect",
    "AWS Engineer",
    "Azure Engineer",
    "GCP Engineer",
    "Platform Reliability Engineer"
  ],
  "Research": [
    "Research Assistant",
    "AI Research Assistant",
    "Machine Learning Research Assistant",
    "Research Scientist",
    "Applied Scientist",
    "AI Scientist",
    "Data Science Research Intern",
    "Mathematics Research Assistant",
    "Quantitative Research Intern"
  ],
  "Quant / Finance": [
    "Quantitative Researcher",
    "Quantitative Developer",
    "Quantitative Analyst",
    "Trading Analyst",
    "Risk Analyst",
    "Financial Data Scientist",
    "Algorithmic Trading Engineer"
  ],
  "Robotics / Computer Vision": [
    "Robotics Software Engineer",
    "Robotics Engineer",
    "Autonomous Systems Engineer",
    "Computer Vision Research Engineer",
    "SLAM Engineer",
    "Perception Engineer"
  ],
  "Product / Business": [
    "AI Product Manager",
    "Product Manager",
    "Technical Product Manager",
    "Product Analyst",
    "Business Analyst",
    "Strategy Analyst",
    "Operations Analyst"
  ],
  "Cybersecurity": [
    "Cybersecurity Analyst",
    "Security Engineer",
    "Application Security Engineer",
    "Cloud Security Engineer",
    "Security Researcher"
  ],
  "Academic / Teaching": [
    "Teaching Assistant",
    "Mathematics Tutor",
    "Programming Tutor",
    "Academic Tutor",
    "Graduate Teaching Assistant"
  ]
};

const locations = [
  "Hong Kong",
  "Singapore",
  "United States",
  "United Kingdom",
  "Canada",
  "Australia",
  "Japan",
  "South Korea",
  "Taiwan",
  "Mainland China",
  "Germany",
  "France",
  "Netherlands",
  "Switzerland",
  "Ireland",
  "United Arab Emirates",
  "Indonesia",
  "Malaysia",
  "Thailand",
  "Remote - Asia",
  "Remote - Worldwide",
  "Hybrid - Hong Kong",
  "Hybrid - Singapore",
  "Onsite - Hong Kong",
  "Onsite - Singapore"
];

const workTypes = [
  "Full time",
  "Part time",
  "Internship",
  "Contract",
  "Freelance",
  "Graduate Program",
  "Research Assistant",
  "Teaching Assistant",
  "Apprenticeship"
];

const workModes = [
  "Hybrid",
  "Remote",
  "Onsite"
];

function sanitizeText(text) {
  return String(text || "")
    .replace(/‑/g, "-")
    .replace(/–/g, "-")
    .replace(/—/g, "-")
    .replace(/“|”/g, '"')
    .replace(/‘|’/g, "'")
    .replace(/&amp;/g, "&");
}

function getPerformanceMetrics(result) {
  if (!result || !result.polished_bullets?.length) {
    return {
      before: 0,
      after: 0,
      improvement: 0,
      topFit: 0,
      bulletCount: 0
    };
  }

  const before =
    result.polished_bullets.reduce((sum, item) => sum + item.score_before, 0) /
    result.polished_bullets.length;

  const after =
    result.polished_bullets.reduce(
      (sum, item) => sum + item.score_after_estimate,
      0
    ) / result.polished_bullets.length;

  const topFit = result.job_matches?.length
    ? Math.max(...result.job_matches.map((job) => job.fit_score))
    : 0;

  return {
    before,
    after,
    improvement: after - before,
    topFit,
    bulletCount: result.polished_bullets.length
  };
}

function CircleScore({ value, label }) {
  const radius = 44;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - value * circumference;

  return (
    <div className="circle-score">
      <svg width="112" height="112">
        <circle
          cx="56"
          cy="56"
          r={radius}
          className="circle-bg"
        />
        <circle
          cx="56"
          cy="56"
          r={radius}
          className="circle-progress"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
        />
      </svg>
      <div className="circle-content">
        <strong>{Math.round(value * 100)}%</strong>
        <span>{label}</span>
      </div>
    </div>
  );
}

function PerformanceDashboard({ result }) {
  const metrics = getPerformanceMetrics(result);

  return (
    <section className="performance-panel">
      <div>
        <p className="section-kicker">Performance Dashboard</p>
        <h2>Resume Improvement Summary</h2>
        <p className="muted">
          Compare the original bullet quality with the improved version and job-fit score.
        </p>
      </div>

      <div className="performance-grid">
        <CircleScore value={metrics.after} label="After Score" />

        <div className="metric-card">
          <span>Before Score</span>
          <strong>{Math.round(metrics.before * 100)}%</strong>
        </div>

        <div className="metric-card">
          <span>Improvement</span>
          <strong>+{Math.round(metrics.improvement * 100)} pts</strong>
        </div>

        <div className="metric-card">
          <span>Top Job Fit</span>
          <strong>{Math.round(metrics.topFit * 100)}%</strong>
        </div>

        <div className="metric-card">
          <span>Polished Bullets</span>
          <strong>{metrics.bulletCount}</strong>
        </div>
      </div>
    </section>
  );
}

function App() {
  const [resumeText, setResumeText] = useState(sampleResume);
  const [targetRole, setTargetRole] = useState("Machine Learning Engineer");
  const [customTargetRole, setCustomTargetRole] = useState("");
  const [location, setLocation] = useState("Hong Kong");
  const [workType, setWorkType] = useState("Full time");
  const [workMode, setWorkMode] = useState("Hybrid");

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadedFileName, setUploadedFileName] = useState("");
  const [error, setError] = useState("");
  const finalTargetRole =
    targetRole === "Other / Custom Position" ? customTargetRole : targetRole;

  async function uploadResumeFile(event) {
    const file = event.target.files[0];

    setError("");
    setResult(null);
    setUploadedFileName("");

    if (!file) return;

    setUploading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/upload-resume`, {
        method: "POST",
        body: formData
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to upload resume");
      }

      const data = await response.json();

      if (!data.extracted_text) {
        throw new Error("No text was extracted from this file.");
      }

      setResumeText(data.extracted_text);
      setUploadedFileName(file.name);
    } catch (err) {
      setUploadedFileName("");
      setError(err.message || "Something went wrong while uploading the file");
    } finally {
      setUploading(false);
    }
  }

  async function analyzeResume() {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          resume_text: resumeText,
          target_role: finalTargetRole,
          location,
          work_type: workType,
          work_mode: workMode
        })
      });

      if (!response.ok) {
        throw new Error("Failed to analyze resume");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  async function downloadPDF() {
    if (!result) return;

    try {
      setError("");

      const response = await fetch(`${API_BASE_URL}/api/v1/download-report`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(result)
      });

      if (!response.ok) {
        throw new Error("Failed to generate PDF");
      }

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);

      const link = document.createElement("a");
      link.href = url;
      link.download = "resume-polisher-report.pdf";
      link.click();

      URL.revokeObjectURL(url);
    } catch (err) {
      setError(err.message || "Failed to download PDF");
    }
  }  

  return (
    <div className="page">
      <div className="app-container">
        <header className="hero">
          <p className="badge">ML Resume Polisher</p>
          <h1>AI Resume Polisher & Job Matcher</h1>
          <p className="subtitle">
            Paste or upload your resume, select your target job, and get polished
            resume bullets, feedback, and company matches.
          </p>
        </header>

        <main className="layout">
          <section className="card input-card">
            <h2>Resume Input</h2>

            <label>Target Position</label>
            <select
              value={targetRole}
              onChange={(event) => setTargetRole(event.target.value)}
            >
              {Object.entries(targetPositionGroups).map(([groupName, positions]) => (
                <optgroup label={groupName} key={groupName}>
                  {positions.map((position) => (
                    <option value={position} key={position}>
                      {position}
                    </option>
                  ))}
                </optgroup>
              ))}

              <option value="Other / Custom Position">Other / Custom Position</option>
            </select>

            {targetRole === "Other / Custom Position" && (
              <>
                <label>Custom Target Position</label>
                <input
                  value={customTargetRole}
                  onChange={(event) => setCustomTargetRole(event.target.value)}
                  placeholder="Type your target position"
                />
              </>
            )}

            <label>Preferred Location</label>
            <input
              list="location-options"
              value={location}
              onChange={(event) => setLocation(event.target.value)}
              placeholder="Select or type any location"
            />
            <datalist id="location-options">
              {locations.map((item) => (
                <option value={item} key={item} />
              ))}
            </datalist>

            <div className="two-columns">
              <div>
                <label>Work Type</label>
                <select
                  value={workType}
                  onChange={(event) => setWorkType(event.target.value)}
                >
                  {workTypes.map((type) => (
                    <option value={type} key={type}>
                      {type}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label>Work Mode</label>
                <select
                  value={workMode}
                  onChange={(event) => setWorkMode(event.target.value)}
                >
                  {workModes.map((mode) => (
                    <option value={mode} key={mode}>
                      {mode}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <label>Upload Resume File</label>
            <input
              type="file"
              accept=".pdf,.docx"
              onChange={uploadResumeFile}
            />

            {uploading && <p className="info">Extracting resume text...</p>}

            {uploadedFileName && (
              <p className="info">
                Uploaded file: <strong>{uploadedFileName}</strong>
              </p>
            )}

            <label>Resume Text</label>
            <textarea
              value={resumeText}
              onChange={(event) => setResumeText(event.target.value)}
              placeholder="Resume text will appear here after upload."
            />

            <button
              onClick={analyzeResume}
              disabled={
                loading ||
                uploading ||
                (targetRole === "Other / Custom Position" && !customTargetRole.trim())
              }
            >

              {loading ? "Analyzing..." : "Analyze Resume"}
            </button>

            {error && <p className="error">{error}</p>}
          </section>

          <section className="card output-card">
            <div className="output-header">
              <h2>Output</h2>
              <button
                className="secondary-button"
                onClick={downloadPDF}
                disabled={!result}
              >
                Download PDF
              </button>
            </div>

            {!result && (
              <div className="empty-state">
                Your polished bullets, feedback, and job matches will appear here.
              </div>
            )}

            {result && (
              <div className="results">
                <PerformanceDashboard result={result} />

                <h3>Polished Bullets</h3>

                {result.polished_bullets.map((item, index) => (
                  <div className="result-box" key={index}>
                    <p className="original">
                      <strong>Original:</strong> {item.original}
                    </p>

                    <p className="polished">
                      <strong>Polished:</strong> {item.polished}
                    </p>

                    <p>
                      <strong>Score:</strong>{" "}
                      {Math.round(item.score_before * 100)}% →{" "}
                      {Math.round(item.score_after_estimate * 100)}%
                    </p>

                    <ul>
                      {item.feedback.map((feedbackItem, feedbackIndex) => (
                        <li key={feedbackIndex}>{feedbackItem}</li>
                      ))}
                    </ul>
                  </div>
                ))}

                <h3>Suggested Job Matches</h3>

                <div className="jobs">
                  {result.job_matches.map((job, index) => (
                    <div className="job-card" key={index}>
                      <h4>{job.company}</h4>
                      <p className="job-role">{job.role}</p>
                      <p>{job.location}</p>
                      <p>
                        {job.work_type} · {job.work_mode}
                      </p>
                      <p>
                        <strong>Fit:</strong> {Math.round(job.fit_score * 100)}%
                      </p>

                      <ul>
                        {job.reasons.map((reason, reasonIndex) => (
                          <li key={reasonIndex}>{reason}</li>
                        ))}
                      </ul>

                      <a href={job.career_url} target="_blank" rel="noreferrer">
                        Open Career Page
                      </a>
                    </div>
                  ))}
                </div>

                <h3>Summary Feedback</h3>
                <ul>
                  {result.summary_feedback.map((feedbackItem, index) => (
                    <li key={index}>{feedbackItem}</li>
                  ))}
                </ul>
              </div>
            )}
          </section>
        </main>
      </div>
    </div>
  );
}

export default App;