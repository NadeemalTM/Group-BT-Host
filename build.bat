@echo off
echo ================================================
echo Bluetooth Music Player - Executable Builder
echo ================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Trying alternative Python paths...
    
    REM Try common Python installation paths
    if exist "C:\Python39\python.exe" (
        set PYTHON_EXE=C:\Python39\python.exe
    ) else if exist "C:\Python310\python.exe" (
        set PYTHON_EXE=C:\Python310\python.exe
    ) else if exist "C:\Python311\python.exe" (
        set PYTHON_EXE=C:\Python311\python.exe
    ) else if exist "C:\Python312\python.exe" (
        set PYTHON_EXE=C:\Python312\python.exe
    ) else if exist "C:\Python313\python.exe" (
        set PYTHON_EXE=C:\Python313\python.exe
    ) else (
        echo Error: Python not found in common locations
        echo Please install Python from https://python.org
        pause
        exit /b 1
    )
) else (
    set PYTHON_EXE=python
)

echo Using Python: %PYTHON_EXE%
echo.

REM Install PyInstaller
echo Installing PyInstaller...
%PYTHON_EXE% -m pip install pyinstaller
if errorlevel 1 (
    echo Warning: PyInstaller installation failed
    echo Trying alternative approach...
)

REM Create dist directory
if not exist "dist" mkdir dist

echo.
echo Building Demo Executable (recommended)...
echo This version works without external dependencies.
%PYTHON_EXE% -m PyInstaller --onefile --windowed --name=BluetoothMusicDemo --distpath=dist demo.py

if exist "dist\BluetoothMusicDemo.exe" (
    echo ✓ Demo executable created successfully!
) else (
    echo ✗ Demo executable build failed
)

echo.
echo Building Main Executable...
echo This version has full functionality but may require additional files.
%PYTHON_EXE% -m PyInstaller --onefile --windowed --name=BluetoothMusicPlayer --distpath=dist main.py

if exist "dist\BluetoothMusicPlayer.exe" (
    echo ✓ Main executable created successfully!
) else (
    echo ✗ Main executable build failed
)

echo.
echo ================================================
echo Build Complete!
echo ================================================
echo.

if exist "dist\BluetoothMusicDemo.exe" (
    echo ✓ Demo Version: dist\BluetoothMusicDemo.exe
    echo   - Works without Python installation
    echo   - Simulates Bluetooth functionality
    echo   - Good for testing interface
)

if exist "dist\BluetoothMusicPlayer.exe" (
    echo ✓ Full Version: dist\BluetoothMusicPlayer.exe  
    echo   - Complete functionality
    echo   - May need additional setup on target systems
)

echo.
echo Files in dist folder:
dir dist\*.exe 2>nul

echo.
echo Next Steps:
echo 1. Test the executable(s) by double-clicking them
echo 2. Copy to other computers (no Python needed)
echo 3. The demo version is more portable
echo 4. For installation package, see installer_script.iss

pause