# Django HR Management System (Employee Database Portal)

A Django-based HR Management System built using PostgreSQL.  
This project demonstrates backend development skills including Django ORM, database modeling, admin customization, and shell-based data operations.

---

## 🚀 Project Overview

This system manages:
- Departments in an organization
- Employees linked to departments via ForeignKey relationship

It provides full CRUD operations using Django Admin and ORM.

---

## 🏗️ Features

### 📁 Department Module
- Create Department
- Update Department
- Delete Department
- Search Department

### 👨‍💼 Employee Module
- Create Employee
- Update Employee
- Delete Employee
- Search Employee
- Filter Employees by Department

---

## 🧠 Models

### Department Model
- name
- description
- created_at
- updated_at

### Employee Model
- employee_id
- first_name
- last_name
- email
- phone
- salary
- joining_date
- designation
- department (ForeignKey)
- status
- created_at
- updated_at

---

## ⚙️ Tech Stack

- Python 3.x
- Django 6.x
- PostgreSQL
- Django ORM
- Django Admin Panel

---

## 📂 Project Structure

``