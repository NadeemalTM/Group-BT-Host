@echo off
echo Testing Python Installation...
echo.

echo Checking C:\Python313\python.exe...
if exist "C:\Python313\python.exe" (
    echo Found Python 3.13
    "C:\Python313\python.exe" --version
    echo Testing basic functionality...
    "C:\Python313\python.exe" -c "print('Python works!')"
) else (
    echo Python 3.13 not found
)

echo.
echo Checking python in PATH...
python --version 2>nul
if errorlevel 1 (
    echo Python not in PATH
) else (
    echo Python found in PATH
)

echo.
pause