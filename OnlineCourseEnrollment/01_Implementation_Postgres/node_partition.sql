-- Drop the existing schema to ensure a clean setup
DROP SCHEMA IF EXISTS online_learning_schema CASCADE;

-- Create the schema for the online learning platform
CREATE SCHEMA IF NOT EXISTS online_learning_schema;

-- Switch to the schema
SET search_path TO online_learning_schema;

-- Create instructors table
CREATE TABLE instructors (
    instructorid SERIAL PRIMARY KEY,
    name VARCHAR(255),
    bio TEXT
);

-- Create categories table
CREATE TABLE categories (
    categoryid SERIAL PRIMARY KEY,
    categoryname VARCHAR(255)
);

-- Create courses table
CREATE TABLE courses (
    courseid SERIAL PRIMARY KEY,
    coursename VARCHAR(255),
    instructorid INT,
    description TEXT,
    categoryid INT,
    FOREIGN KEY (instructorid) REFERENCES instructors(instructorid),
    FOREIGN KEY (categoryid) REFERENCES categories(categoryid)
);

-- Create students table
CREATE TABLE students (
    studentid SERIAL PRIMARY KEY,
    firstname VARCHAR(100),
    lastname VARCHAR(100),
    email VARCHAR(100) UNIQUE
);

-- Create the parent partitioned table for enrollments (partitioned by hash on studentid)
-- Create the parent partitioned table for enrollments (partitioned by hash on studentid)
CREATE TABLE enrollments (
    enrollmentid SERIAL,
    studentid INT,
    courseid INT,
    enrollmentdate DATE,
    PRIMARY KEY (enrollmentid, studentid),  -- Include studentid in the primary key
    FOREIGN KEY (studentid) REFERENCES students(studentid),
    FOREIGN KEY (courseid) REFERENCES courses(courseid)
) PARTITION BY HASH (studentid);


-- Create partition for (studentid % 3 == 0)
CREATE TABLE enrollments_part1
    PARTITION OF enrollments FOR VALUES WITH (modulus 3, remainder 0);

-- Create partition for (studentid % 3 == 1)
CREATE TABLE enrollments_part2
    PARTITION OF enrollments FOR VALUES WITH (modulus 3, remainder 1);

-- Create partition for (studentid % 3 == 2)
CREATE TABLE enrollments_part3
    PARTITION OF enrollments FOR VALUES WITH (modulus 3, remainder 2);

-- Create index on enrollments_part1 for studentid
CREATE INDEX enrollments_part1_idx ON enrollments_part1 (studentid);

-- Create index on enrollments_part2 for studentid
CREATE INDEX enrollments_part2_idx ON enrollments_part2 (studentid);

-- Create index on enrollments_part3 for studentid
CREATE INDEX enrollments_part3_idx ON enrollments_part3 (studentid);
