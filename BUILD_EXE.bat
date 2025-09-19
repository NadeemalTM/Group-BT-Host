@echo off
echo ================================================
echo Bluetooth Music Player - Executable Builder
echo ================================================
echo.
echo This will create standalone .exe files that can be
echo installed on other computers without Python.
echo.
echo Building multiple versions for maximum compatibility...
echo.
pause

cd "e:\Works\python softwares\Bluetooth"

REM Try to use the best available Python
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
echo Running advanced builder...
"%PYTHON_EXE%" advanced_build.py

echo.
echo Build process completed!
echo.
echo Check the 'dist' folder for generated .exe files
echo.
pause