@echo off
echo 📱 Smart Clipboard WhatsApp Sender
echo ================================
echo.
echo Starting the application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

REM Install requirements if needed
if not exist "venv" (
    echo 📦 Setting up virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install requirements
echo 📥 Installing/updating requirements...
pip install -r requirements.txt

REM Run the application
echo 🚀 Launching Smart Clipboard WhatsApp Sender...
echo.
python main.py

REM Deactivate virtual environment
deactivate

echo.
echo Application closed. Press any key to exit...
pause >nul
