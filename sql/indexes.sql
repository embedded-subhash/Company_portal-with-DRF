CREATE INDEX IF NOT EXISTS idx_employee_id
ON employees_employee(employee_id);

CREATE INDEX IF NOT EXISTS idx_employee_email
ON employees_employee(email);

CREATE INDEX IF NOT EXISTS idx_department
ON employees_employee(department_id);

CREATE INDEX IF NOT EXISTS idx_joining_date
ON employees_employee(joining_date);

CREATE INDEX IF NOT EXISTS idx_salary
ON employees_employee(salary);

CREATE INDEX IF NOT EXISTS idx_department_salary
ON employees_employee(department_id, salary);