@echo off
echo Installing PDF analysis libraries...
pip install pdfplumber

echo.
echo Running ATS Compatibility Test...
python src/ats_tester.py

echo.
pause
