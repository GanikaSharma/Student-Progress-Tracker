import pandas as pd
import random

def generate_dataset(n=100):
    data = []
    feedback_samples = [
        "Needs more practice in math",
        "Good understanding but slow in problem solving",
        "Excellent engagement",
        "Struggles with assignments",
        "Strong in theory but weak in application",
        "Very consistent performance"
    ]
    for i in range(1, n+1):
        attendance = random.randint(70, 100)
        assignments = random.randint(5, 10)
        midterm = random.randint(50, 95)
        final = midterm + random.randint(-10, 10)
        feedback = random.choice(feedback_samples)
        data.append([i, attendance, assignments, midterm, final, feedback])

    df = pd.DataFrame(data, columns=[
        "student_id", "attendance", "assignments_completed",
        "midterm_score", "final_score", "feedback"
    ])
    df.to_csv("data/raw/student_data.csv", index=False)
    print("✅ student_data.csv generated!")

if __name__ == "__main__":
    generate_dataset()
