echo creating virtual environment
python -m venv venv
call venv\Scripts\activate.bat
echo installing dependencies
pip install -r requirements.txt