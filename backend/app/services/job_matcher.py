from typing import Dict, List, Set

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


SAMPLE_JOBS = [
    {
        "company": "Google",
        "role": "Machine Learning Engineer Intern",
        "location": "Hong Kong / Singapore",
        "work_type": "Internship",
        "work_mode": "Hybrid",
        "career_url": "https://careers.google.com/",
        "description": (
            "Machine learning internship focused on Python, data preprocessing, "
            "model training, evaluation, TensorFlow, PyTorch, statistical learning, "
            "experimentation, and scalable ML systems."
        ),
        "required_skills": {
            "python",
            "machine learning",
            "data preprocessing",
            "model evaluation",
            "tensorflow",
            "pytorch",
            "statistics",
        },
    },
    {
        "company": "NVIDIA",
        "role": "Deep Learning Software Engineer",
        "location": "Hong Kong / Taiwan / Remote Asia",
        "work_type": "Full time",
        "work_mode": "Hybrid",
        "career_url": "https://www.nvidia.com/en-us/about-nvidia/careers/",
        "description": (
            "Deep learning engineering role involving PyTorch, CUDA, computer vision, "
            "model optimization, GPU acceleration, numerical methods, deployment, "
            "and high-performance machine learning systems."
        ),
        "required_skills": {
            "python",
            "pytorch",
            "deep learning",
            "computer vision",
            "model optimization",
            "deployment",
            "numerical methods",
        },
    },
    {
        "company": "Apple",
        "role": "Applied Machine Learning Engineer",
        "location": "Singapore / US / UK",
        "work_type": "Full time",
        "work_mode": "Onsite",
        "career_url": "https://jobs.apple.com/",
        "description": (
            "Applied machine learning role focused on model development, NLP, "
            "experimentation, data analysis, Python, production ML pipelines, "
            "evaluation metrics, and user-facing intelligent systems."
        ),
        "required_skills": {
            "python",
            "machine learning",
            "nlp",
            "experimentation",
            "data analysis",
            "model development",
            "production ml",
        },
    },
    {
        "company": "Microsoft",
        "role": "AI Engineer",
        "location": "Hong Kong / Japan / US",
        "work_type": "Full time",
        "work_mode": "Hybrid",
        "career_url": "https://jobs.careers.microsoft.com/",
        "description": (
            "AI engineering role involving Python, Azure, FastAPI, APIs, RAG, "
            "vector embeddings, LLM applications, deployment, monitoring, "
            "and production-grade AI systems."
        ),
        "required_skills": {
            "python",
            "azure",
            "fastapi",
            "api",
            "rag",
            "vector embeddings",
            "deployment",
            "monitoring",
        },
    },
    {
        "company": "ByteDance",
        "role": "Machine Learning Engineer",
        "location": "Hong Kong / Singapore",
        "work_type": "Full time",
        "work_mode": "Onsite",
        "career_url": "https://jobs.bytedance.com/",
        "description": (
            "Machine learning engineering role focused on recommendation systems, "
            "large-scale data processing, Python, SQL, model training, ranking, "
            "online experimentation, and ML infrastructure."
        ),
        "required_skills": {
            "python",
            "sql",
            "recommendation systems",
            "ranking",
            "model training",
            "large-scale data",
            "experimentation",
        },
    },
]


def normalize_text(text: str) -> str:
    return text.lower().replace("‑", "-").replace("–", "-")


def find_skill_matches(
    resume_text: str,
    required_skills: Set[str]
) -> Dict[str, List[str]]:
    normalized_resume = normalize_text(resume_text)

    matched_skills = []
    missing_skills = []

    for skill in sorted(required_skills):
        if skill.lower() in normalized_resume:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
    }


def compute_similarity_scores(
    query_text: str,
    job_descriptions: List[str]
) -> List[float]:
    documents = [query_text] + job_descriptions

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2)
    )

    tfidf_matrix = vectorizer.fit_transform(documents)

    query_vector = tfidf_matrix[0:1]
    job_vectors = tfidf_matrix[1:]

    similarities = cosine_similarity(query_vector, job_vectors).flatten()

    return similarities.tolist()


def match_jobs(
    resume_text: str,
    target_role: str,
    location: str,
    work_type: str,
    work_mode: str
) -> List[Dict]:
    query_text = (
        f"Target role: {target_role}. "
        f"Preferred location: {location}. "
        f"Work type: {work_type}. "
        f"Work mode: {work_mode}. "
        f"Resume: {resume_text}"
    )

    job_descriptions = [
        (
            f"{job['role']} "
            f"{job['description']} "
            f"{job['location']} "
            f"{job['work_type']} "
            f"{job['work_mode']}"
        )
        for job in SAMPLE_JOBS
    ]

    similarity_scores = compute_similarity_scores(query_text, job_descriptions)

    matches = []

    for job, similarity in zip(SAMPLE_JOBS, similarity_scores):
        skill_result = find_skill_matches(resume_text, job["required_skills"])

        location_bonus = 0.08 if location.lower() in job["location"].lower() else 0
        work_type_bonus = 0.04 if work_type.lower() == job["work_type"].lower() else 0
        work_mode_bonus = 0.04 if work_mode.lower() == job["work_mode"].lower() else 0

        if job["required_skills"]:
            skill_coverage = len(skill_result["matched_skills"]) / len(job["required_skills"])
        else:
            skill_coverage = 0

        fit_score = round(
            min(
                0.35
                + similarity * 0.35
                + skill_coverage * 0.18
                + location_bonus
                + work_type_bonus
                + work_mode_bonus,
                0.98
            ),
            2
        )

        reasons = [
            f"Vector similarity score: {round(similarity, 3)}."
        ]

        if skill_result["matched_skills"]:
            reasons.append(
                "Matched skills: "
                + ", ".join(skill_result["matched_skills"])
                + "."
            )

        if skill_result["missing_skills"]:
            reasons.append(
                "Missing or weak skills to improve: "
                + ", ".join(skill_result["missing_skills"][:5])
                + "."
            )

        if location_bonus:
            reasons.append("Location preference overlaps with this role.")

        if work_type_bonus or work_mode_bonus:
            reasons.append("Work type or work mode preference is aligned.")

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