"""
Installation and Setup Script for Bluetooth Multi-Device Music Player
This script will install required dependencies and set up the application.
"""

import subprocess
import sys
import os
import platform

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    print(f"✓ Python version: {sys.version.split()[0]}")
    return True

def install_pip_packages():
    """Install required Python packages."""
    packages = [
        "pygame==2.5.2",
        "pybluez==0.23", 
        "pyaudio==0.2.11",
        "mutagen==1.47.0",
        "pillow==10.0.1",
        "numpy==1.24.3"
    ]
    
    print("Installing Python packages...")
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✓ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install {package}: {e}")
            return False
    
    return True

def install_windows_bluetooth():
    """Install Windows-specific Bluetooth packages."""
    if platform.system() != "Windows":
        print("Skipping Windows-specific packages (not on Windows)")
        return True
    
    windows_packages = [
        "pycaw==20220416"
    ]
    
    print("Installing Windows-specific packages...")
    
    for package in windows_packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✓ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to install {package}: {e}")
            print("This package is optional and the application may still work.")
    
    return True

def check_bluetooth_adapter():
    """Check if Bluetooth adapter is available."""
    try:
        if platform.system() == "Windows":
            result = subprocess.run(
                ["powershell", "-Command", "Get-NetAdapter | Where-Object {$_.InterfaceDescription -like '*Bluetooth*'}"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.stdout.strip():
                print("✓ Bluetooth adapter detected")
                return True
            else:
                print("⚠ No Bluetooth adapter detected. Please ensure Bluetooth is enabled.")
                return False
        else:
            print("Bluetooth check skipped (Windows only)")
            return True
            
    except Exception as e:
        print(f"Warning: Could not check Bluetooth adapter: {e}")
        return True

def create_desktop_shortcut():
    """Create a desktop shortcut for the application."""
    try:
        if platform.system() == "Windows":
            import winshell
            from win32com.client import Dispatch
            
            desktop = winshell.desktop()
            path = os.path.join(desktop, "Bluetooth Music Player.lnk")
            target = os.path.join(os.getcwd(), "main.py")
            wDir = os.getcwd()
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = sys.executable
            shortcut.Arguments = f'"{target}"'
            shortcut.WorkingDirectory = wDir
            shortcut.IconLocation = sys.executable
            shortcut.save()
            
            print("✓ Desktop shortcut created")
            return True
            
    except ImportError:
        print("Note: Install 'pywin32' and 'winshell' to create desktop shortcut")
    except Exception as e:
        print(f"Warning: Could not create desktop shortcut: {e}")
    
    return False

def setup_audio_drivers():
    """Check and provide information about audio drivers."""
    print("\\nAudio Driver Information:")
    print("For best compatibility with multiple Bluetooth devices:")
    print("1. Ensure Windows is up to date")
    print("2. Install latest Bluetooth drivers from your device manufacturer")
    print("3. Enable 'Stereo Audio' in Bluetooth device properties")
    print("4. Disable audio enhancements that might interfere with multi-device playback")

def main():
    """Main setup function."""
    print("=" * 60)
    print("Bluetooth Multi-Device Music Player - Setup")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install packages
    if not install_pip_packages():
        print("\\nSetup failed: Could not install required packages")
        return False
    
    # Install Windows-specific packages
    install_windows_bluetooth()
    
    # Check Bluetooth
    check_bluetooth_adapter()
    
    # Create shortcut
    create_desktop_shortcut()
    
    # Audio driver info
    setup_audio_drivers()
    
    print("\\n" + "=" * 60)
    print("Setup completed successfully!")
    print("=" * 60)
    print("\\nTo run the application:")
    print(f"1. Navigate to: {os.getcwd()}")
    print("2. Run: python main.py")
    print("\\nOr use the desktop shortcut if created.")
    print("\\nFor troubleshooting, see README.md")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\\nSetup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\\nSetup failed with error: {e}")
        sys.exit(1)