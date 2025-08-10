import joblib
import os

MODEL_FILE = "ml/model.pkl"
VECTORIZER_FILE = "ml/vectorizer.pkl"

_model = None
_vectorizer = None

def _load_model():
    global _model, _vectorizer
    if _model is None or _vectorizer is None:
        if not (os.path.exists(MODEL_FILE) and os.path.exists(VECTORIZER_FILE)):
            raise FileNotFoundError("Model or vectorizer not found. Please run model.py first.")
        _model = joblib.load(MODEL_FILE)
        _vectorizer = joblib.load(VECTORIZER_FILE)

def suggest_category(description: str) -> str:
    _load_model()
    desc = description.lower()
    X_vec = _vectorizer.transform([desc])
    prediction = _model.predict(X_vec)
    return prediction[0]

if __name__ == "__main__":
    test_desc = "Uber ride"
    test_amount = 150
    category = suggest_category(test_desc)  # <-- use suggest_category here
    print(f"Predicted category for '{test_desc}' with amount {test_amount} is: {category}")