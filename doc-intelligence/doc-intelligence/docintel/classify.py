"""Stage 3 - document classification (TF-IDF + linear SVM)."""
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC


def build():
    return Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_df=0.9, sublinear_tf=True)),
        ("svm", LinearSVC(C=1.0)),
    ])


def train(texts, labels, test_size=0.2, seed=7):
    X_tr, X_te, y_tr, y_te = train_test_split(
        texts, labels, test_size=test_size, random_state=seed, stratify=labels)

    model = build().fit(X_tr, y_tr)
    print(classification_report(y_te, model.predict(X_te), digits=3))

    # final model uses everything
    return build().fit(texts, labels)


def save(model, path):
    joblib.dump(model, path)


def load(path):
    return joblib.load(path)


def predict(model, norm_text):
    """Returns (label, margin). margin is the SVM decision gap between the
    top two classes - a rough confidence, not a probability."""
    scores = model.decision_function([norm_text])[0]
    order = scores.argsort()[::-1]
    label = model.classes_[order[0]]
    margin = float(scores[order[0]] - scores[order[1]])
    return label, margin
