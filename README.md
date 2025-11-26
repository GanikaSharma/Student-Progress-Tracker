 # Student Progress Prediction & Recommendation System

🎓 Student Performance Tracker
📌 Project Overview

The Student Performance Tracker is a data-driven system designed to analyze and predict students’ academic performance based on multiple factors such as study hours, attendance, feedback, and test scores.
It helps educators identify at-risk students and improve academic outcomes.

🧠 Features
✅ Data preprocessing and cleaning
✅ Exploratory Data Analysis (EDA) with visual insights
✅ Multiple regression models for performance prediction
✅ Model evaluation and selection
✅ Interactive performance dashboard

⚙️ Tech Stack
• Language: Python
• Libraries: pandas, numpy, matplotlib, seaborn, scikit-learn, xgboost, joblib
• Visualization: Matplotlib, Seaborn
• Environment: Jupyter Notebook

🗂️ Project Structure
Student_Performance_Tracker/
│
├── data/                     # Raw and processed datasets
├── models/                   # Trained models (.pkl files)
├── notebooks/                # Jupyter notebooks
│   ├── 01_data_preprocessing.ipynb
│   ├── 02_data_visualization.ipynb
│   ├── 03_modeling.ipynb
│   ├── 04_modeling_improved.ipynb
│   ├── 05_model_evaluation.ipynb
│   └── 06_dashboard.ipynb
│
├── README.md                 # Project documentation
└── requirements.txt          # Dependencies

🔍 How It Works
1. Load and preprocess data → Handle missing values, encode labels.
2. Explore → Visualize trends between study hours, marks, attendance.
3. Model → Train multiple regression algorithms (Linear, Ridge, XGBoost).
4. Evaluate → Compare models using R², MAE, RMSE.
5. Dashboard → Present key insights and student score predictions visually.

📊 Sample Insights
• Students with consistent study hours and attendance perform 25% better.
• Feedback sentiment strongly correlates with marks.
• The final XGBoost model achieved the highest R² score.

🚀 How to Run Locally
git clone https://github.com/<your-username>/Student_Performance_Tracker.git
cd Student_Performance_Tracker
pip install -r requirements.txt
jupyter notebook

🔮 How to Run a Prediction (CLI)
You can use the trained model to predict a student’s performance category directly from the command line.
➡️ Step 1: Navigate to the project folder
cd Student-Progress-Tracker
➡️ Step 2: Run the prediction script
Use:
python scripts/predict.py <student_id> <attendance> <assignments_completed> <midterm_score> "<feedback>"
Example:
python scripts/predict.py 101 75 8 81 "Very consistent performance"
✔ Expected Output
✅ Predicted Final Score: High

🧩 Future Improvements
• Add live dashboard using Streamlit / Dash
• Integrate database (MySQL / Firebase)
• Deploy predictive model as a REST API

👩‍💻 Author

Ganika Sharma
B.Tech CSE | NIT | Tech Enthusiast | Data-Driven Developer
🌐 LinkedIn

⭐ Contribute
Pull requests are welcome!
If you find issues, feel free to open an issue or suggest an enhancement.