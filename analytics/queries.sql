-- Placement rate by domain
SELECT domain, AVG(placement_probability) AS avg_probability
FROM students
JOIN predictions USING(student_id)
GROUP BY domain;

-- High-risk students
SELECT student_id, cgpa, placement_probability
FROM students
JOIN predictions USING(student_id)
WHERE placement_probability < 30;

-- Skill impact analysis
SELECT AVG(technical) AS avg_tech_skill, AVG(placement_probability)
FROM skills
JOIN predictions USING(student_id);
