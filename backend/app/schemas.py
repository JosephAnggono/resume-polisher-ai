from typing import List
from pydantic import BaseModel, Field


class UserPreferences(BaseModel):
    target_role: str = Field(..., examples=["Machine Learning Engineer"])
    location: str = Field(..., examples=["Hong Kong"])
    work_type: str = Field(default="Full time")
    work_mode: str = Field(default="Hybrid")


class ResumeRequest(UserPreferences):
    resume_text: str = Field(..., min_length=10)


class BulletRequest(UserPreferences):
    bullets: List[str] = Field(..., min_length=1)


class PolishedBullet(BaseModel):
    original: str
    polished: str
    feedback: List[str]
    score_before: float
    score_after_estimate: float


class JobMatch(BaseModel):
    company: str
    role: str
    location: str
    work_type: str
    work_mode: str
    fit_score: float
    career_url: str
    reasons: List[str]


class AnalyzeResponse(BaseModel):
    target_role: str
    location: str
    work_type: str
    work_mode: str
    extracted_bullets: List[str]
    polished_bullets: List[PolishedBullet]
    job_matches: List[JobMatch]
    summary_feedback: List[str]
