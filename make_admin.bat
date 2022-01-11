@echo off
call .\venv\Scripts\activate.bat
py make_admin.py %1 %2
call deactivate