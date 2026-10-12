import subprocess
import sys
from pathlib import Path

from docintel import preprocess, fields

ROOT = Path(__file__).parent.parent


def test_clean_joins_hyphenated_words():
    assert "classification" in preprocess.clean("classi-\nfication")


def test_tokenize_drops_stopwords():
    toks = preprocess.tokenize("The invoice is due on the first of the month")
    assert "the" not in toks and "invoice" in toks


def test_fields_amounts_and_dates():
    f = fields.find_fields("Total Rs. 1,200.50 due 12 Mar 2024, mail a@b.com")
    assert f["amounts"] == ["Rs. 1,200.50"]
    assert f["dates"] == ["12 Mar 2024"]
    assert f["emails"] == ["a@b.com"]


def test_end_to_end(tmp_path):
    py = sys.executable
    data = tmp_path / "raw"
    subprocess.run([py, "scripts/make_sample_data.py", "--n", "8", "--out", str(data)], cwd=ROOT, check=True)
    subprocess.run([py, "main.py", "train", "--data", str(data)], cwd=ROOT, check=True)
    out = tmp_path / "res.csv"
    subprocess.run([py, "main.py", "run", "--input", str(data / "invoice"), "--out", str(out)], cwd=ROOT, check=True)
    assert "invoice" in out.read_text()
