REM --------------------------- DELETE MIGRATIONS ------------------------------
call .\commands\delete_migrations.bat
REM ---------------------------- RESET DATABASE --------------------------------
python .\commands\scripts\reset_db.py
REM ---------------------------- MAKE MIGRATIONS -------------------------------
call .\commands\migrations.bat
