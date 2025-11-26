def generate_recommendations(student_row):
    recs = []

    if student_row["attendance"] < 0.5:
        recs.append("Improve attendance for better performance.")

    if student_row["assignments_completed"] < 0.5:
        recs.append("Complete more assignments regularly.")

    if student_row["final_score"] < 0.4:
        recs.append("Spend more time on revision and mock tests.")

    if not recs:
        recs.append("Great job! Maintain your performance.")

    return recs
 
