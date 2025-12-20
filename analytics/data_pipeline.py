import sqlite3
import pandas as pd

conn = sqlite3.connect("analytics/placement.db")

df = pd.read_csv("data/cleaned_placement_data.csv")

# 2. Connect to SQLite
conn = sqlite3.connect("analytics/placement.db")

# 3. Insert into students table
students_df = df[[
    "student_id",
    "cgpa",
    "internships",
    "projects",
    "domain"
]]

students_df.to_sql("students", conn, if_exists="append", index=False)

# 4. Insert predictions
pred_df = df[
    ["student_id", "placed"]
]

pred_df.to_sql("predictions", conn, if_exists="replace", index=False)

conn.close()
print("✅ Data inserted successfully into database")
