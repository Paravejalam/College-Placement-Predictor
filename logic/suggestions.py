def generate_suggestions(inputs: dict):
    """
    Generate role-based improvement suggestions dynamically
    based on selected domain and skill levels
    """

    suggestions = []

    # -------------------------
    # COMMON SUGGESTIONS
    # -------------------------
    if inputs.get("internships", 0) < 1:
        suggestions.append("Do at least 1 internship (AICTE / Internshala / Forage)")

    if inputs.get("projects", 0) < 2:
        suggestions.append("Build 2–3 real-world projects and deploy them")

    if inputs.get("certifications", 0) < 1:
        suggestions.append("Add certifications from Coursera, Udemy, Google, IBM")

    if inputs.get("skills", 0) < 7:
        suggestions.append("Improve overall technical skills and problem-solving")

    # -------------------------
    # DOMAIN-SPECIFIC SUGGESTIONS
    # -------------------------
    domain = inputs.get("domain", "")

    # 🧠 DATA SCIENCE / ML
    if domain == "Data Science":
        suggestions.extend([
            "Build ML projects (Prediction, Recommendation, NLP, Time Series)",
            "Improve Python, NumPy, Pandas, Scikit-learn",
            "Learn Machine Learning & Model Evaluation",
            "Add SHAP, Feature Engineering, EDA to projects",
            "Use Jupyter Notebook & GitHub for documentation"
        ])

    # 🌐 WEB DEVELOPMENT
    elif domain == "Web Development":
        suggestions.extend([
            "Create Full Stack projects (Job Portal, E-commerce, Dashboard)",
            "Improve HTML, CSS, JavaScript, React",
            "Learn Backend (Node.js / Express)",
            "Practice REST API & Authentication (JWT)",
            "Host projects and push clean code to GitHub"
        ])

    # 🛢 DATA ENGINEERING
    elif domain == "Data Engineering":
        suggestions.extend([
            "Build ETL and data pipeline projects",
            "Improve SQL & Advanced SQL queries",
            "Learn Apache Spark, Hadoop, Airflow",
            "Practice cloud tools (AWS / GCP / Azure)",
            "Work on real-time or batch data processing"
        ])

    # 📊 DATA ANALYTICS
    elif domain == "Data Analytics":
        suggestions.extend([
            "Build dashboards using Power BI / Tableau",
            "Improve SQL and Excel (Advanced)",
            "Work on business & KPI analysis projects",
            "Use Python for data cleaning & visualization",
            "Focus on storytelling with data"
        ])

    # ⚙️ SOFTWARE / IT / OTHER
    else:
        suggestions.extend([
            "Improve DSA using LeetCode / HackerRank",
            "Strengthen OOPs, DBMS, OS, CN fundamentals",
            "Build core programming projects",
            "Maintain GitHub with clean README files"
        ])

    # -------------------------
    # COMMUNICATION & APTITUDE
    # -------------------------
    if inputs.get("communication_score", 0) < 7:
        suggestions.append("Improve communication & interview skills")

    if inputs.get("aptitude_score", 0) < 7:
        suggestions.append("Practice aptitude & logical reasoning")

    return suggestions
