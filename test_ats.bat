@echo off
echo Installing PDF analysis libraries...
pip install pdfplumber

echo.
echo Running ATS Compatibility Test...
python ats_tester.py

echo.
pause
