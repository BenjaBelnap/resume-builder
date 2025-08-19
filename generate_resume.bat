@echo off
echo Installing required packages...
pip install -r requirements.txt

echo.
echo Generating resume PDF...
python resume_generator.py

echo.
echo Done! Check resume.pdf
pause
