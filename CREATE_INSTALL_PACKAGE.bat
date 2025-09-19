@echo off
echo ================================================
echo Creating Installation Package for Other PCs
echo ================================================
echo.

cd "e:\Works\python softwares\Bluetooth"

echo Creating ZIP package for easy distribution...
echo.

REM Try to create ZIP using PowerShell (Windows 10/11)
powershell -command "Compress-Archive -Path 'dist\BluetoothMusicPlayer_Portable\*' -DestinationPath 'BluetoothMusicPlayer_ForInstall.zip' -Force"

if exist "BluetoothMusicPlayer_ForInstall.zip" (
    echo ✅ SUCCESS! Installation package created:
    echo.
    echo 📦 BluetoothMusicPlayer_ForInstall.zip
    echo.
    echo This ZIP file contains everything needed to install
    echo the Bluetooth Music Player on other computers.
    echo.
    echo HOW TO SHARE WITH FRIENDS:
    echo ===========================
    echo 1. Send them the ZIP file ^(email, cloud storage, USB^)
    echo 2. They extract it to any folder
    echo 3. They double-click "BluetoothMusicPlayer.bat"
    echo 4. Done! They can now share music with multiple devices
    echo.
    echo REQUIREMENTS FOR OTHER PCs:
    echo ===========================
    echo - Windows 7/10/11
    echo - Python 3.7+ ^(free from python.org^)
    echo - Bluetooth-enabled computer ^(for real devices^)
    echo.
    echo The application includes:
    echo ✅ Bluetooth device discovery
    echo ✅ Multi-device connection
    echo ✅ Music file loading
    echo ✅ Synchronized playback
    echo ✅ Complete user interface
    echo ✅ Documentation and help
    echo.
) else (
    echo ❌ Could not create ZIP automatically.
    echo.
    echo MANUAL STEPS:
    echo =============
    echo 1. Go to: dist\BluetoothMusicPlayer_Portable\
    echo 2. Select all files and folders
    echo 3. Right-click → Send to → Compressed folder
    echo 4. Rename to "BluetoothMusicPlayer_ForInstall.zip"
    echo 5. Share this ZIP file with friends
    echo.
)

echo SIZE CHECK:
for %%f in (BluetoothMusicPlayer_ForInstall.zip) do echo File size: %%~zf bytes
echo.

echo 🎉 Your Bluetooth Music Player is ready for installation on other PCs!
echo.
echo ALTERNATIVE: If you want a true .exe file:
echo 1. Copy this entire project to a computer with working Python
echo 2. Run: pip install pyinstaller
echo 3. Run: pyinstaller --onefile portable\app\console_demo.py
echo 4. Copy the generated .exe back here
echo.
pause