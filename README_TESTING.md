# HRMS Testing Guide

## Running the suite

1. Activate the virtual environment.
2. Run:
   - `python manage.py test`
   - `coverage run --source='accounts,employees,departments,documents,reports,logs,api' manage.py test`
   - `coverage html`
   - `coverage report -m`

## Coverage target

- Minimum target: 85%

## What is covered

- Model validation and ORM behavior
- Authentication and JWT flows
- Permission enforcement
- Report generation
- Document upload/download endpoints
- Fixture loading and test data setup

## Suggested workflow

- Run the suite locally before each release.
- Review failures in the test report.
- Expand tests for any newly introduced business logic.
