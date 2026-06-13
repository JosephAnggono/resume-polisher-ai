import re
from typing import Dict, List


TECH_KEYWORDS = {
    "python", "sql", "pandas", "numpy", "scikit-learn", "sklearn",
    "pytorch", "tensorflow", "docker", "fastapi", "api", "aws",
    "azure", "gcp", "mlflow", "airflow", "spark", "feature",
    "model", "embedding", "rag"
}

IMPACT_WORDS = {
    "improved", "reduced", "increased", "optimized", "automated",
    "enabled", "deployed", "saved", "scaled", "launched"
}

ACTION_VERBS = {
    "built", "developed", "designed", "implemented", "created",
    "trained", "deployed", "optimized", "analyzed", "engineered",
    "automated", "evaluated", "integrated"
}


def contains_metric(text: str) -> bool:
    return bool(
        re.search(
            r"(\d+|%|x\b|times|hours|days|users|accuracy|latency|cost)",
            text.lower()
        )
    )


def keyword_score(text: str, keywords: set[str]) -> float:
    lowered = text.lower()
    hits = sum(1 for keyword in keywords if keyword in lowered)
    return min(hits / 3, 1.0)


def score_bullet(bullet: str) -> Dict:
    text = bullet.strip("-•* ").strip()
    words = text.split()

    first_word = words[0].lower() if words else ""
    starts_with_action = first_word in ACTION_VERBS
    length_good = 10 <= len(words) <= 35

    clarity_score = 0.5
    if starts_with_action:
        clarity_score += 0.25
    if length_good:
        clarity_score += 0.25

    metric_score = 1.0 if contains_metric(text) else 0.0
    technical_score = keyword_score(text, TECH_KEYWORDS)
    impact_score = keyword_score(text, IMPACT_WORDS)

    overall = round(
        clarity_score * 0.25
        + metric_score * 0.25
        + technical_score * 0.25
        + impact_score * 0.25,
        2
    )

    feedback: List[str] = []

    if not starts_with_action:
        feedback.append(
            "Start with a stronger action verb such as Built, Developed, Designed, Implemented, or Deployed."
        )

    if not metric_score:
        feedback.append(
            "Add a measurable result, such as accuracy, latency, cost reduction, users served, or time saved."
        )

    if technical_score < 0.34:
        feedback.append(
            "Mention relevant tools or ML methods, such as Python, SQL, PyTorch, scikit-learn, embeddings, APIs, or cloud services."
        )

    if impact_score < 0.34:
        feedback.append(
            "Explain the business or user impact instead of only describing the task."
        )

    if not feedback:
        feedback.append(
            "Strong bullet. Next, tailor keywords to the exact job description."
        )

    return {
        "bullet": bullet,
        "clarity_score": round(min(clarity_score, 1.0), 2),
        "metric_score": round(metric_score, 2),
        "technical_score": round(technical_score, 2),
        "impact_score": round(impact_score, 2),
        "overall_score": overall,
        "feedback": feedback,
    }
