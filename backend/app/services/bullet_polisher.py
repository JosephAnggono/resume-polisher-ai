from typing import Dict
from app.services.resume_scorer import score_bullet


def polish_bullet(bullet: str, target_role: str) -> Dict:
    clean = bullet.strip().lstrip("-•* ").strip()
    lower = clean.lower()

    if "dashboard" in lower:
        polished = (
            "Developed an interactive analytics dashboard using Python/BI tooling "
            "to help stakeholders monitor key business trends; add metric such as "
            "users served or reporting time saved."
        )

    elif "clean" in lower or "preprocess" in lower:
        polished = (
            "Built reproducible Python data preprocessing pipelines to transform "
            "raw datasets into model-ready features; add metric such as processing "
            "time reduced or rows handled."
        )

    elif "churn" in lower:
        polished = (
            f"Contributed to a customer churn prediction workflow for a {target_role} "
            "context by preparing features, training baseline models, and communicating "
            "retention insights; add model metric if available."
        )

    elif "model" in lower or "classifier" in lower or "machine learning" in lower:
        polished = (
            f"Designed and evaluated a supervised ML model for {target_role} applications, "
            "covering feature engineering, validation, error analysis, and experiment tracking."
        )

    elif "accuracy" in lower:
        polished = (
            "Improved model performance through feature iteration and hyperparameter tuning; "
            "specify before/after accuracy or another evaluation metric."
        )

    else:
        polished = (
            f"Strengthened {target_role}-relevant contribution: {clean}; "
            "add technical method, measurable outcome, and user/business impact."
        )

    before = score_bullet(bullet)
    after = score_bullet("- " + polished)

    score_after_estimate = max(
        after["overall_score"],
        min(before["overall_score"] + 0.25, 0.95)
    )

    return {
        "original": bullet,
        "polished": "- " + polished,
        "feedback": before["feedback"],
        "score_before": before["overall_score"],
        "score_after_estimate": round(score_after_estimate, 2),
    }
