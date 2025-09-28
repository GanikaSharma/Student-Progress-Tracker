import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer

class Preprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.vectorizer = TfidfVectorizer(max_features=50)

    def fit_transform(self, df):
        X_num = df[["attendance", "assignments_completed", "midterm_score"]]
        X_num_scaled = self.scaler.fit_transform(X_num)

        X_text = self.vectorizer.fit_transform(df["feedback"]).toarray()

        X = np.hstack([X_num_scaled, X_text])
        y = df["final_score"]

        return X, y

    def transform(self, df):
        X_num = df[["attendance", "assignments_completed", "midterm_score"]]
        X_num_scaled = self.scaler.transform(X_num)

        X_text = self.vectorizer.transform(df["feedback"]).toarray()

        X = np.hstack([X_num_scaled, X_text])
        y = df["final_score"]

        return X, y
