import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

def clean_data(df: pd.DataFrame):
    df = df.copy()
    df = df.dropna()
    return df

def encode_features(df: pd.DataFrame):
    df = df.copy()
    label_encoders = {}

    for col in df.select_dtypes(include=["object"]).columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le

    return df, label_encoders

def scale_features(df: pd.DataFrame):
    df = df.copy()
    scaler = StandardScaler()

    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    return df, scaler
