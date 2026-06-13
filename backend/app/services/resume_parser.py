import re
from typing import List


BULLET_MARKERS = {"-", "•", "*", "‣", "◦", "▪", "▫", "●"}


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
    }

    return cleaned.upper() in common_headings


def is_bullet_marker_only(line: str) -> bool:
    return line.strip() in BULLET_MARKERS


def is_bullet_with_text(line: str) -> bool:
    return bool(re.match(r"^([-•*‣◦▪▫●]|\d+[.)])\s+.+", line.strip()))


def clean_bullet_prefix(line: str) -> str:
    return re.sub(r"^([-•*‣◦▪▫●]|\d+[.)])\s+", "", line.strip()).strip()


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
    bullets = []

    current_bullet = None
    waiting_for_bullet_text = False

    for line in raw_lines:
        if not line:
            if current_bullet:
                bullets.append(current_bullet)
                current_bullet = None
            waiting_for_bullet_text = False
            continue

        if is_section_heading(line):
            if current_bullet:
                bullets.append(current_bullet)
                current_bullet = None
            waiting_for_bullet_text = False
            continue

        if is_bullet_marker_only(line):
            if current_bullet:
                bullets.append(current_bullet)
                current_bullet = None
            waiting_for_bullet_text = True
            continue

        if is_bullet_with_text(line):
            if current_bullet:
                bullets.append(current_bullet)

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

    if current_bullet:
        bullets.append(current_bullet)

    return bullets