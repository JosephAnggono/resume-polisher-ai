import { useState } from "react";
import "./App.css";

const API_BASE_URL = "http://127.0.0.1:8000";

const sampleResume = `Data Science Intern, ABC Startup
- Made dashboard for sales team
- Used Python to clean data
- Helped model customer churn`;

function App() {
  const [resumeText, setResumeText] = useState(sampleResume);
  const [targetRole, setTargetRole] = useState("Machine Learning Engineer");
  const [location, setLocation] = useState("Hong Kong");
  const [workType, setWorkType] = useState("Full time");
  const [workMode, setWorkMode] = useState("Hybrid");

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [uploading, setUploading] = useState(false);
  const [uploadedFileName, setUploadedFileName] = useState("");

  async function uploadResumeFile(event) {
    const file = event.target.files[0];

    if (!file) return;

    setUploading(true);
    setError("");
    setResult(null);
    setUploadedFileName(file.name);

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

      setResumeText(data.extracted_text);
    } catch (err) {
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
          target_role: targetRole,
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

  function downloadResult() {
    if (!result) return;

    const polishedBullets = result.polished_bullets
      .map((item) => item.polished)
      .join("\n");

    const feedback = result.polished_bullets
      .map((item, index) => {
        return `${index + 1}. Original: ${item.original}
Polished: ${item.polished}
Score: ${Math.round(item.score_before * 100)}% → ${Math.round(
          item.score_after_estimate * 100
        )}%
Feedback:
${item.feedback.map((f) => `- ${f}`).join("\n")}`;
      })
      .join("\n\n");

    const jobMatches = result.job_matches
      .map((job) => {
        return `${job.company} - ${job.role}
Location: ${job.location}
Work Type: ${job.work_type}
Work Mode: ${job.work_mode}
Fit Score: ${Math.round(job.fit_score * 100)}%
Career URL: ${job.career_url}
Reasons:
${job.reasons.map((r) => `- ${r}`).join("\n")}`;
      })
      .join("\n\n");

    const content = `Resume Polisher AI Result

Target Role: ${result.target_role}
Location: ${result.location}
Work Type: ${result.work_type}
Work Mode: ${result.work_mode}

==============================
POLISHED BULLETS
==============================

${polishedBullets}

==============================
FEEDBACK
==============================

${feedback}

==============================
JOB MATCHES
==============================

${jobMatches}

==============================
SUMMARY FEEDBACK
==============================

${result.summary_feedback.map((item) => `- ${item}`).join("\n")}
`;

    const blob = new Blob([content], { type: "text/plain" });
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = "resume-polisher-result.txt";
    link.click();

    URL.revokeObjectURL(url);
  }

  return (
    <div className="page">
      <header className="hero">
        <p className="badge">ML Resume Polisher</p>
        <h1>AI Resume Polisher & Job Matcher</h1>
        <p className="subtitle">
          Paste your resume, select your target job, and get polished resume
          bullets, feedback, and company matches.
        </p>
      </header>

      <main className="layout">
        <section className="card input-card">
          <h2>Resume Input</h2>

          <label>Target Position</label>
          <input
            value={targetRole}
            onChange={(e) => setTargetRole(e.target.value)}
          />

          <label>Preferred Location</label>
          <input
            value={location}
            onChange={(e) => setLocation(e.target.value)}
          />

          <div className="two-columns">
            <div>
              <label>Work Type</label>
              <select
                value={workType}
                onChange={(e) => setWorkType(e.target.value)}
              >
                <option>Full time</option>
                <option>Part time</option>
                <option>Internship</option>
              </select>
            </div>

            <div>
              <label>Work Mode</label>
              <select
                value={workMode}
                onChange={(e) => setWorkMode(e.target.value)}
              >
                <option>Hybrid</option>
                <option>Remote</option>
                <option>Onsite</option>
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
            onChange={(e) => setResumeText(e.target.value)}
          />

          <button onClick={analyzeResume} disabled={loading}>
            {loading ? "Analyzing..." : "Analyze Resume"}
          </button>

          {error && <p className="error">{error}</p>}
        </section>

        <section className="card output-card">
          <div className="output-header">
            <h2>Output</h2>
            <button
              className="secondary-button"
              onClick={downloadResult}
              disabled={!result}
            >
              Download Result
            </button>
          </div>

          {!result && (
            <div className="empty-state">
              Your polished bullets, feedback, and job matches will appear here.
            </div>
          )}

          {result && (
            <div className="results">
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
  );
}

export default App;