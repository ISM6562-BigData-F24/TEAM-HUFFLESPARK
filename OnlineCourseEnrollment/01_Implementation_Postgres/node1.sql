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

-- Create the parent partitioned enrollments table (without primary key)
CREATE TABLE enrollments (
    enrollmentid SERIAL,
    studentid INT,
    courseid INT,
    enrollmentdate DATE
) PARTITION BY HASH (studentid);

-- Create the local partition for enrollments on Node1
CREATE TABLE enrollments_part1
    PARTITION OF enrollments FOR VALUES WITH (modulus 3, remainder 0);

-- Enable postgres_fdw extension
CREATE EXTENSION IF NOT EXISTS postgres_fdw;

-- Create a foreign server connection to Node2
CREATE SERVER node2_server
    FOREIGN DATA WRAPPER postgres_fdw
    OPTIONS (host 'project-node2', dbname 'project_db2', port '5432');

-- Create a foreign server connection to Node3
CREATE SERVER node3_server
    FOREIGN DATA WRAPPER postgres_fdw
    OPTIONS (host 'project-node3', dbname 'project_db3', port '5432');

-- Create user mappings for connecting to Node2 and Node3 (replace with actual credentials)
CREATE USER MAPPING FOR user1
    SERVER node2_server
    OPTIONS (user 'user2', password 'password2');

CREATE USER MAPPING FOR user1
    SERVER node3_server
    OPTIONS (user 'user3', password 'password3');

-- Create foreign table for the enrollments partition on Node2
CREATE FOREIGN TABLE enrollments_part2
    PARTITION OF enrollments FOR VALUES WITH (modulus 3, remainder 1)
    SERVER node2_server
    OPTIONS (schema_name 'online_learning_schema', table_name 'enrollments_node2');

-- Create foreign table for the enrollments partition on Node3
CREATE FOREIGN TABLE enrollments_part3
    PARTITION OF enrollments FOR VALUES WITH (modulus 3, remainder 2)
    SERVER node3_server
    OPTIONS (schema_name 'online_learning_schema', table_name 'enrollments_node3');