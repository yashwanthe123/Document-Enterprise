"""CLI for the document intelligence pipeline.

    python main.py train --data data/raw
    python main.py run --input some.pdf
    python main.py run --input data/raw/invoice --out outputs/results.csv
"""
import argparse
import csv
import json
from pathlib import Path

from docintel import preprocess, classify, extract
from docintel.pipeline import DocPipeline

MODEL_PATH = Path("models/doc_classifier.joblib")


def cmd_train(args):
    texts, labels = [], []
    for cat_dir in sorted(p for p in Path(args.data).iterdir() if p.is_dir()):
        pdfs = list(cat_dir.glob("*.pdf"))
        print(f"{cat_dir.name}: {len(pdfs)} docs")
        for pdf in pdfs:
            text, _ = extract.read_pdf(pdf)
            texts.append(preprocess.normalized(text))
            labels.append(cat_dir.name)

    model = classify.train(texts, labels)
    MODEL_PATH.parent.mkdir(exist_ok=True)
    classify.save(model, MODEL_PATH)
    print("model saved to", MODEL_PATH)


def cmd_run(args):
    src = Path(args.input)
    paths = [src] if src.is_file() else sorted(src.rglob("*.pdf"))
    pipe = DocPipeline(MODEL_PATH if MODEL_PATH.exists() else None)
    results = pipe.run_many(paths)

    out = Path(args.out)
    out.parent.mkdir(exist_ok=True)
    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["file", "pages", "category", "margin", "keywords", "amounts", "dates"])
        for r in results:
            w.writerow([r["name"], r["pages"], r["category"],
                        None if r["margin"] is None else round(r["margin"], 2),
                        "; ".join(r["keywords"]), "; ".join(r["fields"]["amounts"]),
                        "; ".join(r["fields"]["dates"])])

    json_path = out.with_suffix(".json")
    slim = [{k: v for k, v in r.items() if k not in ("raw", "norm")} for r in results]
    json_path.write_text(json.dumps(slim, indent=2))

    for r in results[:5]:
        print(f'{r["name"]:<22} {r["category"]}  {r["keywords"][:4]}')
    print(f"... {len(results)} documents -> {out}, {json_path}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    t = sub.add_parser("train")
    t.add_argument("--data", default="data/raw")
    t.set_defaults(fn=cmd_train)

    r = sub.add_parser("run")
    r.add_argument("--input", required=True)
    r.add_argument("--out", default="outputs/results.csv")
    r.set_defaults(fn=cmd_run)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
