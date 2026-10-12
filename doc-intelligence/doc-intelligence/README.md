# Document Intelligence Pipeline

Takes a pile of unstructured PDFs and turns them into something searchable:
each document gets a category, a set of keywords and a few structured fields
(dates, amounts, emails, IDs).

Built in plain Python + scikit-learn. No external APIs, runs offline.

## Stages

    PDF -> extract -> preprocess -> classify -> keywords -> fields -> CSV / JSON

| stage | file | what it does |
|-------|------|--------------|
| extract | `docintel/extract.py` | text from PDF pages (pypdf), bad pages skipped |
| preprocess | `docintel/preprocess.py` | de-hyphenate, normalise whitespace, tokenize, drop stopwords |
| classify | `docintel/classify.py` | TF-IDF (1-2 grams) + LinearSVC |
| keywords | `docintel/keywords.py` | top TF-IDF terms/phrases for the document |
| fields | `docintel/fields.py` | regex for dates, amounts, emails, phones, reference IDs |

`docintel/pipeline.py` strings these together. Every stage reads and writes the
same dict, so adding or removing a stage doesn't break the rest.

## Setup

    python -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt

## Try it with generated data

Real documents are confidential, so there's a script that makes a synthetic
corpus (invoices, contracts, resumes, reports):

    python scripts/make_sample_data.py --n 30
    python main.py train --data data/raw
    python main.py run --input data/raw/invoice --out outputs/results.csv

To use your own PDFs, put them in `data/raw/<category>/` and train again.

## Output

`outputs/results.csv` (one row per file) and `outputs/results.json` (full detail).
`margin` is the SVM score gap between the best and second-best class. Small
margin means the model wasn't sure, so those are worth checking by hand.

## Tests

    pytest

## Limitations

- The synthetic data is very clean, so the accuracy on it says little about
  messy real-world files. Expect to retrain on real documents.
- Scanned PDFs (images) have no text layer; they would need an OCR step first.
- The regex patterns lean towards Indian formats (Rs., +91 phone numbers).
- Keywords are statistical, not semantic - no entity linking or summarisation.

## Ideas for later

- OCR stage for scanned PDFs
- table extraction for invoices
- probability calibration for the classifier
