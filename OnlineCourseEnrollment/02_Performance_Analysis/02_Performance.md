# Performance Queries

## Question 1:
**Business Question**: *What are the names of all courses that student with ID = 10 is enrolled in?*

- **Postgres Query**: 
```SQL
EXPLAIN ANALYZE
SELECT coursename
FROM online_learning_schema.enrollments e
JOIN online_learning_schema.courses c ON e.courseid = c.courseid
WHERE e.studentid = 10;
```

- **Cassandra Query**: 
```SQL
SELECT coursename
FROM courses_by_student
WHERE studentid = 10;
```
---

## Question 2:
**Business Question**: *What are the first names and last names of students enrolled in the course with ID = 5?*

- **Postgres Query**: 
```SQL
EXPLAIN ANALYZE
SELECT s.firstname, s.lastname
FROM online_learning_schema.enrollments e
JOIN online_learning_schema.students s ON e.studentid = s.studentid
WHERE e.courseid = 5;
```
- **Cassandra Query**: 
```SQL
SELECT firstname, lastname
FROM students_by_course
WHERE courseid = 5;
```
---

## Question 3:
**Business Question**: *Who is the instructor for the course with ID = 3?*

- **Postgres Query**: 
```SQL
EXPLAIN ANALYZE
SELECT i.name, i.bio
FROM online_learning_schema.courses c
JOIN online_learning_schema.instructors i ON c.instructorid = i.instructorid
WHERE c.courseid = 3;
```

- **Cassandra Query**: 
```SQL
SELECT name, bio
FROM instructors_by_course
WHERE courseid = 3;
```
---

## Question 4:
**Business Question**: *List all the courses in the category 'Technology'.*

- **Postgres Query**: 
```SQL
EXPLAIN ANALYZE
SELECT coursename
FROM online_learning_schema.courses c
JOIN online_learning_schema.categories cat ON c.categoryid = cat.categoryid
WHERE cat.categoryname = 'Technology';
```
- **Cassandra Query**: 
```SQL
SELECT coursename
FROM courses_by_category
WHERE categoryid = 1;  -- Assuming 1 is for 'Technology'
```

---

## Question 5:
**Business Question**: *How many students enrolled in course ID 8 during January 2024?*

- **Postgres Query**: 
```SQL
EXPLAIN ANALYZE
SELECT COUNT(*)
FROM online_learning_schema.enrollments
WHERE courseid = 8
AND enrollmentdate BETWEEN '2024-01-01' AND '2024-01-31';
```
- **Cassandra Query**: 
```SQL
SELECT COUNT(*)
FROM enrollments_by_course
WHERE courseid = 8
AND enrollment_date >= '2024-01-01' AND enrollment_date <= '2024-01-31';
```

