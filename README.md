# Resume Polisher AI

AI-powered resume optimization and job matching application.

## Overview

Resume Polisher AI helps users improve resume bullet points for a target role. Users paste their resume, select job preferences, and receive polished bullet points, feedback, scoring, and suggested job matches.

## Features

- Resume text input
- Target role, location, work type, and work mode selection
- Resume bullet extraction
- Bullet quality scoring
- Resume bullet rewriting
- Resume improvement feedback
- Sample job matching
- Downloadable result file

## Tech Stack

### Frontend
- React
- Vite
- CSS

### Backend
- Python
- FastAPI
- Pydantic
- Uvicorn

### ML / NLP Logic
- Rule-based bullet extraction
- Resume scoring heuristics
- Keyword-based job matching
- Deterministic bullet rewriting baseline

## Project Structure

```text
resume-polisher-ai/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── schemas.py
│   │   └── services/
│   │       ├── resume_parser.py
│   │       ├── resume_scorer.py
│   │       ├── bullet_polisher.py
│   │       └── job_matcher.py
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── App.jsx
│       └── App.css
├── README.md
└── .gitignore