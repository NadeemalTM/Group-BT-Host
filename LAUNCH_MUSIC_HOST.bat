@echo off
title Music Host by Nadeemal - Universal Audio Streaming
color 0A

echo.
echo ========================================================
echo           🎵 MUSIC HOST BY NADEEMAL 🎵
echo ========================================================
echo           Universal Audio Streaming Solution
echo ========================================================
echo.
echo Stream any Windows audio to multiple Bluetooth devices
echo simultaneously - YouTube, Spotify, games, and more!
echo.
echo Features:
echo ✓ Capture audio from ANY Windows application
echo ✓ Connect to multiple Bluetooth speakers/headphones
echo ✓ Real-time streaming with volume control
echo ✓ Easy-to-use interface
echo ✓ No complex setup required
echo.
echo Perfect for:
echo • House parties with multiple speakers
echo • Sharing music with friends' headphones  
echo • Creating synchronized audio across rooms
echo • Group listening experiences
echo.
pause

cd "e:\Works\python softwares\Bluetooth"

REM Try to find Python installation
set PYTHON_EXE=

if exist "C:\Python313\python.exe" (
    set PYTHON_EXE=C:\Python313\python.exe
    echo Using Python 3.13
) else if exist "C:\Python311\python.exe" (
    set PYTHON_EXE=C:\Python311\python.exe
    echo Using Python 3.11
) else if exist "C:\Python312\python.exe" (
    set PYTHON_EXE=C:\Python312\python.exe
    echo Using Python 3.12
) else (
    set PYTHON_EXE=python
    echo Using Python from PATH
)

echo.
echo Starting Music Host...
echo.

REM Start the console version (most compatible)
"%PYTHON_EXE%" music_host_console.py

REM If console version fails, try GUI version
if errorlevel 1 (
    echo.
    echo Console version failed, trying GUI version...
    "%PYTHON_EXE%" music_host_main.py
)

if errorlevel 1 (
    echo.
    echo ❌ Error starting Music Host
    echo.
    echo Troubleshooting:
    echo 1. Ensure Python is installed from https://python.org
    echo 2. Restart your computer after Python installation
    echo 3. Run as administrator if needed
    echo 4. Check that all files are in the same folder
    echo.
    pause
) else (
    echo.
    echo 👋 Music Host session ended
    echo Thank you for using Music Host by Nadeemal!
    echo.
)

pause