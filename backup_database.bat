@echo off

echo Creating database backup...

pg_dump -U postgres company_db > sql\backup.sql

echo Backup completed successfully!
pause