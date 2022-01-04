if not exist .\venv (
    md venv
)
if not exist .\venv\Scripts\activate.bat (
    py -m venv .\venv
)
call .\venv\Scripts\activate.bat
py -m pip install -r requirements.txt
py prepare.py
deactivate
