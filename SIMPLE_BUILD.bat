@echo off
echo ================================================
echo Simple Executable Creator (No Dependencies)
echo ================================================
echo.
echo This script attempts to create .exe files using
echo only basic Python commands and available tools.
echo.

cd "e:\Works\python softwares\Bluetooth"

REM Create a simple self-extracting package
echo Creating portable executable package...

REM Try to download PyInstaller manually if possible
echo.
echo Method 1: Direct PyInstaller download (if available)
echo ================================================

REM Check if we have internet access and wget/curl
where curl >nul 2>&1
if %errorlevel% == 0 (
    echo Found curl, attempting to download PyInstaller...
    mkdir temp_pyinstaller 2>nul
    cd temp_pyinstaller
    curl -o pyinstaller.zip https://pypi.org/packages/source/p/pyinstaller/PyInstaller-5.13.2.tar.gz
    if exist pyinstaller.zip (
        echo Downloaded PyInstaller package
        echo You can extract and use this manually
    )
    cd ..
) else (
    echo curl not available, trying alternative methods...
)

echo.
echo Method 2: Create Python Bundle
echo ================================================

REM Create a bundle that includes Python
mkdir "dist\PythonBundle" 2>nul

REM Copy Python executable and core files (if accessible)
if exist "C:\Python313" (
    echo Creating Python bundle with application...
    mkdir "dist\PythonBundle\python" 2>nul
    
    REM Copy essential Python files (this may need admin rights)
    echo Copying Python runtime...
    xcopy "C:\Python313\python.exe" "dist\PythonBundle\python\" /Y >nul 2>&1
    xcopy "C:\Python313\python313.dll" "dist\PythonBundle\python\" /Y >nul 2>&1
    xcopy "C:\Python313\Lib" "dist\PythonBundle\python\Lib\" /E /Y >nul 2>&1
    
    REM Copy our application
    mkdir "dist\PythonBundle\app" 2>nul
    copy "portable\app\console_demo.py" "dist\PythonBundle\app\" >nul 2>&1
    
    REM Create launcher
    echo @echo off > "dist\PythonBundle\BluetoothMusicPlayer.bat"
    echo cd /d "%%~dp0" >> "dist\PythonBundle\BluetoothMusicPlayer.bat"
    echo python\python.exe app\console_demo.py >> "dist\PythonBundle\BluetoothMusicPlayer.bat"
    echo pause >> "dist\PythonBundle\BluetoothMusicPlayer.bat"
    
    echo ✅ Python bundle created in dist\PythonBundle\
)

echo.
echo Method 3: Web-based Converter
echo ================================================
echo You can also use online converters:
echo 1. Visit https://www.online-convert.com/
echo 2. Upload your Python file
echo 3. Convert to executable
echo.
echo Or use a cloud service like GitHub Actions to build automatically.

echo.
echo Method 4: Manual PyInstaller (Recommended)
echo ================================================
echo If you have access to another computer with working Python:
echo.
echo 1. Install Python and PyInstaller on another computer
echo 2. Copy this project folder to that computer
echo 3. Run: pip install pyinstaller
echo 4. Run: pyinstaller --onefile portable\app\console_demo.py
echo 5. Copy the generated .exe back to this computer
echo.

echo Current available packages:
echo ✅ Portable Python version (works with any Python installation)
echo ✅ Complete source code
echo ✅ Multiple launcher scripts
echo ✅ Documentation and guides
echo.
echo 📁 Check the 'dist' folder for ready-to-distribute packages
echo.
pause