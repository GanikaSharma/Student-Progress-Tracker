import joblib
import pandas as pd
import sys
import os

# -----------------------------
# 1️⃣ Load Model + Encoders
# -----------------------------
MODEL_PATH = "models/random_forest.pkl"
ENCODER_PATH = "models/label_encoders.pkl"

if not os.path.exists(MODEL_PATH):
    print("❌ Model file missing! Expected at: models/random_forest.pkl")
    sys.exit(1)

model = joblib.load(MODEL_PATH)

# Load encoders only if they exist
label_encoders = joblib.load(ENCODER_PATH) if os.path.exists(ENCODER_PATH) else None


# -----------------------------
# 2️⃣ Prediction Function
# -----------------------------
def predict(input_data):
    df = pd.DataFrame([input_data])

    # Apply label encoder to feedback if available
    if label_encoders and "feedback" in label_encoders:
        df["feedback"] = label_encoders["feedback"].transform(df["feedback"])

    # Ensure columns match model
    if hasattr(model, "feature_names_in_"):
        missing_cols = set(model.feature_names_in_) - set(df.columns)
        if missing_cols:
            raise ValueError(f"Missing required columns for prediction: {missing_cols}")

        df = df[model.feature_names_in_]

    # Run prediction
    prediction = model.predict(df)[0]
    return prediction


# -----------------------------
# 3️⃣ Command Line Interface
# -----------------------------
if __name__ == "__main__":
    # Usage:
    # python scripts/predict.py attendance assignments_completed midterm_score feedback

    if len(sys.argv) != 5:
        print("Usage: python scripts/predict.py <attendance> <assignments_completed> <midterm_score> <feedback>")
        sys.exit(1)

    try:
        data = {
            "student_id": 9999,  # dummy ID, not used for prediction but required by model
            "attendance": float(sys.argv[1]),
            "assignments_completed": int(sys.argv[2]),
            "midterm_score": float(sys.argv[3]),
            "feedback": sys.argv[4]
        }
    except ValueError:
        print("❌ Error: Numeric fields must contain valid numbers.")
        sys.exit(1)

    result = predict(data)
    print(f"\n✅ Predicted Final Score: {result}\n")
