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
- Dockerized frontend and backend

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
- TF-IDF vector-based job matching
- Cosine similarity ranking
- Skill gap feedback
- Deterministic bullet rewriting baseline

### DevOps

- Docker
- Docker Compose

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
│   ├── Dockerfile
│   ├── .dockerignore
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── App.css
│   ├── Dockerfile
│   ├── .dockerignore
│   └── package.json
├── docker-compose.yml
├── README.md
└── .gitignore
```

## API Endpoints

```text
GET  /health
POST /api/v1/extract-bullets
POST /api/v1/score-resume
POST /api/v1/polish-bullets
POST /api/v1/match-jobs
POST /api/v1/analyze
```

## Run Locally

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend API:

```text
http://127.0.0.1:8000/docs
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173/
```

## Run with Docker

From the project root:

```bash
docker compose up --build
```

Frontend:

```text
http://localhost:5173
```

Backend API:

```text
http://localhost:8000/docs
```

Stop containers:

```bash
docker compose down
```

## System Flow

```text
User Input
   ↓
React Frontend
   ↓
FastAPI Backend
   ↓
Resume Parser
   ↓
Bullet Scorer
   ↓
Bullet Polisher
   ↓
Job Matcher
   ↓
JSON Response
   ↓
Frontend Output + Download
```

## Current Status

The current version is a full-stack MVP. It supports PDF/DOCX resume upload, text extraction, bullet extraction, scoring, rewriting, feedback generation, TF-IDF vector-based job matching, Dockerized local execution, and result download.

## Planned Improvements

- PDF and DOCX resume upload
- Resume section extraction
- Transformer embedding job matching
- Vector database retrieval
- LLM-based bullet rewriting
- Skill gap analysis
- User authentication
- CI/CD pipeline
- Kubernetes orchestration

## ML Engineering Focus

This project demonstrates full-stack ML application development, API design, NLP preprocessing, rule-based ML baselines, resume scoring, job matching, containerization, and deployment preparation.