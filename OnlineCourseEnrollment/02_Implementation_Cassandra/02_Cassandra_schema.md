# Query-First Approach

## Key Application Queries:
1. **Retrieve all courses a student has enrolled in.**
2. **Retrieve all students enrolled in a specific course.**
3. **Retrieve instructor details for a specific course.**
4. **Retrieve courses by category.**
5. **Retrieve the number of enrollments in a course during a specific time period.**

These queries form the foundation of how data will be accessed in the application and drive the schema design for efficient querying in Cassandra.

---
## Create keyspace with SimpleStrategy and replication factor 1
```CQL
CREATE KEYSPACE IF NOT EXISTS online_learning
WITH REPLICATION = {
  'class': 'SimpleStrategy',
  'replication_factor': 1
};
```

## Use the created keyspace
```CQL
USE online_learning;
```

---

## Table 1: courses_by_student
```CQL
CREATE TABLE courses_by_student (
    studentid INT,
    courseid INT,
    enrollment_date DATE,
    coursename TEXT,
    instructorid INT,
    PRIMARY KEY (studentid, courseid)
);
```

- **Purpose**: This table supports the query that retrieves all courses a student is enrolled in.
- **Explanation**:
  - **Partition Key** (studentid): This ensures that all enrollments for a specific student are stored together and can be retrieved quickly.
  - **Clustering Column** (courseid): Ensures that each enrollment is uniquely identifiable and allows for efficient querying by course within the same partition.
  - **Why this structure?**: The query access pattern in the application needs to retrieve all courses for a student, making studentid the ideal partition key.

---

## Table 2: students_by_course
```CQL
CREATE TABLE students_by_course (
    courseid INT,
    studentid INT,
    enrollment_date DATE,
    firstname TEXT,
    lastname TEXT,
    email TEXT,
    PRIMARY KEY (courseid, studentid)
);
```
- **Purpose**: Supports the query that retrieves all students enrolled in a specific course.
- **Explanation**:
  - **Partition Key** (courseid): All student enrollments for a course are stored in the same partition, enabling fast retrieval of all students in a given course.
  - **Clustering Column** (studentid): Ensures uniqueness within the course and provides fast querying of specific students in a course.
  - **Why this structure?**: Since the query is about retrieving all students for a course, courseid serves as the best partition key to group all relevant student enrollments together.

---

## Table 3: instructors_by_course
```CQL
CREATE TABLE instructors_by_course (
    courseid INT,
    instructorid INT,
    name TEXT,
    bio TEXT,
    PRIMARY KEY (courseid, instructorid)
);
```
- **Purpose**: Facilitates retrieving instructor details for a specific course.
- **Explanation**:
  - **Partition Key** (courseid): Since this query focuses on a single course, courseid is the natural partition key.
  - **Clustering Column** (instructorid): Though there’s usually one instructor per course, using instructorid as a clustering column ensures uniqueness and possible future expansion if courses are co-taught.
  - **Why this structure?**: Queries involving the retrieval of instructor details are typically scoped by course, making courseid the appropriate partition key.

---

## Table 4: courses_by_category
```CQL
CREATE TABLE courses_by_category (
    categoryid INT,
    courseid INT,
    coursename TEXT,
    description TEXT,
    instructorid INT,
    PRIMARY KEY (categoryid, courseid)
);
```
- **Purpose**: Supports queries that retrieve courses based on category.
- **Explanation**:
  - **Partition Key** (categoryid): Organizes courses by category for fast querying of all courses within a particular category.
  - **Clustering Column** (courseid): Allows efficient organization and retrieval of individual courses within each category.
  - **Why this structure?**: The query pattern is focused on retrieving courses by their associated category, making categoryid the logical partition key.

---

## Table 5: enrollments_by_course
```CQL
CREATE TABLE enrollments_by_course (
    courseid INT,
    enrollment_date DATE,
    studentid INT,
    PRIMARY KEY (courseid, enrollment_date, studentid)
);
```
- **Purpose**: Supports the query that retrieves the number of enrollments in a course during a specific time period.
- **Explanation**:
  - **Partition Key** (courseid): Groups all enrollment data for a course together for fast access.
  - **Clustering Column** (enrollment_date, studentid): Organizes enrollments by date and ensures uniqueness for each student in a course on a given date. This also allows for efficient querying based on date ranges.
  - **Why this structure?**: Since the query pattern focuses on enrollments in a course over time, courseid is the partition key, and enrollment_date is used as a clustering column to support date-based filtering.

---

## Data Insertion
We have used the commands in the insert_data_