# Alternative simple build script
# Run this if build_exe.py has issues

import subprocess
import sys
import os

def simple_build():
    """Simple PyInstaller build."""
    print("Installing PyInstaller...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    print("Building demo executable...")
    subprocess.run([
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed", 
        "--name=BluetoothMusicDemo",
        "demo.py"
    ])
    
    print("Building main executable...")
    subprocess.run([
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--name=BluetoothMusicPlayer",
        "main.py"
    ])
    
    print("Done! Check the 'dist' folder for executables.")

if __name__ == "__main__":
    simple_build()