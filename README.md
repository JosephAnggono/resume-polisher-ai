# Resume Polisher AI

A full-stack web app that reviews a resume against a target role: it pulls out the bullet
points, scores each one, suggests a stronger rewrite, and ranks sample job postings by how
well they match.

**Stack:** React (Vite) · FastAPI · scikit-learn · PyMuPDF / python-docx · ReportLab · Docker Compose

## What it does

1. **Upload or paste a resume** (PDF, DOCX or plain text) and choose a target role, location,
   work type and work mode.
2. **Extract bullet points** with a rule-based parser that recognises section headings and
   bullet markers.
3. **Score each bullet** on action verbs, measurable results and role keywords.
4. **Rewrite weak bullets** with a deterministic baseline, plus feedback on what to fix.
5. **Match jobs**: rank a set of sample postings by TF-IDF cosine similarity to the resume
   and list the skills each posting asks for that the resume does not mention.
6. **Download a PDF report** of the scores, rewrites and matches.

```text
React frontend → FastAPI → parse → score → rewrite → match jobs → JSON / PDF report
```

## Run it

With Docker (from the project root):

```bash
docker compose up --build
```

- App: http://localhost:5173
- API docs: http://localhost:8000/docs

Without Docker:

```bash
# backend
cd backend
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload

# frontend (second terminal)
cd frontend
npm install
npm run dev
```

Tests: `cd backend && pytest -q`

## API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/api/v1/upload-resume` | Extract text from a PDF or DOCX |
| POST | `/api/v1/extract-bullets` | Find bullet points in resume text |
| POST | `/api/v1/score-resume` | Score a list of bullets |
| POST | `/api/v1/polish-bullets` | Suggest rewrites |
| POST | `/api/v1/match-jobs` | Rank sample jobs by similarity |
| POST | `/api/v1/analyze` | Run the full pipeline in one call |
| POST | `/api/v1/download-report` | Return the results as a PDF |

## Project layout

```text
backend/app/
  main.py                 FastAPI routes
  schemas.py              request and response models
  services/
    document_parser.py    PDF / DOCX text extraction
    resume_parser.py      bullet extraction
    resume_scorer.py      bullet scoring
    bullet_polisher.py    rewrite suggestions
    job_matcher.py        TF-IDF job matching and skill gaps
    pdf_report.py         PDF report
backend/tests/            API tests (pytest)
frontend/src/             React interface
```

## Limitations

- Scoring and rewriting are rule-based baselines, not a trained or LLM model.
- Job matching runs against a built-in set of sample postings, not live listings.

## Next steps

- Replace TF-IDF with sentence embeddings for job matching.
- Add an LLM rewriting option and compare it with the rule-based baseline.
- Connect a real job source and add continuous integration.
