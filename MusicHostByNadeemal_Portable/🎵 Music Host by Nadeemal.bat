@echo off
title Music Host by Nadeemal - Universal Audio Streaming
color 0A
echo.
echo ================================================
echo    🎵 Music Host by Nadeemal 🎵
echo    Universal Audio Streaming
echo ================================================
echo.
echo Captures any Windows audio and streams to
echo multiple Bluetooth devices simultaneously!
echo.
echo Perfect for: Parties, Group Listening, Multi-room Audio
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Python not detected in PATH
    echo.
    echo Checking common Python locations...
    
    REM Try common Python installation paths
    set PYTHON_FOUND=0
    
    if exist "C:\Python39\python.exe" (
        set PYTHON_EXE=C:\Python39\python.exe
        set PYTHON_FOUND=1
    ) else if exist "C:\Python310\python.exe" (
        set PYTHON_EXE=C:\Python310\python.exe
        set PYTHON_FOUND=1
    ) else if exist "C:\Python311\python.exe" (
        set PYTHON_EXE=C:\Python311\python.exe
        set PYTHON_FOUND=1
    ) else if exist "C:\Python312\python.exe" (
        set PYTHON_EXE=C:\Python312\python.exe
        set PYTHON_FOUND=1
    ) else if exist "C:\Python313\python.exe" (
        set PYTHON_EXE=C:\Python313\python.exe
        set PYTHON_FOUND=1
    ) else if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python39\python.exe" (
        set PYTHON_EXE=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python39\python.exe
        set PYTHON_FOUND=1
    ) else if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe" (
        set PYTHON_EXE=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe
        set PYTHON_FOUND=1
    ) else if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe" (
        set PYTHON_EXE=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe
        set PYTHON_FOUND=1
    ) else if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" (
        set PYTHON_EXE=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe
        set PYTHON_FOUND=1
    ) else if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\python.exe" (
        set PYTHON_EXE=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\python.exe
        set PYTHON_FOUND=1
    )
    
    if %PYTHON_FOUND%==0 (
        echo.
        echo ❌ Python not found on this system
        echo.
        echo 📥 To use Music Host by Nadeemal, please:
        echo 1. Download Python from https://python.org
        echo 2. During installation, check "Add Python to PATH"
        echo 3. Run this launcher again
        echo.
        echo 💡 Alternatively, ask the person who shared this
        echo    to create a standalone .exe version for you.
        echo.
        pause
        exit /b 1
    )
    
    echo ✅ Found Python: %PYTHON_EXE%
    echo.
) else (
    set PYTHON_EXE=python
    echo ✅ Python found in PATH
    echo.
)

echo 🚀 Starting Music Host by Nadeemal...
echo.

REM Try GUI version first
echo Attempting to start GUI interface...
%PYTHON_EXE% music_host_gui_simple.py 2>nul
if errorlevel 1 (
    echo.
    echo ⚠️  GUI version failed to start
    echo 💻 Starting console version instead...
    echo.
    echo ╔══════════════════════════════════════════════╗
    echo ║  Console version provides the same features  ║
    echo ║  Use menu options to control your audio      ║
    echo ╚══════════════════════════════════════════════╝
    echo.
    %PYTHON_EXE% music_host_console.py
) else (
    echo ✅ GUI started successfully!
)

echo.
echo Thank you for using Music Host by Nadeemal! 🎵
pause