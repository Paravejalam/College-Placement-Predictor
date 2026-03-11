---
title: College Placement Predictor
emoji: 🎓
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

## 🚀 Live Application
👉 https://college-placement-predictor-5ijenf8fsnyq67zuubgpra.streamlit.app/

# 🎓 College Placement Predictor & Resume Insights Dashboard

An end-to-end **Machine Learning + Data Analytics project** that predicts college placement probability, analyzes resume strength, and provides actionable insights using **Streamlit**, **ML**, **SHAP explainability**, and ****Power BI Dashboards (Exploratory / Planned)**
This project also demonstrates strong **Data Analytics skills using SQL and Excel**, including placement trend analysis and reporting.
---

## 🧠 Tech Stack

### Programming & Data
- Python, Pandas, NumPy
- SQL (SQLite)

### Data Analytics & Reporting
- Excel (Analytical Reports & Charts)
- Power BI (Interactive Dashboards)

### Machine Learning
- Scikit-learn
- Logistic Regression
- Feature Engineering & Probability Prediction

### Explainable AI & NLP
- SHAP (Model Explainability)
- Resume Parsing (NLP)
- ATS Resume Matching

### Web Application
- Streamlit
- Custom CSS (Dark UI)
- What-If Simulator

### Database & Pipeline
- SQLite
- Python Data Pipelines

### Deployment
- Git & GitHub
- Streamlit Cloud



## 🚀 Project Highlights

- 📊 **Placement Probability Prediction** (ML-based)
- 📄 **Resume Upload + Auto-Fill (NLP-based parsing)**
- 🧠 **Explainable AI (SHAP Waterfall Plot)**
- 🔁 **What-If Simulator** (real-time improvement analysis)
- 📈 **ATS Resume Matching Score**
- 📝 **Personalized Skill Improvement Suggestions**
- 📑 **Downloadable PDF Resume Report**
- 📊 **Power BI Interactive Dashboards**
- 🌐 **Production-ready Streamlit Web App**

---

## 📊 Data Analytics (SQL + Excel)

- Performed SQL analysis on student placement data using JOINs, GROUP BY, and aggregations  
- Calculated domain-wise placement percentages  
- Exported SQL results into Excel for reporting  
- Created Excel column charts to visualize placement trends  

📁 **Excel Report:**  
- `excel_reports/placement_summary.xlsx`

---

## 🔢 Model Input Features

- CGPA  
- Number of Internships  
- Number of Projects  
- Certifications  
- Aptitude Score  
- Technical Score  
- Communication Score  
- Overall Skills  
- Preferred Domain  

---

## 🛠️ Tech Stack

**Programming & ML**
- Python
- NumPy, Pandas
- Scikit-learn (Logistic Regression)
- SHAP (Explainability)

**Web App**
- Streamlit
- HTML/CSS (Dark + Mobile responsive UI)

**NLP**
- Resume PDF Parsing
- Feature extraction from resume text

**Visualization**
- Power BI
- Plotly / Matplotlib

---

## 🧩 Project Structure

college-placement-predictor/
│
├── app.py
├── requirements.txt
├── README.md
│
├── components/
│ ├── header.py
│ └── pdf_report.py
│
├── forms/
│ └── form_inputs.py
│
├── logic/
│ ├── prediction.py
│ ├── ats.py
│ ├── suggestions.py
│ └── what_if.py
│
├── ml/
│ ├── model.py
│ └── preprocess.py
│
├── model/
│ └── model.pkl
│
├── reports/
│ └── report.py
│
├── styles/
│ ├── base.css
│ ├── dark.css
│ └── mobile.css
│
└── utils/
├── resume_parser.py
└── constants.py


---

## ▶️ How to Run Locally

### 1️⃣ Clone Repository
```bash
git clone https://github.com/your-username/college-placement-predictor.git

2️⃣ Move into Project Folder
cd college-placement-predictor

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run Streamlit App
streamlit run app.py


📊 Power BI Dashboards

This project also includes Power BI dashboards for deep data analysis:

📈 Placement Rate by Domain

📉 Skills vs CGPA Distribution

🧠 Resume Strength Analysis

📊 Internship & Project Impact

🎯 Actual vs Predicted Placement Comparison

(Dashboards created using real project dataset for analytical insights)

🧠 ML Explainability

SHAP Waterfall Plot shows feature-wise impact

Helps understand why a candidate is likely/unlikely to be placed

Improves trust and transparency of predictions

🔮 Future Enhancements

🔬 Deep Learning model (XGBoost / Neural Network)

🧾 Resume keyword optimization suggestions

🔁 Multi-resume comparison

☁️ Cloud deployment (Streamlit Cloud / Render)

👔 Recruiter dashboard view

🙌 Author

Paravej Alam
🎓 Data Analyst | Machine Learning Enthusiast
📊 Python | Power BI | Machine Learning | Streamlit
