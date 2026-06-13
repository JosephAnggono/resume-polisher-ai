from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import ResumeRequest, BulletRequest, AnalyzeResponse
from app.services.resume_parser import extract_bullets
from app.services.resume_scorer import score_bullet
from app.services.bullet_polisher import polish_bullet
from app.services.job_matcher import match_jobs


app = FastAPI(
    title="Resume Polisher AI API",
    description="Backend MVP for AI resume bullet polishing and job matching.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "resume-polisher-ai"
    }


@app.post("/api/v1/extract-bullets")
def extract_resume_bullets(request: ResumeRequest):
    bullets = extract_bullets(request.resume_text)
    return {
        "bullets": bullets,
        "count": len(bullets)
    }


@app.post("/api/v1/score-resume")
def score_resume(request: BulletRequest):
    scores = [score_bullet(bullet) for bullet in request.bullets]
    average = round(
        sum(item["overall_score"] for item in scores) / len(scores),
        2
    ) if scores else 0

    return {
        "average_score": average,
        "scores": scores
    }


@app.post("/api/v1/polish-bullets")
def polish_resume_bullets(request: BulletRequest):
    polished = [
        polish_bullet(bullet, request.target_role)
        for bullet in request.bullets
    ]

    return {
        "polished_bullets": polished
    }


@app.post("/api/v1/match-jobs")
def match_relevant_jobs(request: ResumeRequest):
    jobs = match_jobs(
        resume_text=request.resume_text,
        target_role=request.target_role,
        location=request.location,
        work_type=request.work_type,
        work_mode=request.work_mode,
    )

    return {
        "job_matches": jobs
    }


@app.post("/api/v1/analyze", response_model=AnalyzeResponse)
def analyze_resume(request: ResumeRequest):
    bullets = extract_bullets(request.resume_text)

    polished = [
        polish_bullet(bullet, request.target_role)
        for bullet in bullets
    ]

    jobs = match_jobs(
        resume_text=request.resume_text,
        target_role=request.target_role,
        location=request.location,
        work_type=request.work_type,
        work_mode=request.work_mode,
    )

    summary_feedback = []

    if not bullets:
        summary_feedback.append(
            "No bullet points were detected. Use '-' or '•' at the beginning of each resume bullet."
        )

    if bullets:
        average_before = sum(
            item["score_before"]
            for item in polished
        ) / len(polished)

        if average_before < 0.55:
            summary_feedback.append(
                "Your resume bullets need more measurable impact, technical keywords, and stronger action verbs."
            )

    summary_feedback.append(
        "Next version should compare your resume against real job descriptions using embeddings and vector search."
    )

    return AnalyzeResponse(
        target_role=request.target_role,
        location=request.location,
        work_type=request.work_type,
        work_mode=request.work_mode,
        extracted_bullets=bullets,
        polished_bullets=polished,
        job_matches=jobs,
        summary_feedback=summary_feedback,
    )
