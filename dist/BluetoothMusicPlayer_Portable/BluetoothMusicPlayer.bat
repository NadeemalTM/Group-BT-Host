@echo off
setlocal

REM Bluetooth Music Player Launcher
REM This batch file includes Python and the application

echo ================================================
echo Bluetooth Multi-Device Music Player
echo Portable Installation Package
echo ================================================
echo.

REM Check if we're running from the right location
if not exist "app\console_demo.py" (
    echo Error: Application files not found
    echo Please run this from the application directory
    pause
    exit /b 1
)

REM Try to find Python
set PYTHON_EXE=

REM Check for embedded Python (if included)
if exist "python\python.exe" (
    set PYTHON_EXE=python\python.exe
    echo Found embedded Python
    goto :run_app
)

REM Check common Python installations
if exist "C:\Python313\python.exe" (
    set PYTHON_EXE=C:\Python313\python.exe
    echo Found Python 3.13
    goto :run_app
)

if exist "C:\Python311\python.exe" (
    set PYTHON_EXE=C:\Python311\python.exe
    echo Found Python 3.11
    goto :run_app
)

if exist "C:\Python312\python.exe" (
    set PYTHON_EXE=C:\Python312\python.exe
    echo Found Python 3.12
    goto :run_app
)

REM Try python in PATH
python --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_EXE=python
    echo Found Python in PATH
    goto :run_app
)

REM Python not found
echo Error: Python not found!
echo.
echo This application requires Python to run.
echo Please either:
echo   1. Install Python from https://python.org
echo   2. Use the standalone .exe version (if available)
echo.
echo Python installation guide:
echo   - Download Python 3.11 or newer
echo   - During installation, check "Add Python to PATH"
echo   - Restart your computer after installation
echo.
pause
exit /b 1

:run_app
echo Starting Bluetooth Music Player...
echo Using: %PYTHON_EXE%
echo.

cd app
"%PYTHON_EXE%" console_demo.py

if errorlevel 1 (
    echo.
    echo Application exited with an error.
    echo If you see import errors, the Python installation may be incomplete.
    echo.
)

echo.
echo Application finished.
pause
