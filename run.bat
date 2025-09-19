@echo off
echo ====================================
echo Bluetooth Multi-Device Music Player
echo Quick Start Script
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://python.org
    pause
    exit /b 1
)

echo Python detected. Starting application...
echo.

REM Run the application
python main.py

if errorlevel 1 (
    echo.
    echo Application exited with an error.
    echo Check the console output above for details.
    echo.
    echo If this is the first run, try running setup.py first:
    echo   python setup.py
    echo.
    pause
)