import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("analytics/placement.db")

# Query 1: Placement rate by domain
q1 = """
SELECT domain, AVG(placement_probability) AS avg_probability
FROM students
JOIN predictions USING(student_id)
GROUP BY domain;
"""
df_domain = pd.read_sql(q1, conn)

# Query 2: High risk students
q2 = """
SELECT student_id, cgpa, placement_probability
FROM students
JOIN predictions USING(student_id)
WHERE placement_probability < 30;
"""
df_risk = pd.read_sql(q2, conn)

conn.close()

print(df_domain.head())
print(df_risk.head())

with pd.ExcelWriter("excel_reports/placement_summary.xlsx", engine="xlsxwriter") as writer:
    df_domain.to_excel(writer, sheet_name="Domain_Analysis", index=False)
    df_risk.to_excel(writer, sheet_name="High_Risk_Students", index=False)
