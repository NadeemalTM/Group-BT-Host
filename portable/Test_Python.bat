@echo off
echo ================================================
echo Python Installation Test
echo ================================================
echo.

echo Testing Python 3.13 (detected on your system)...
if exist "C:\Python313\python.exe" (
    echo Found: C:\Python313\python.exe
    "C:\Python313\python.exe" --version
    echo.
    
    echo Testing basic Python functionality...
    "C:\Python313\python.exe" -c "print('Python works!')"
    
    echo Testing Tkinter (GUI library)...
    "C:\Python313\python.exe" -c "import tkinter; print('Tkinter works!')" 2>nul
    if errorlevel 1 (
        echo Tkinter not working - this may cause GUI issues
    )
    
    echo Testing other modules...
    "C:\Python313\python.exe" -c "import threading, os, sys, time; print('Core modules work!')"
    
    echo.
    echo Testing pip...
    "C:\Python313\python.exe" -m pip --version 2>nul
    if errorlevel 1 (
        echo pip not working - cannot install packages
        echo This explains the dependency installation failures
    ) else (
        echo pip works!
    )
    
) else (
    echo C:\Python313\python.exe not found
)

echo.
echo Testing standard Python in PATH...
python --version >nul 2>&1
if not errorlevel 1 (
    echo python command works in PATH
    python --version
) else (
    echo python not found in PATH
)

echo.
echo Testing Python launcher...
py --version >nul 2>&1
if not errorlevel 1 (
    echo py launcher works
    py --version
) else (
    echo py launcher not found
)

echo.
echo ================================================
echo Test Results Summary
echo ================================================

if exist "C:\Python313\python.exe" (
    echo Python 3.13 installation found
    echo Demo version should work with fixed launchers
    
    "C:\Python313\python.exe" -m pip --version >nul 2>&1
    if errorlevel 1 (
        echo pip issues detected - full version may have problems
        echo Recommendation: Use demo version
    ) else (
        echo pip works - full version should work too
    )
) else (
    echo No Python installation found
    echo Please install Python from https://python.org
)

echo.
pause