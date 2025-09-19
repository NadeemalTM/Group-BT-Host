@echo off
echo ================================================
echo Bluetooth Music Player - Direct Launcher
echo ================================================
echo.

echo Using Python 3.13 directly...
cd /d "%~dp0app"

echo Starting demo version...
"C:\Python313\python.exe" demo.py

if errorlevel 1 (
    echo.
    echo Demo failed. Checking Python installation...
    "C:\Python313\python.exe" --version
    echo.
    echo If you see version info above, Python works.
    echo The issue might be with the application code.
    echo.
    echo Try running manually:
    echo 1. Open Command Prompt
    echo 2. Navigate to: %~dp0app
    echo 3. Run: "C:\Python313\python.exe" demo.py
    echo.
)

echo.
pause