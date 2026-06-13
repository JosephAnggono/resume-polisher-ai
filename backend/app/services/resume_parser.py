import re
from typing import List


def extract_bullets(resume_text: str) -> List[str]:
    bullets = []

    for raw_line in resume_text.splitlines():
        line = raw_line.strip()

        if not line:
            continue

        if re.match(r"^([-•*]|\d+[.)])\s+", line):
            normalized = re.sub(r"^([-•*]|\d+[.)])\s+", "- ", line)
            bullets.append(normalized)

    return bullets
