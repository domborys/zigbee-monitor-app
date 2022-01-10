@echo off
set projpath=%~dp0..\..
call %projpath\venv\Scripts\activate.bat
sphinx-apidoc -f -o %~dp0source projpath
call make clean
call make html
deactivate