@echo off
title Music Host by Nadeemal - GUI Executable Builder
color 0A
echo.
echo ================================================
echo    Music Host by Nadeemal
echo    GUI Executable Builder
echo ================================================
echo.
echo Creating standalone GUI .exe for universal distribution...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! 
    echo.
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo ✅ Python found - building GUI executable...
echo.

REM Run the GUI builder
python build_gui_executable.py

echo.
echo ================================================
echo Build process completed!
echo ================================================
echo.

if exist "dist\MusicHostByNadeemal_Portable" (
    echo 🎉 SUCCESS! Your portable GUI application is ready:
    echo.
    echo 📁 Location: dist\MusicHostByNadeemal_Portable\
    echo 🚀 Launcher: Launch_MusicHost.bat
    echo.
    echo 📋 To distribute to other PCs:
    echo 1. Copy the entire "MusicHostByNadeemal_Portable" folder
    echo 2. Paste it anywhere on the target computer
    echo 3. Double-click "Launch_MusicHost.bat"
    echo 4. No Python installation required on target PCs!
    echo.
    echo Opening the portable folder...
    explorer "dist\MusicHostByNadeemal_Portable"
) else (
    echo ❌ Build may have failed. Check the output above for errors.
    echo.
    echo 🔄 Troubleshooting tips:
    echo 1. Ensure all Python files are in the same folder
    echo 2. Try running: pip install pyinstaller
    echo 3. Check Windows Defender isn't blocking the build
    echo.
)

echo.
pause