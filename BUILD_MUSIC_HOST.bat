@echo off
echo ================================================
echo Music Host by Nadeemal - Executable Builder
echo ================================================
echo.
echo This will create a standalone .exe file that works
echo on any Windows computer without requiring Python.
echo.
echo Building "Music Host by Nadeemal"...
echo ✓ Captures any Windows audio (YouTube, Spotify, etc.)
echo ✓ Streams to multiple Bluetooth devices simultaneously  
echo ✓ Professional interface with modern design
echo ✓ No Python installation required on target computers
echo.
pause

cd "e:\Works\python softwares\Bluetooth"

REM Find the best Python installation
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
echo Running Music Host builder...
"%PYTHON_EXE%" build_music_host.py

echo.
echo Build process completed!
echo.
echo Check the 'dist' folder for your standalone application:
echo   • MusicHostByNadeemal.exe - Ready to distribute
echo   • MusicHost_Portable/ - Complete portable package
echo.
echo Your friends can now run this on any Windows computer
echo without installing Python!
echo.
pause