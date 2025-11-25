# researchSummarizer/app/services/extractor.py
import io
import pdfplumber
from docx import Document
from typing import Optional


def extract_text_from_pdf_bytes(file_bytes: bytes) -> str:
    """
    Extract text from PDF bytes using pdfplumber.
    Returns plain text (best-effort). May not perfectly handle 2-column PDFs.
    """
    text_parts = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            # extract_text() may return None for empty pages
            t = page.extract_text()
            if t:
                text_parts.append(t)
    return "\n\n".join(text_parts).strip()


def extract_text_from_docx_bytes(file_bytes: bytes) -> str:
    """
    Extract text from a docx file given bytes.
    """
    # python-docx expects a file-like object
    f = io.BytesIO(file_bytes)
    doc = Document(f)
    paragraphs = [p.text for p in doc.paragraphs if p.text and p.text.strip()]
    return "\n\n".join(paragraphs).strip()


def extract_text_from_bytes(filename: str, file_bytes: bytes) -> Optional[str]:
    """
    Dispatch helper: choose extractor based on filename extension.
    Returns extracted text or None if unsupported.
    """
    name = filename.lower()
    if name.endswith(".pdf"):
        return extract_text_from_pdf_bytes(file_bytes)
    if name.endswith(".docx"):
        return extract_text_from_docx_bytes(file_bytes)
    return None
