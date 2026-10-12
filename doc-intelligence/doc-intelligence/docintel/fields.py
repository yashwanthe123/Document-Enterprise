"""Stage 5 - pick out structured bits (dates, amounts, contacts) with regex."""
import re

PATTERNS = {
    "emails": r"[\w.+-]+@[\w-]+\.[\w.-]+",
    "phones": r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}(?!\d)",
    "dates": r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s\d{4}\b",
    "amounts": r"(?:Rs\.?|INR|₹|\$)\s?\d[\d,]*(?:\.\d{1,2})?",
    "ids": r"\b(?:INV|PO|REF|CN)[-/]?\d{3,}\b",
}


def find_fields(text):
    out = {}
    for name, pat in PATTERNS.items():
        hits = re.findall(pat, text)
        seen = []
        for h in hits:
            h = h.strip()
            if h not in seen:
                seen.append(h)
        out[name] = seen[:10]
    return out
