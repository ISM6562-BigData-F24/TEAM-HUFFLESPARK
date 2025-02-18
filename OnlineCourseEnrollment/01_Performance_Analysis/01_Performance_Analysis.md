# **Performance Benchmark: Partitioning vs Sharding**

## **1. Introduction**
This document compares the performance between **partitioning** (single-node) and **sharding** (multi-node) in PostgreSQL using key operations such as inserts, select queries, range queries, and deletes.

---

## **2. Partitioning Setup**

### **Insert Performance**
```sql
EXPLAIN ANALYZE INSERT INTO online_learning_schema.enrollments (studentid, courseid, enrollmentdate)
VALUES (6, 10, '2024-02-01');
```

- **Execution Time**: 5.186 ms

### **Select Query Performance**

```sql

EXPLAIN ANALYZE SELECT * FROM online_learning_schema.enrollments WHERE studentid = 6;
```

- **Execution Time**: 0.417 ms

### **Range Query Performance**

```sql
EXPLAIN ANALYZE SELECT * FROM online_learning_schema.enrollments WHERE enrollmentdate BETWEEN '2024-01-01' AND '2024-01-31';
```

- **Execution Time**: 0.794 ms

### **Cross-partition Query**
```sql
EXPLAIN ANALYZE SELECT * FROM online_learning_schema.enrollments WHERE studentid IN (1, 2, 3);
```
- **Execution Time**: 0.488 ms

### **Delete Performance**

```sql
EXPLAIN ANALYZE DELETE FROM online_learning_schema.enrollments WHERE studentid = 6;
```
- **Execution Time**: 5.421 ms

## **3. Sharding Setup**

### **Insert Performance**
```sql
EXPLAIN ANALYZE INSERT INTO online_learning_schema.enrollments (studentid, courseid, enrollmentdate)
VALUES (7, 10, '2024-02-02');
```
- **Execution Time**: 56.728 ms

### **Select Query Performance**

```sql
EXPLAIN ANALYZE SELECT * FROM online_learning_schema.enrollments WHERE studentid = 7;
```
- **Execution Time**: 5.509 ms

### **Range Query Performance**

```sql
EXPLAIN ANALYZE SELECT * FROM online_learning_schema.enrollments WHERE enrollmentdate BETWEEN '2024-01-01' AND '2024-01-31';
```
- **Execution Time**: 35.135 ms

### **Cross-node Query**

```sql
EXPLAIN ANALYZE SELECT * FROM online_learning_schema.enrollments WHERE studentid IN (1, 2, 3);
```
- **Execution Time**: 8.012 ms

### **Delete Performance**

```sql
EXPLAIN ANALYZE DELETE FROM online_learning_schema.enrollments WHERE studentid = 7;
```
- **Execution Time**: 8.358 ms

## **4. Performance Comparison**

| Operation                 | Partitioning (ms) | Sharding (ms) |
|---------------------------|-------------------|---------------|
| Insert Performance         | 5.186             | 56.728        |
| Select Query Performance   | 0.417             | 5.509         |
| Range Query Performance    | 0.794             | 35.135        |
| Cross-partition/Node Query | 0.488             | 8.012         |
| Delete Performance         | 5.421             | 8.358         |

## **5. Conclusion**

- **Insert Performance**: Partitioning is significantly faster in inserts due to being contained in a single node.
- **Select Query**: Partitioning shows faster response times for single record selects.
- **Range Query**: Partitioning is faster for range queries since it doesn’t involve cross-node data fetching.
- **Cross-partition/Node Query**: Partitioning is more efficient here due to the overhead of cross-node communication in sharding.
- **Delete Performance**: Sharding shows slower performance due to the foreign scans and multi-node coordination.

## **6. Observations**

- **Partitioning** is more efficient for most operations, given that it avoids the overhead of communication between multiple nodes.
- **Sharding** is better suited for scenarios where horizontal scalability and distribution of load across multiple nodes is necessary.
