@echo off
echo Installing required packages...
pip install -r requirements.txt

echo.
echo Building resume and cover letter PDFs...
python src/build.py

echo.
echo Done! Check the output/ directory for your PDFs
pause
