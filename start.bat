@echo off
echo Starting 美股估值器...
cd /d "%~dp0"
"C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Scripts\streamlit.exe" run app.py
pause
