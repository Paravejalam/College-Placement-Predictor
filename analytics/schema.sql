CREATE TABLE students (
    student_id INTEGER PRIMARY KEY,
    cgpa REAL,
    domain TEXT,
    internships INTEGER,
    projects INTEGER,
    certifications INTEGER
);

CREATE TABLE skills (
    student_id INTEGER,
    aptitude INTEGER,
    technical INTEGER,
    communication INTEGER,
    overall_skills INTEGER
);

CREATE TABLE predictions (
    student_id INTEGER,
    placement_probability REAL,
    prediction_date TEXT
);
