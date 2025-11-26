import joblib
import pandas as pd
import sys

# 1️⃣ Load the model once
try:
    model = joblib.load("models/random_forest.pkl")
except FileNotFoundError:
    print("Model file not found. Make sure 'models/random_forest.pkl' exists.")
    sys.exit(1)

# 2️⃣ Define prediction function
def predict(input_data):
    # Ensure input matches the feature columns expected by the model
    df = pd.DataFrame([input_data])
    # Optional: reorder columns if needed (use model.feature_names_in_ if available)
    if hasattr(model, "feature_names_in_"):
        df = df[model.feature_names_in_]
    pred = model.predict(df)[0]
    return pred

# 3️⃣ Main function to accept command line arguments
if __name__ == "__main__":
    # python predict.py 75 80 90 10
    if len(sys.argv) != 5:
        print("Usage: python predict.py attendance test1 test2 assignments_submitted")
        sys.exit(1)

    try:
        data = {
            "attendance": float(sys.argv[1]),
            "test1": float(sys.argv[2]),
            "test2": float(sys.argv[3]),
            "assignments_submitted": int(sys.argv[4])
        }
    except ValueError:
        print("All input values must be numeric.")
        sys.exit(1)

    result = predict(data)
    print(f"Predicted Performance Category: {result}")
