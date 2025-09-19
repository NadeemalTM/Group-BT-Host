@echo off
echo ================================================
echo Alternative Build Method - Portable Approach
echo ================================================
echo.

echo The current Python installation appears to have issues.
echo Let's create a portable version instead.
echo.

REM Create portable folder structure
if not exist "portable" mkdir portable
if not exist "portable\app" mkdir portable\app
if not exist "portable\docs" mkdir portable\docs

echo Copying application files...
copy "main.py" "portable\app\" >nul
copy "demo.py" "portable\app\" >nul
copy "bluetooth_manager.py" "portable\app\" >nul
copy "audio_engine.py" "portable\app\" >nul
copy "gui_components.py" "portable\app\" >nul
copy "requirements.txt" "portable\app\" >nul

echo Copying documentation...
copy "README.md" "portable\docs\" >nul
copy "SETUP_GUIDE.md" "portable\docs\" >nul
copy "PROJECT_SUMMARY.md" "portable\docs\" >nul
copy "BUILD_GUIDE.md" "portable\docs\" >nul

REM Create launcher scripts
echo Creating launcher scripts...

REM Main app launcher
(
echo @echo off
echo echo Starting Bluetooth Music Player...
echo echo.
echo REM Try different Python executables
echo python demo.py 2^>nul
echo if errorlevel 1 ^(
echo     py demo.py 2^>nul
echo     if errorlevel 1 ^(
echo         python3 demo.py 2^>nul
echo         if errorlevel 1 ^(
echo             echo Error: Python not found or not working properly
echo             echo.
echo             echo Please install Python from https://python.org
echo             echo Make sure to check "Add Python to PATH" during installation
echo             echo.
echo             pause
echo             exit /b 1
echo         ^)
echo     ^)
echo ^)
) > "portable\Launch_Demo.bat"

REM Full app launcher
(
echo @echo off
echo echo Starting Bluetooth Music Player ^(Full Version^)...
echo echo.
echo echo Installing dependencies...
echo pip install pygame mutagen pillow numpy 2^>nul
echo if errorlevel 1 echo Warning: Some dependencies may not be installed
echo echo.
echo echo Starting application...
echo python main.py 2^>nul
echo if errorlevel 1 ^(
echo     echo Full version failed, trying demo version...
echo     python demo.py
echo ^)
) > "portable\Launch_Full.bat"

REM Setup script
(
echo @echo off
echo echo ================================================
echo echo Bluetooth Music Player - First Time Setup
echo echo ================================================
echo echo.
echo echo This will install required Python packages.
echo echo Make sure you have Python installed first.
echo echo.
echo pause
echo echo.
echo echo Installing packages...
echo pip install pygame mutagen pillow numpy pyinstaller
echo echo.
echo echo Setup complete! You can now use the launcher scripts.
echo pause
) > "portable\Setup.bat"

REM Create README for portable version
(
echo # Bluetooth Music Player - Portable Version
echo.
echo This is a portable version that works with any Python installation.
echo.
echo ## Quick Start
echo.
echo 1. **First Time Setup:**
echo    - Make sure Python is installed on your system
echo    - Double-click `Setup.bat` to install dependencies
echo.
echo 2. **Running the Application:**
echo    - Double-click `Launch_Demo.bat` for demo version ^(recommended^)
echo    - Double-click `Launch_Full.bat` for full version
echo.
echo 3. **Demo vs Full Version:**
echo    - **Demo**: Simulates Bluetooth functionality, works anywhere
echo    - **Full**: Real Bluetooth features, needs compatible hardware
echo.
echo ## Files Included
echo.
echo - `Launch_Demo.bat` - Start demo version
echo - `Launch_Full.bat` - Start full version  
echo - `Setup.bat` - Install Python dependencies
echo - `app\` - Application source code
echo - `docs\` - Documentation files
echo.
echo ## System Requirements
echo.
echo - Windows 10/11
echo - Python 3.7+ ^(download from python.org^)
echo - Bluetooth adapter ^(for full version^)
echo.
echo ## Troubleshooting
echo.
echo If launchers don't work:
echo 1. Open Command Prompt in the `app` folder
echo 2. Run: `python demo.py`
echo 3. Check that Python is installed and in PATH
echo.
echo For more help, see the documentation in the `docs` folder.
) > "portable\README.txt"

REM Create desktop shortcuts
echo Creating desktop shortcuts...
set DESKTOP=%USERPROFILE%\Desktop

REM Demo shortcut
(
echo @echo off
echo cd /d "%~dp0"
echo start "" "Launch_Demo.bat"
) > "%DESKTOP%\Bluetooth Music Player Demo.bat"

REM Full version shortcut
(
echo @echo off
echo cd /d "%~dp0"
echo start "" "Launch_Full.bat"
) > "%DESKTOP%\Bluetooth Music Player.bat"

echo.
echo ================================================
echo Portable Version Created Successfully!
echo ================================================
echo.
echo Created in: portable\
echo.
echo What you get:
echo   ✓ Launch_Demo.bat      - Demo version launcher
echo   ✓ Launch_Full.bat      - Full version launcher
echo   ✓ Setup.bat            - Dependency installer
echo   ✓ README.txt           - Instructions
echo   ✓ app\                 - Source code
echo   ✓ docs\                - Documentation
echo.
echo Desktop shortcuts created:
echo   ✓ Bluetooth Music Player Demo.bat
echo   ✓ Bluetooth Music Player.bat
echo.
echo Next Steps:
echo 1. Test by double-clicking portable\Launch_Demo.bat
echo 2. Share the entire 'portable' folder with others
echo 3. Recipients only need Python installed
echo 4. No complex setup required!
echo.
pause