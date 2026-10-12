"""Stage 4 - keyword / key-phrase extraction.

If a trained model is available we reuse its TF-IDF vectorizer (so rare but
discriminative terms rank higher). Otherwise fall back to plain term counts.
"""
from collections import Counter
import numpy as np
from .preprocess import tokenize


def tfidf_keywords(vectorizer, norm_text, k=8):
    row = vectorizer.transform([norm_text])
    if row.nnz == 0:
        return []
    names = np.array(vectorizer.get_feature_names_out())
    idx = row.toarray()[0].argsort()[::-1][:k]
    return [names[i] for i in idx if row[0, i] > 0]


def count_keywords(text, k=8):
    return [w for w, _ in Counter(tokenize(text)).most_common(k)]
