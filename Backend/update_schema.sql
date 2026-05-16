-- SQL script to update course_table column lengths
-- Execute this on your PostgreSQL database inside the EC2 instance

ALTER TABLE course_table ALTER COLUMN course_description TYPE VARCHAR(2000);
ALTER TABLE course_table ALTER COLUMN skill_set TYPE VARCHAR(1000);
ALTER TABLE course_table ALTER COLUMN required_knowledge TYPE VARCHAR(1000);
ALTER TABLE course_table ALTER COLUMN benefits TYPE VARCHAR(1000);
