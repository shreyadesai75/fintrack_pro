import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib


DATA_CSV = "ml/data.csv"
MODEL_FILE = "ml/model.pkl"
VECTORIZER_FILE = "ml/vectorizer.pkl"

def train_and_save():
    df = pd.read_csv(DATA_CSV)
    df['description'] = df['description'].fillna("").str.lower()

    X = df['description']
    y = df['category']

    vectorizer = TfidfVectorizer(stop_words='english')
    X_vec = vectorizer.fit_transform(X)

    model = MultinomialNB()
    model.fit(X_vec, y)

    joblib.dump(model, MODEL_FILE)
    joblib.dump(vectorizer, VECTORIZER_FILE)

    print(f"Model and vectorizer saved: {MODEL_FILE}, {VECTORIZER_FILE}")

if __name__ == "__main__":
    train_and_save()
