@echo off
echo ================================================
echo Bluetooth Music Player - Console Version
echo ================================================
echo.

echo This version works without GUI libraries
echo Starting console application...
echo.

cd /d "%~dp0app"
"C:\Python313\python.exe" console_demo.py

echo.
echo Application finished.
pause