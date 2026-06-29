-- Highest-paid employee
SELECT *
FROM employees_employee
ORDER BY salary DESC
LIMIT 1;

-- Lowest-paid employee
SELECT *
FROM employees_employee
ORDER BY salary ASC
LIMIT 1;

-- Average salary by department
SELECT
    department_id,
    AVG(salary)
FROM employees_employee
GROUP BY department_id;

-- Employees joined this year
SELECT *
FROM employees_employee
WHERE EXTRACT(YEAR FROM joining_date)
      = EXTRACT(YEAR FROM CURRENT_DATE);

-- Top 10 highest salaries
SELECT *
FROM employees_employee
ORDER BY salary DESC
LIMIT 10;

-- Total employees per department
SELECT
    department_id,
    COUNT(*)
FROM employees_employee
GROUP BY department_id;

-- Departments with more than 20 employees
SELECT
    department_id,
    COUNT(*)
FROM employees_employee
GROUP BY department_id
HAVING COUNT(*) > 20;

-- Employees earning above department average
SELECT *
FROM employees_employee e
WHERE salary >
(
    SELECT AVG(salary)
    FROM employees_employee
    WHERE department_id = e.department_id
);