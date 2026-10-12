"""Chains the stages together. Each stage takes and returns the same dict,
so stages can be added/removed without touching the others."""
from pathlib import Path

from . import extract, preprocess, classify, keywords, fields


class DocPipeline:
    def __init__(self, model_path=None):
        self.model = classify.load(model_path) if model_path else None
        self.stages = [
            self._extract,
            self._preprocess,
            self._classify,
            self._keywords,
            self._fields,
        ]

    def _extract(self, doc):
        doc["raw"], doc["pages"] = extract.read_pdf(doc["path"])
        return doc

    def _preprocess(self, doc):
        doc["norm"] = preprocess.normalized(doc["raw"])
        return doc

    def _classify(self, doc):
        if self.model is None:
            doc["category"], doc["margin"] = None, None
        else:
            doc["category"], doc["margin"] = classify.predict(self.model, doc["norm"])
        return doc

    def _keywords(self, doc):
        if self.model is not None:
            doc["keywords"] = keywords.tfidf_keywords(self.model.named_steps["tfidf"], doc["norm"])
        else:
            doc["keywords"] = keywords.count_keywords(doc["raw"])
        return doc

    def _fields(self, doc):
        doc["fields"] = fields.find_fields(doc["raw"])
        return doc

    def run(self, path):
        doc = {"path": str(path), "name": Path(path).name}
        for stage in self.stages:
            doc = stage(doc)
        return doc

    def run_many(self, paths):
        results = []
        for p in paths:
            try:
                results.append(self.run(p))
            except Exception as e:
                print(f"[error] {p}: {e}")
        return results
