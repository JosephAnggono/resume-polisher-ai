import re
from typing import List, Optional


BULLET_MARKERS = {"-", "•", "*", "‣", "◦", "▪", "▫", "●"}

ACTION_VERBS = {
    "built",
    "developed",
    "designed",
    "implemented",
    "created",
    "trained",
    "deployed",
    "optimized",
    "analyzed",
    "engineered",
    "automated",
    "evaluated",
    "integrated",
    "conducted",
    "mentored",
    "coordinated",
    "contributed",
    "improved",
    "led",
    "managed",
    "researched",
    "implemented",
}


def is_section_heading(line: str) -> bool:
    cleaned = line.strip()

    if not cleaned:
        return False

    common_headings = {
        "EDUCATION",
        "WORKING EXPERIENCE",
        "WORK EXPERIENCE",
        "LEADERSHIP EXPERIENCE",
        "ACHIEVEMENTS",
        "ADDITIONAL INFORMATION",
        "TECHNICAL SKILLS",
        "SKILLS",
        "INTERESTS",
        "PROJECTS",
        "EXPERIENCE",
        "CERTIFICATIONS",
        "PUBLICATIONS",
        "SUMMARY",
        "PROFILE",
        "AWARDS",
        "ACTIVITIES",
        "VOLUNTEERING",
    }

    return cleaned.upper() in common_headings


def is_bullet_marker_only(line: str) -> bool:
    return line.strip() in BULLET_MARKERS


def is_bullet_with_text(line: str) -> bool:
    return bool(re.match(r"^([-•*‣◦▪▫●]|\d+[.)])\s+.+", line.strip()))


def clean_bullet_prefix(line: str) -> str:
    return re.sub(r"^([-•*‣◦▪▫●]|\d+[.)])\s+", "", line.strip()).strip()


def should_skip_bullet(bullet: Optional[str]) -> bool:
    """
    Skip bullets that are not achievement/experience/project bullets.

    Examples skipped:
    - Programming: Python, C++, MATLAB
    - Languages: English, Mandarin, Indonesian
    - AI/ML Frameworks: PyTorch, TensorFlow
    - Cover-letter paragraphs accidentally merged into resume bullets
    """

    if not bullet:
        return True

    text = str(bullet).lower().strip("-•* ").strip()

    if not text:
        return True

    skip_prefixes = [
        "languages:",
        "programming:",
        "programming &",
        "tools:",
        "tools &",
        "ai/ml",
        "llm &",
        "data:",
        "mathematics:",
        "interests",
        "technical skills",
        "frameworks:",
        "mlops",
        "skills:",
        "awards:",
    ]

    if any(text.startswith(prefix) for prefix in skip_prefixes):
        return True

    cover_letter_phrases = [
        "sincerely",
        "thank you for considering",
        "my curriculum vitae is attached",
        "i welcome the opportunity",
        "i am deeply impressed",
        "dear hiring manager",
        "dear recruiter",
        "to whom it may concern",
    ]

    if any(phrase in text for phrase in cover_letter_phrases):
        return True

    words = text.split()
    first_word = words[0] if words else ""

    looks_like_skill_list = ":" in text and text.count(",") >= 2

    if looks_like_skill_list and first_word not in ACTION_VERBS:
        return True

    return False


def append_current_bullet(
    bullets: List[str],
    current_bullet: Optional[str]
) -> None:
    """
    Safely append current bullet only if it exists and should not be skipped.
    """

    if current_bullet and not should_skip_bullet(current_bullet):
        bullets.append(current_bullet)


def extract_bullets(resume_text: str) -> List[str]:
    """
    Extract bullet points from resume text.

    Handles:
    1. Normal bullets:
       - Built ML model

    2. PDF-extracted bullets where marker is on its own line:
       •
       Built ML model

    3. Wrapped bullet lines:
       •
       Built ML model using Python and PyTorch
       to improve classification performance
    """

    raw_lines = [line.strip() for line in resume_text.splitlines()]
    bullets: List[str] = []

    current_bullet: Optional[str] = None
    waiting_for_bullet_text = False

    for line in raw_lines:
        if not line:
            append_current_bullet(bullets, current_bullet)
            current_bullet = None
            waiting_for_bullet_text = False
            continue

        if is_section_heading(line):
            append_current_bullet(bullets, current_bullet)
            current_bullet = None
            waiting_for_bullet_text = False
            continue

        if is_bullet_marker_only(line):
            append_current_bullet(bullets, current_bullet)
            current_bullet = None
            waiting_for_bullet_text = True
            continue

        if is_bullet_with_text(line):
            append_current_bullet(bullets, current_bullet)

            bullet_text = clean_bullet_prefix(line)
            current_bullet = f"- {bullet_text}"
            waiting_for_bullet_text = False
            continue

        if waiting_for_bullet_text:
            current_bullet = f"- {line}"
            waiting_for_bullet_text = False
            continue

        if current_bullet:
            current_bullet = f"{current_bullet} {line}"

    append_current_bullet(bullets, current_bullet)

    return bullets