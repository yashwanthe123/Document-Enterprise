"""Stage 1 - pull raw text out of a PDF."""
from pathlib import Path
from pypdf import PdfReader


def read_pdf(path):
    """Return (text, n_pages). Pages that fail to parse are skipped."""
    reader = PdfReader(str(path))
    pages = []
    for i, page in enumerate(reader.pages):
        try:
            pages.append(page.extract_text() or "")
        except Exception as e:
            print(f"  [skip] {Path(path).name} page {i + 1}: {e}")
    return "\n".join(pages), len(reader.pages)
