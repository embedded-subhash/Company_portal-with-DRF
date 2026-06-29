# Query Optimization Report

## Indexed Query

Query:

SELECT *
FROM employees_employee
WHERE employee_id = 'EMP001';

Execution Plan:

Index Scan using idx_employee_id

Benefits:

- Faster lookup
- Reduced execution time
- Avoids full table scan

---

## Non-Indexed Query

Query:

SELECT *
FROM employees_employee
WHERE first_name = 'John';

Execution Plan:

Sequential Scan

Drawbacks:

- Reads entire table
- Slower on large datasets

---

## ORM Optimizations

Applied:

- select_related('department')
- annotate()
- aggregate()

Benefits:

- Eliminates N+1 queries
- Reduces database hits
- Improves response time

---

## Database Improvements

Implemented:

- CHECK constraints
- UNIQUE constraints
- Single-column indexes
- Composite indexes
- Raw SQL reports
- Transaction management
- Backup and restore procedures