@echo off
echo 🎓 Starting Alphabet Learning App...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if main.py exists
if not exist "main.py" (
    echo ❌ main.py not found in current directory
    pause
    exit /b 1
)

REM Run the application
echo 🚀 Launching the app...
python main.py

REM If there was an error, pause to show the message
if errorlevel 1 (
    echo.
    echo ❌ An error occurred while running the app
    pause
) 