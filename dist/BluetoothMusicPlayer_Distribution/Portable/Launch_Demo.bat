@echo off
echo Starting Bluetooth Music Player (Demo)...
echo.

REM Change to app directory
cd /d "%~dp0app"

REM Try different Python executables in order of preference
echo Searching for Python installation...

REM Try Python 3.13 (detected on your system)
if exist "C:\Python313\python.exe" (
    echo Found Python 3.13, starting application...
    "C:\Python313\python.exe" demo.py
    goto :success
)

REM Try standard PATH python
python --version >nul 2>&1
if not errorlevel 1 (
    echo Found Python in PATH, starting application...
    python demo.py
    goto :success
)

REM Try py launcher
py --version >nul 2>&1
if not errorlevel 1 (
    echo Found Python launcher, starting application...
    py demo.py
    goto :success
)

REM Try other common Python installations
if exist "C:\Python39\python.exe" (
    echo Found Python 3.9, starting application...
    "C:\Python39\python.exe" demo.py
    goto :success
)

if exist "C:\Python310\python.exe" (
    echo Found Python 3.10, starting application...
    "C:\Python310\python.exe" demo.py
    goto :success
)

if exist "C:\Python311\python.exe" (
    echo Found Python 3.11, starting application...
    "C:\Python311\python.exe" demo.py
    goto :success
)

if exist "C:\Python312\python.exe" (
    echo Found Python 3.12, starting application...
    "C:\Python312\python.exe" demo.py
    goto :success
)

REM If we get here, Python wasn't found
echo Error: Python not found!
echo.
echo We looked for Python in these locations:
echo   - C:\Python313\python.exe (your system)
echo   - Standard PATH locations
echo   - C:\Python39\, C:\Python310\, C:\Python311\, C:\Python312\
echo.
echo Solutions:
echo 1. Install Python from https://python.org
echo 2. Make sure to check "Add Python to PATH" during installation
echo 3. Or reinstall Python with "Add to PATH" option
echo.
pause
exit /b 1

:success
echo.
echo Application finished. Press any key to close...
pause >nul
