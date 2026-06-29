@echo off

echo Restoring database...

psql -U postgres company_db < sql\backup.sql

echo Database restored successfully!
pause