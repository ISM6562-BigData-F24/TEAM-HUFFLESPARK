-- Drop the existing schema to ensure a clean setup
DROP SCHEMA IF EXISTS online_learning_schema CASCADE;

-- Create the schema for the online learning platform
CREATE SCHEMA IF NOT EXISTS online_learning_schema;

-- Switch to the schema
SET search_path TO online_learning_schema;

-- Recreate the enrollments_node3 table without a primary key constraint
CREATE TABLE enrollments_node3 (
    enrollmentid SERIAL,
    studentid INT,
    courseid INT,
    enrollmentdate DATE
);

