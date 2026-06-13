from io import BytesIO
from docx import Document
import fitz

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
        if paragraph.text.strip():
            text_parts.append(paragraph.text.strip())

    return "\n".join(text_parts).strip()


def extract_text_from_file(filename: str, file_bytes: bytes) -> str:
    lower_filename = filename.lower()

    if lower_filename.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)

    if lower_filename.endswith(".docx"):
        return extract_text_from_docx(file_bytes)

    raise ValueError("Unsupported file type. Please upload a PDF or DOCX file.")