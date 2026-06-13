from io import BytesIO
from typing import Optional

import fitz
from docx import Document


def extract_text_from_pdf(file_bytes: bytes) -> str:
    text_parts = []

    with fitz.open(stream=file_bytes, filetype="pdf") as document:
        for page in document:
            text_parts.append(page.get_text())

    return "\n".join(text_parts).strip()


def extract_text_from_docx(file_bytes: bytes) -> str:
    file_stream = BytesIO(file_bytes)
    document = Document(file_stream)

    text_parts = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if text:
            text_parts.append(text)

    return "\n".join(text_parts).strip()


def extract_text_from_file(
    file_bytes: bytes,
    filename: Optional[str] = None,
    content_type: Optional[str] = None,
) -> str:
    safe_filename = str(filename or "").lower()
    safe_content_type = str(content_type or "").lower()

    is_pdf = (
        safe_filename.endswith(".pdf")
        or safe_content_type == "application/pdf"
        or file_bytes[:4] == b"%PDF"
    )

    is_docx = (
        safe_filename.endswith(".docx")
        or safe_content_type
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

    if is_pdf:
        return extract_text_from_pdf(file_bytes)

    if is_docx:
        return extract_text_from_docx(file_bytes)

    raise ValueError("Unsupported file type. Please upload a PDF or DOCX file.")