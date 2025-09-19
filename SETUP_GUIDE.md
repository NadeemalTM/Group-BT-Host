# Installation and Setup Guide

## Python Installation Issues

If you encounter Python-related errors, follow these steps:

### Option 1: Install Python from Official Website (Recommended)

1. **Download Python**
   - Go to https://python.org/downloads/
   - Download Python 3.9+ (64-bit recommended)
   - **Important**: Check "Add Python to PATH" during installation
   - **Important**: Check "Install for all users"

2. **Verify Installation**
   ```cmd
   python --version
   pip --version
   ```

### Option 2: Use Microsoft Store Python

1. **Install from Microsoft Store**
   - Open Microsoft Store
   - Search for "Python 3.11" or "Python 3.12"
   - Install the official Python package

2. **Test Installation**
   ```cmd
   python --version
   ```

### Option 3: Use Anaconda/Miniconda

1. **Download Anaconda**
   - Go to https://anaconda.com/download
   - Download and install Anaconda

2. **Create Environment**
   ```cmd
   conda create -n bluetooth-music python=3.11
   conda activate bluetooth-music
   ```

## Fixing Common Issues

### Tkinter Issues

If you get Tcl/Tk errors:

1. **Reinstall Python** with full Tcl/Tk support
2. **Or use alternative** GUI framework:

```python
# Alternative: Use PyQt5 instead of Tkinter
pip install PyQt5
```

### Bluetooth Issues

For Bluetooth functionality on Windows:

1. **Enable Bluetooth**
   - Windows Settings > Devices > Bluetooth & other devices
   - Turn on Bluetooth

2. **Install Bluetooth Drivers**
   - Device Manager > Bluetooth
   - Update all Bluetooth drivers

3. **Alternative: Use Windows Built-in Tools**
   ```powershell
   # Check Bluetooth status
   Get-Service -Name "bthserv"
   
   # Restart Bluetooth service if needed
   Restart-Service -Name "bthserv"
   ```

## Quick Test Commands

```cmd
# Test Python installation
python -c "print('Python works!')"

# Test Tkinter
python -c "import tkinter; print('Tkinter works!')"

# Test threading
python -c "import threading; print('Threading works!')"

# Test file operations
python -c "import os; print('File operations work!')"
```

## Running the Application

### Method 1: Command Line
```cmd
cd "path\to\bluetooth-music-player"
python main.py
```

### Method 2: Batch File
Double-click `run.bat`

### Method 3: Demo Mode
If main application fails:
```cmd
python demo.py
```

## Troubleshooting

### Error: "python is not recognized"
- Python not in PATH
- Reinstall Python with "Add to PATH" checked
- Or use full path: `C:\Python39\python.exe main.py`

### Error: "No module named 'pygame'"
```cmd
pip install pygame
pip install mutagen
pip install pillow
pip install numpy
```

### Error: "Can't find init.tcl"
- Tkinter not properly installed
- Try: `pip install tk`
- Or reinstall Python with all components

### Bluetooth Not Working
- Check Windows Bluetooth settings
- Ensure devices are discoverable
- Try pairing through Windows first
- Restart Bluetooth service

## Alternative Approaches

If the full application doesn't work, you can:

1. **Use the Demo Version** (`demo.py`) - simulates Bluetooth functionality
2. **Use Windows Built-in Audio Routing** - pair devices manually and use system audio
3. **Use Third-party Software** - like VB-Audio Cable for audio routing

## System Requirements Verification

```cmd
# Check Windows version
winver

# Check Bluetooth capability
devmgmt.msc
# Look for Bluetooth section

# Check audio devices
mmsys.cpl
# Check playback devices
```

## Getting Help

If you continue having issues:

1. Check Python version: `python --version`
2. Check installed packages: `pip list`
3. Check system information: `systeminfo`
4. Run demo mode: `python demo.py`

The demo mode will show you how the interface should work, even without real Bluetooth functionality.