if not exist .\venv (
    md venv
)
if not exist .\venv\Scripts\activate.bat (
    python -m venv .\venv
)
call .\venv\Scripts\activate.bat
pip install -r requirements.txt
python prepare.py
deactivate
