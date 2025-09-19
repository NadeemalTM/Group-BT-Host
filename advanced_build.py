"""
Advanced Executable Builder with Multiple Methods
This script tries different approaches to create standalone .exe files
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

class ExecutableBuilder:
    def __init__(self):
        self.project_dir = Path.cwd()
        self.dist_dir = self.project_dir / "dist"
        self.build_dir = self.project_dir / "build"
        self.portable_dir = self.project_dir / "portable"
        
        # Ensure directories exist
        self.dist_dir.mkdir(exist_ok=True)
        
    def check_and_install_tools(self):
        """Check and install required build tools."""
        tools = []
        
        print("🔧 Checking build tools...")
        
        # Check PyInstaller
        try:
            import PyInstaller
            print("✅ PyInstaller already installed")
        except ImportError:
            print("📦 Installing PyInstaller...")
            tools.append("pyinstaller")
        
        # Check auto-py-to-exe (GUI tool)
        try:
            import auto_py_to_exe
            print("✅ auto-py-to-exe already installed")
        except ImportError:
            print("📦 Installing auto-py-to-exe...")
            tools.append("auto-py-to-exe")
        
        # Check cx_Freeze
        try:
            import cx_Freeze
            print("✅ cx_Freeze already installed")
        except ImportError:
            print("📦 Installing cx_Freeze...")
            tools.append("cx_Freeze")
        
        # Try to install missing tools
        if tools:
            for tool in tools:
                try:
                    subprocess.run([sys.executable, "-m", "pip", "install", tool], 
                                 check=True, capture_output=True)
                    print(f"✅ {tool} installed successfully")
                except subprocess.CalledProcessError as e:
                    print(f"❌ Failed to install {tool}: {e}")
                    
        return len(tools) == 0  # Return True if no tools needed installation
    
    def method1_pyinstaller_simple(self):
        """Method 1: Simple PyInstaller build."""
        print("\n🚀 Method 1: PyInstaller Simple Build")
        print("=" * 50)
        
        try:
            # Build console version (most likely to work)
            console_cmd = [
                sys.executable, "-m", "PyInstaller",
                "--onefile",
                "--name=BluetoothMusicConsole",
                "--distpath=dist",
                "--workpath=build/console",
                "portable/app/console_demo.py"
            ]
            
            print("Building console version...")
            result = subprocess.run(console_cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Console executable created successfully!")
                print(f"📁 Location: {self.dist_dir}/BluetoothMusicConsole.exe")
                return True
            else:
                print(f"❌ Console build failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Method 1 failed: {e}")
            return False
    
    def method2_pyinstaller_advanced(self):
        """Method 2: Advanced PyInstaller with spec file."""
        print("\n🚀 Method 2: PyInstaller Advanced Build")
        print("=" * 50)
        
        # Create advanced spec file
        spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

console_analysis = Analysis(
    ['portable/app/console_demo.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('README.md', '.'),
        ('portable/README.txt', '.'),
        ('FIX_GUIDE.md', '.'),
    ],
    hiddenimports=['threading', 'time', 'os', 'sys'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

console_pyz = PYZ(console_analysis.pure, console_analysis.zipped_data, cipher=block_cipher)

console_exe = EXE(
    console_pyz,
    console_analysis.scripts,
    console_analysis.binaries,
    console_analysis.zipfiles,
    console_analysis.datas,
    [],
    name='BluetoothMusicPlayer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''
        
        spec_file = self.project_dir / "bluetooth_music.spec"
        with open(spec_file, 'w') as f:
            f.write(spec_content)
        
        try:
            cmd = [sys.executable, "-m", "PyInstaller", "--clean", str(spec_file)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Advanced executable created successfully!")
                return True
            else:
                print(f"❌ Advanced build failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Method 2 failed: {e}")
            return False
    
    def method3_cx_freeze(self):
        """Method 3: cx_Freeze build."""
        print("\n🚀 Method 3: cx_Freeze Build")
        print("=" * 50)
        
        setup_content = '''
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_options = {
    'packages': [],
    'excludes': ['tkinter', 'matplotlib', 'numpy', 'pandas'],
    'include_files': [
        ('README.md', 'README.md'),
        ('portable/README.txt', 'README.txt'),
    ]
}

base = 'Console'  # Use 'Win32GUI' for GUI applications

executables = [
    Executable('portable/app/console_demo.py', base=base, target_name='BluetoothMusicPlayer.exe')
]

setup(
    name='BluetoothMusicPlayer',
    version='1.0',
    description='Multi-Device Bluetooth Music Player',
    options={'build_exe': build_options},
    executables=executables
)
'''
        
        setup_file = self.project_dir / "setup_cx.py"
        with open(setup_file, 'w') as f:
            f.write(setup_content)
        
        try:
            cmd = [sys.executable, str(setup_file), "build"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ cx_Freeze executable created successfully!")
                # Find and copy the executable
                build_dirs = list(self.project_dir.glob("build/exe.*"))
                if build_dirs:
                    exe_file = build_dirs[0] / "BluetoothMusicPlayer.exe"
                    if exe_file.exists():
                        shutil.copy2(exe_file, self.dist_dir / "BluetoothMusicPlayer_cx.exe")
                        print(f"📁 Copied to: {self.dist_dir}/BluetoothMusicPlayer_cx.exe")
                return True
            else:
                print(f"❌ cx_Freeze build failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Method 3 failed: {e}")
            return False
    
    def method4_create_installer(self):
        """Method 4: Create NSIS installer script."""
        print("\n🚀 Method 4: Creating Installer Script")
        print("=" * 50)
        
        nsis_script = '''
; Bluetooth Music Player Installer
; Created with NSIS

!define APP_NAME "Bluetooth Music Player"
!define APP_VERSION "1.0"
!define APP_PUBLISHER "Your Name"
!define APP_URL "https://github.com/yourusername/bluetooth-music-player"

; Main Install settings
Name "${APP_NAME}"
InstallDir "$PROGRAMFILES\\${APP_NAME}"
InstallDirRegKey HKLM "Software\\${APP_NAME}" ""
OutFile "BluetoothMusicPlayerInstaller.exe"

; Interface Settings
!include "MUI2.nsh"
!define MUI_ABORTWARNING
!define MUI_ICON "app.ico"

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; Languages
!insertmacro MUI_LANGUAGE "English"

; Installation
Section "Main Application" SecMain
    SetOutPath "$INSTDIR"
    
    ; Copy executable files
    File "dist\\BluetoothMusicConsole.exe"
    File "dist\\BluetoothMusicPlayer.exe"
    
    ; Copy documentation
    File "README.md"
    File "portable\\README.txt"
    File "FIX_GUIDE.md"
    
    ; Create shortcuts
    CreateDirectory "$SMPROGRAMS\\${APP_NAME}"
    CreateShortCut "$SMPROGRAMS\\${APP_NAME}\\${APP_NAME}.lnk" "$INSTDIR\\BluetoothMusicConsole.exe"
    CreateShortCut "$SMPROGRAMS\\${APP_NAME}\\${APP_NAME} (Advanced).lnk" "$INSTDIR\\BluetoothMusicPlayer.exe"
    CreateShortCut "$SMPROGRAMS\\${APP_NAME}\\Uninstall.lnk" "$INSTDIR\\Uninstall.exe"
    
    ; Create desktop shortcut
    CreateShortCut "$DESKTOP\\${APP_NAME}.lnk" "$INSTDIR\\BluetoothMusicConsole.exe"
    
    ; Registry
    WriteRegStr HKLM "Software\\${APP_NAME}" "" "$INSTDIR"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}" "DisplayName" "${APP_NAME}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}" "UninstallString" "$INSTDIR\\Uninstall.exe"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}" "Publisher" "${APP_PUBLISHER}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}" "URLInfoAbout" "${APP_URL}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}" "DisplayVersion" "${APP_VERSION}"
    
    ; Uninstaller
    WriteUninstaller "$INSTDIR\\Uninstall.exe"
SectionEnd

; Uninstallation
Section "Uninstall"
    ; Remove files
    Delete "$INSTDIR\\BluetoothMusicConsole.exe"
    Delete "$INSTDIR\\BluetoothMusicPlayer.exe"
    Delete "$INSTDIR\\README.md"
    Delete "$INSTDIR\\README.txt"
    Delete "$INSTDIR\\FIX_GUIDE.md"
    Delete "$INSTDIR\\Uninstall.exe"
    
    ; Remove shortcuts
    Delete "$SMPROGRAMS\\${APP_NAME}\\${APP_NAME}.lnk"
    Delete "$SMPROGRAMS\\${APP_NAME}\\${APP_NAME} (Advanced).lnk"
    Delete "$SMPROGRAMS\\${APP_NAME}\\Uninstall.lnk"
    Delete "$DESKTOP\\${APP_NAME}.lnk"
    RMDir "$SMPROGRAMS\\${APP_NAME}"
    
    ; Remove registry keys
    DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}"
    DeleteRegKey HKLM "Software\\${APP_NAME}"
    
    ; Remove directory
    RMDir "$INSTDIR"
SectionEnd
'''
        
        nsis_file = self.project_dir / "installer.nsi"
        with open(nsis_file, 'w') as f:
            f.write(nsis_script)
        
        print("✅ NSIS installer script created!")
        print(f"📁 Location: {nsis_file}")
        print("📝 To create installer:")
        print("   1. Install NSIS from https://nsis.sourceforge.io/")
        print("   2. Right-click installer.nsi → Compile NSIS Script")
        return True
    
    def method5_batch_wrapper(self):
        """Method 5: Create batch file that runs Python directly."""
        print("\n🚀 Method 5: Batch File Wrapper")
        print("=" * 50)
        
        batch_content = '''@echo off
setlocal

REM Bluetooth Music Player Launcher
REM This batch file includes Python and the application

echo ================================================
echo Bluetooth Multi-Device Music Player
echo Portable Installation Package
echo ================================================
echo.

REM Check if we're running from the right location
if not exist "app\\console_demo.py" (
    echo Error: Application files not found
    echo Please run this from the application directory
    pause
    exit /b 1
)

REM Try to find Python
set PYTHON_EXE=

REM Check for embedded Python (if included)
if exist "python\\python.exe" (
    set PYTHON_EXE=python\\python.exe
    echo Found embedded Python
    goto :run_app
)

REM Check common Python installations
if exist "C:\\Python313\\python.exe" (
    set PYTHON_EXE=C:\\Python313\\python.exe
    echo Found Python 3.13
    goto :run_app
)

if exist "C:\\Python311\\python.exe" (
    set PYTHON_EXE=C:\\Python311\\python.exe
    echo Found Python 3.11
    goto :run_app
)

if exist "C:\\Python312\\python.exe" (
    set PYTHON_EXE=C:\\Python312\\python.exe
    echo Found Python 3.12
    goto :run_app
)

REM Try python in PATH
python --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_EXE=python
    echo Found Python in PATH
    goto :run_app
)

REM Python not found
echo Error: Python not found!
echo.
echo This application requires Python to run.
echo Please either:
echo   1. Install Python from https://python.org
echo   2. Use the standalone .exe version (if available)
echo.
echo Python installation guide:
echo   - Download Python 3.11 or newer
echo   - During installation, check "Add Python to PATH"
echo   - Restart your computer after installation
echo.
pause
exit /b 1

:run_app
echo Starting Bluetooth Music Player...
echo Using: %PYTHON_EXE%
echo.

cd app
"%PYTHON_EXE%" console_demo.py

if errorlevel 1 (
    echo.
    echo Application exited with an error.
    echo If you see import errors, the Python installation may be incomplete.
    echo.
)

echo.
echo Application finished.
pause
'''
        
        # Create standalone package structure
        standalone_dir = self.dist_dir / "BluetoothMusicPlayer_Portable"
        standalone_dir.mkdir(exist_ok=True)
        
        # Copy application files
        app_dir = standalone_dir / "app"
        app_dir.mkdir(exist_ok=True)
        
        if (self.portable_dir / "app" / "console_demo.py").exists():
            shutil.copy2(self.portable_dir / "app" / "console_demo.py", app_dir)
        
        # Copy documentation
        for doc_file in ["README.md", "FIX_GUIDE.md"]:
            if (self.project_dir / doc_file).exists():
                shutil.copy2(self.project_dir / doc_file, standalone_dir)
        
        if (self.portable_dir / "README.txt").exists():
            shutil.copy2(self.portable_dir / "README.txt", standalone_dir)
        
        # Create launcher
        launcher_file = standalone_dir / "BluetoothMusicPlayer.bat"
        with open(launcher_file, 'w') as f:
            f.write(batch_content)
        
        print("✅ Portable package created!")
        print(f"📁 Location: {standalone_dir}")
        print("📦 This package can be zipped and shared")
        return True
    
    def create_distribution_package(self):
        """Create a comprehensive distribution package."""
        print("\n📦 Creating Distribution Package")
        print("=" * 50)
        
        # Create distribution directory
        dist_package = self.dist_dir / "BluetoothMusicPlayer_Distribution"
        dist_package.mkdir(exist_ok=True)
        
        # Copy all available executables
        exe_files = list(self.dist_dir.glob("*.exe"))
        for exe_file in exe_files:
            if exe_file.parent != dist_package:  # Don't copy if already in package
                shutil.copy2(exe_file, dist_package)
                print(f"📁 Copied: {exe_file.name}")
        
        # Copy portable version
        portable_dist = dist_package / "Portable"
        if self.portable_dir.exists():
            shutil.copytree(self.portable_dir, portable_dist, dirs_exist_ok=True)
            print("📁 Copied: Portable version")
        
        # Copy documentation
        doc_files = ["README.md", "FIX_GUIDE.md", "BUILD_GUIDE.md", "DISTRIBUTION_SUMMARY.md"]
        for doc_file in doc_files:
            if (self.project_dir / doc_file).exists():
                shutil.copy2(self.project_dir / doc_file, dist_package)
        
        # Create distribution README
        dist_readme = '''# Bluetooth Multi-Device Music Player - Distribution Package

This package contains multiple versions of the Bluetooth Music Player for maximum compatibility.

## Available Versions:

1. **Executable Files (.exe)**
   - BluetoothMusicConsole.exe - Console version (recommended)
   - BluetoothMusicPlayer.exe - Full version (if available)
   - These run without Python installation

2. **Portable Folder**
   - Contains Python source code version
   - Requires Python installation on target computer
   - Multiple launcher options available

## Quick Start:

### For Non-Technical Users:
1. Try running any .exe file directly
2. If .exe doesn't work, use Portable/Launch_Console.bat

### For Technical Users:
1. Use Portable version for full source code access
2. See documentation files for advanced setup

## System Requirements:
- Windows 10/11
- For .exe files: No additional requirements
- For Portable version: Python 3.7+

## Installation:
1. Copy desired version to target computer
2. Run the executable or launcher
3. Follow on-screen instructions

For detailed instructions, see the included documentation files.
'''
        
        with open(dist_package / "README.txt", 'w') as f:
            f.write(dist_readme)
        
        print(f"✅ Distribution package created: {dist_package}")
        return dist_package
    
    def build_all(self):
        """Build using all available methods."""
        print("🚀 Bluetooth Music Player - Executable Builder")
        print("=" * 60)
        print("Attempting to create standalone .exe files using multiple methods")
        print("=" * 60)
        
        # Check and install tools
        tools_ready = self.check_and_install_tools()
        
        success_methods = []
        
        # Try all methods
        if self.method1_pyinstaller_simple():
            success_methods.append("PyInstaller Simple")
        
        if self.method2_pyinstaller_advanced():
            success_methods.append("PyInstaller Advanced")
        
        if self.method3_cx_freeze():
            success_methods.append("cx_Freeze")
        
        if self.method4_create_installer():
            success_methods.append("NSIS Installer Script")
        
        if self.method5_batch_wrapper():
            success_methods.append("Portable Batch Package")
        
        # Create distribution package
        dist_package = self.create_distribution_package()
        
        # Summary
        print("\n" + "=" * 60)
        print("BUILD SUMMARY")
        print("=" * 60)
        
        if success_methods:
            print("✅ Successful build methods:")
            for method in success_methods:
                print(f"   • {method}")
        else:
            print("❌ No methods succeeded")
        
        print(f"\\n📂 Output directory: {self.dist_dir}")
        print("📁 Files created:")
        
        for file in sorted(self.dist_dir.glob("*")):
            if file.is_file():
                size = file.stat().st_size / (1024 * 1024)  # MB
                print(f"   • {file.name} ({size:.1f} MB)")
            elif file.is_dir():
                print(f"   📁 {file.name}/ (directory)")
        
        print(f"\\n📦 Distribution package: {dist_package}")
        print("\\n🎉 Ready for deployment!")
        
        return len(success_methods) > 0

def main():
    builder = ExecutableBuilder()
    success = builder.build_all()
    
    if success:
        print("\\n🎉 Build completed successfully!")
        print("You can now distribute the files in the 'dist' directory")
    else:
        print("\\n❌ Build failed. Check error messages above.")
        print("Try using the portable version as a fallback.")
    
    input("\\nPress Enter to exit...")

if __name__ == "__main__":
    main()