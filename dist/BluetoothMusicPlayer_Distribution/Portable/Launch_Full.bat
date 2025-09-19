@echo off
echo Starting Bluetooth Music Player (Full Version)...
echo.

REM Change to app directory
cd /d "%~dp0app"

REM Determine which Python to use
set PYTHON_EXE=

REM Try Python 3.13 (detected on your system)
if exist "C:\Python313\python.exe" (
    set PYTHON_EXE=C:\Python313\python.exe
    echo Found Python 3.13
    goto :install_deps
)

REM Try standard PATH python
python --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_EXE=python
    echo Found Python in PATH
    goto :install_deps
)

REM Try py launcher
py --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_EXE=py
    echo Found Python launcher
    goto :install_deps
)

REM Try other common installations
if exist "C:\Python39\python.exe" (
    set PYTHON_EXE=C:\Python39\python.exe
    echo Found Python 3.9
    goto :install_deps
)

if exist "C:\Python310\python.exe" (
    set PYTHON_EXE=C:\Python310\python.exe
    echo Found Python 3.10
    goto :install_deps
)

if exist "C:\Python311\python.exe" (
    set PYTHON_EXE=C:\Python311\python.exe
    echo Found Python 3.11
    goto :install_deps
)

if exist "C:\Python312\python.exe" (
    set PYTHON_EXE=C:\Python312\python.exe
    echo Found Python 3.12
    goto :install_deps
)

REM Python not found
echo Error: Python not found!
echo Please install Python and try again.
pause
exit /b 1

:install_deps
echo.
echo Installing/checking dependencies...
echo This may take a moment...

REM Try to install dependencies (may fail if pip issues exist)
"%PYTHON_EXE%" -m pip install pygame mutagen pillow numpy 2>nul
if errorlevel 1 (
    echo Warning: Could not install some dependencies
    echo The application may still work in demo mode
)

echo.
echo Starting full application...
"%PYTHON_EXE%" main.py
if errorlevel 1 (
    echo.
    echo Full version failed, trying demo version instead...
    "%PYTHON_EXE%" demo.py
)

echo.
echo Application finished. Press any key to close...
pause >nul
