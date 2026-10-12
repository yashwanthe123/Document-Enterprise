"""Stage 2 - clean the raw text and tokenize it."""
import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# words that show up everywhere in business documents and tell us nothing
EXTRA_STOP = {"page", "pdf", "document", "date", "ref", "no", "per", "shall", "will"}
STOP = set(ENGLISH_STOP_WORDS) | EXTRA_STOP


def clean(text):
    text = text.replace("\r", "\n")
    text = re.sub(r"-\n(?=[a-z])", "", text)          # re-join words split across lines
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def tokenize(text):
    words = re.findall(r"[a-zA-Z][a-zA-Z\-']+", text.lower())
    return [w for w in words if len(w) > 2 and w not in STOP]


def normalized(text):
    """Cleaned text re-joined as tokens - this is what the classifier sees."""
    return " ".join(tokenize(clean(text)))
