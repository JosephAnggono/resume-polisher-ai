from typing import List, Dict


SAMPLE_JOBS = [
    {
        "company": "Google",
        "role": "Machine Learning Engineer Intern",
        "location": "Hong Kong / Singapore",
        "work_type": "Internship",
        "work_mode": "Hybrid",
        "career_url": "https://careers.google.com/",
        "keywords": {"python", "machine learning", "data", "model", "tensorflow", "pytorch"},
    },
    {
        "company": "NVIDIA",
        "role": "Deep Learning Software Engineer",
        "location": "Hong Kong / Taiwan / Remote Asia",
        "work_type": "Full time",
        "work_mode": "Hybrid",
        "career_url": "https://www.nvidia.com/en-us/about-nvidia/careers/",
        "keywords": {"python", "deep learning", "pytorch", "cuda", "model", "optimization"},
    },
    {
        "company": "Apple",
        "role": "Applied Machine Learning Engineer",
        "location": "Singapore / US / UK",
        "work_type": "Full time",
        "work_mode": "Onsite",
        "career_url": "https://jobs.apple.com/",
        "keywords": {"machine learning", "nlp", "python", "model", "experimentation"},
    },
    {
        "company": "Microsoft",
        "role": "AI Engineer",
        "location": "Hong Kong / Japan / US",
        "work_type": "Full time",
        "work_mode": "Hybrid",
        "career_url": "https://jobs.careers.microsoft.com/",
        "keywords": {"python", "azure", "api", "machine learning", "rag", "deployment"},
    },
]


def match_jobs(
    resume_text: str,
    target_role: str,
    location: str,
    work_type: str,
    work_mode: str
) -> List[Dict]:
    text = f"{resume_text} {target_role} {location} {work_type} {work_mode}".lower()
    matches = []

    for job in SAMPLE_JOBS:
        keyword_hits = [keyword for keyword in job["keywords"] if keyword in text]

        role_bonus = 0.15 if any(
            token in job["role"].lower()
            for token in target_role.lower().split()
        ) else 0

        location_bonus = 0.10 if location.lower() in job["location"].lower() else 0
        type_bonus = 0.05 if work_type.lower() == job["work_type"].lower() else 0
        mode_bonus = 0.05 if work_mode.lower() == job["work_mode"].lower() else 0

        keyword_score = min(len(keyword_hits) / max(len(job["keywords"]), 1), 1.0)

        fit_score = round(
            min(
                0.45
                + keyword_score * 0.35
                + role_bonus
                + location_bonus
                + type_bonus
                + mode_bonus,
                0.98
            ),
            2
        )

        reasons = []

        if keyword_hits:
            reasons.append(f"Matched keywords: {', '.join(sorted(keyword_hits))}.")

        if location_bonus:
            reasons.append("Location preference overlaps with this role.")

        if type_bonus or mode_bonus:
            reasons.append("Work type/mode preference is partially aligned.")

        if not reasons:
            reasons.append("General role similarity based on target position.")

        matches.append({
            "company": job["company"],
            "role": job["role"],
            "location": job["location"],
            "work_type": job["work_type"],
            "work_mode": job["work_mode"],
            "fit_score": fit_score,
            "career_url": job["career_url"],
            "reasons": reasons,
        })

    return sorted(matches, key=lambda item: item["fit_score"], reverse=True)
