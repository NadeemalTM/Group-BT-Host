"""
Advanced Executable Builder for Music Host by Nadeemal
Creates standalone .exe files that work without Python installation
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import json

class MusicHostBuilder:
    def __init__(self):
        self.project_dir = Path.cwd()
        self.dist_dir = self.project_dir / "dist"
        self.build_dir = self.project_dir / "build"
        
        # Ensure directories exist
        self.dist_dir.mkdir(exist_ok=True)
        
    def create_requirements_file(self):
        """Create requirements.txt with minimal dependencies."""
        requirements = [
            "# Music Host by Nadeemal - Requirements",
            "# Minimal dependencies for Windows audio and Bluetooth",
            "",
            "# GUI framework (built into Python)",
            "# tkinter - included with Python",
            "",
            "# Audio processing (optional - we use simulation if not available)",
            "# pyaudio>=0.2.11",
            "",
            "# Windows-specific libraries (optional)",
            "# pywin32>=305",
            "",
            "# For building executable",
            "# pyinstaller>=5.0",
        ]
        
        with open(self.project_dir / "requirements.txt", 'w') as f:
            f.write('\n'.join(requirements))
            
        print("✅ Created requirements.txt")
        
    def create_spec_file(self):
        """Create PyInstaller spec file for advanced building."""
        spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Analysis - what files to include
analysis = Analysis(
    ['music_host_main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('README.md', '.'),
        ('LICENSE.txt', '.'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'threading',
        'time',
        'json',
        'subprocess',
        'ctypes',
        'ctypes.wintypes',
        'winreg',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'pygame',
        'cv2',
        'tensorflow',
        'torch',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(analysis.pure, analysis.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    analysis.scripts,
    analysis.binaries,
    analysis.zipfiles,
    analysis.datas,
    [],
    name='MusicHostByNadeemal',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
    version='version_info.txt' if os.path.exists('version_info.txt') else None,
)
'''
        
        spec_file = self.project_dir / "music_host.spec"
        with open(spec_file, 'w') as f:
            f.write(spec_content)
            
        print(f"✅ Created spec file: {spec_file}")
        return spec_file
        
    def create_version_info(self):
        """Create version info file for Windows executable."""
        version_info = '''# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1,0,0,0),
    prodvers=(1,0,0,0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Nadeemal'),
        StringStruct(u'FileDescription', u'Music Host - Universal Audio Streaming'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'MusicHostByNadeemal'),
        StringStruct(u'LegalCopyright', u'© 2024 Nadeemal. All rights reserved.'),
        StringStruct(u'OriginalFilename', u'MusicHostByNadeemal.exe'),
        StringStruct(u'ProductName', u'Music Host by Nadeemal'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
        
        with open(self.project_dir / "version_info.txt", 'w') as f:
            f.write(version_info)
            
        print("✅ Created version info file")
        
    def create_icon(self):
        """Create or copy application icon."""
        assets_dir = self.project_dir / "assets"
        assets_dir.mkdir(exist_ok=True)
        
        icon_path = assets_dir / "icon.ico"
        
        if not icon_path.exists():
            # Create a simple text-based "icon" placeholder
            print("ℹ️  No icon found, executable will use default Windows icon")
            print("   To add custom icon, place icon.ico in assets/ folder")
        else:
            print(f"✅ Using icon: {icon_path}")
            
    def install_pyinstaller(self):
        """Install PyInstaller if not available."""
        try:
            import PyInstaller
            print("✅ PyInstaller already installed")
            return True
        except ImportError:
            print("📦 Installing PyInstaller...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], 
                             check=True, capture_output=True)
                print("✅ PyInstaller installed successfully")
                return True
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install PyInstaller: {e}")
                return False
                
    def build_executable(self):
        """Build the executable using PyInstaller."""
        if not self.install_pyinstaller():
            return False
            
        print("🚀 Building executable...")
        
        # Create spec file
        spec_file = self.create_spec_file()
        
        try:
            # Build using spec file
            cmd = [sys.executable, "-m", "PyInstaller", "--clean", str(spec_file)]
            
            print("Running PyInstaller...")
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_dir)
            
            if result.returncode == 0:
                exe_path = self.dist_dir / "MusicHostByNadeemal.exe"
                if exe_path.exists():
                    file_size = exe_path.stat().st_size / (1024 * 1024)  # MB
                    print(f"✅ Executable created successfully!")
                    print(f"📁 Location: {exe_path}")
                    print(f"📊 Size: {file_size:.1f} MB")
                    return True
                else:
                    print("❌ Executable file not found after build")
                    return False
            else:
                print(f"❌ PyInstaller failed:")
                print(result.stderr)
                return False
                
        except Exception as e:
            print(f"❌ Build failed: {e}")
            return False
            
    def create_installer_script(self):
        """Create NSIS installer script."""
        nsis_script = f'''!define APP_NAME "Music Host by Nadeemal"
!define APP_VERSION "1.0"
!define APP_PUBLISHER "Nadeemal"
!define APP_EXE "MusicHostByNadeemal.exe"

Name "${{APP_NAME}}"
OutFile "MusicHostInstaller.exe"
InstallDir "$PROGRAMFILES\\${{APP_NAME}}"
RequestExecutionLevel admin

Page directory
Page instfiles

Section "Install"
    SetOutPath $INSTDIR
    
    ; Copy main executable
    File "dist\\${{APP_EXE}}"
    
    ; Copy documentation
    File /nonfatal "README.md"
    File /nonfatal "LICENSE.txt"
    
    ; Create shortcuts
    CreateDirectory "$SMPROGRAMS\\${{APP_NAME}}"
    CreateShortCut "$SMPROGRAMS\\${{APP_NAME}}\\${{APP_NAME}}.lnk" "$INSTDIR\\${{APP_EXE}}"
    CreateShortCut "$SMPROGRAMS\\${{APP_NAME}}\\Uninstall.lnk" "$INSTDIR\\Uninstall.exe"
    CreateShortCut "$DESKTOP\\${{APP_NAME}}.lnk" "$INSTDIR\\${{APP_EXE}}"
    
    ; Create uninstaller
    WriteUninstaller "$INSTDIR\\Uninstall.exe"
    
    ; Registry entries
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}" "DisplayName" "${{APP_NAME}}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}" "UninstallString" "$INSTDIR\\Uninstall.exe"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}" "Publisher" "${{APP_PUBLISHER}}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}" "DisplayVersion" "${{APP_VERSION}}"
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\\${{APP_EXE}}"
    Delete "$INSTDIR\\README.md"
    Delete "$INSTDIR\\LICENSE.txt"
    Delete "$INSTDIR\\Uninstall.exe"
    
    Delete "$SMPROGRAMS\\${{APP_NAME}}\\${{APP_NAME}}.lnk"
    Delete "$SMPROGRAMS\\${{APP_NAME}}\\Uninstall.lnk"
    Delete "$DESKTOP\\${{APP_NAME}}.lnk"
    RMDir "$SMPROGRAMS\\${{APP_NAME}}"
    
    DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}"
    
    RMDir "$INSTDIR"
SectionEnd
'''
        
        nsis_file = self.project_dir / "installer.nsi"
        with open(nsis_file, 'w') as f:
            f.write(nsis_script)
            
        print(f"✅ Created NSIS installer script: {nsis_file}")
        print("📝 To create installer:")
        print("   1. Install NSIS from https://nsis.sourceforge.io/")
        print("   2. Right-click installer.nsi → Compile NSIS Script")
        
    def create_portable_package(self):
        """Create portable package."""
        portable_dir = self.dist_dir / "MusicHost_Portable"
        portable_dir.mkdir(exist_ok=True)
        
        # Copy executable if it exists
        exe_file = self.dist_dir / "MusicHostByNadeemal.exe"
        if exe_file.exists():
            shutil.copy2(exe_file, portable_dir)
            
        # Copy source files for backup
        source_files = [
            "music_host_main.py",
            "audio_capture.py", 
            "enhanced_bluetooth.py",
            "README.md"
        ]
        
        for file_name in source_files:
            src_file = self.project_dir / file_name
            if src_file.exists():
                shutil.copy2(src_file, portable_dir)
                
        # Create launcher batch file
        launcher_content = '''@echo off
echo ================================================
echo Music Host by Nadeemal - Portable Version
echo ================================================
echo.

if exist "MusicHostByNadeemal.exe" (
    echo Starting Music Host...
    start "" "MusicHostByNadeemal.exe"
) else (
    echo Executable not found. Checking for Python...
    
    python --version >nul 2>&1
    if not errorlevel 1 (
        echo Running from Python source...
        python music_host_main.py
    ) else (
        echo Error: Neither executable nor Python found.
        echo Please ensure you have either:
        echo 1. The .exe file in this folder, or
        echo 2. Python installed on your system
        pause
    )
)
'''
        
        launcher_file = portable_dir / "Start_MusicHost.bat"
        with open(launcher_file, 'w') as f:
            f.write(launcher_content)
            
        # Create README for portable version
        readme_content = '''# Music Host by Nadeemal - Portable Version

## Quick Start

Double-click `Start_MusicHost.bat` to launch the application.

## What This Does

This application captures any audio playing on your Windows computer and streams it to multiple connected Bluetooth devices simultaneously.

### Features:
- 🎵 Capture audio from any Windows application (YouTube, Spotify, games, etc.)
- 📱 Connect to multiple Bluetooth speakers and headphones at once
- 🔊 Real-time audio streaming with volume control
- 🎯 Easy-to-use graphical interface
- ⚙️ No complex setup required

### How to Use:
1. Start the application
2. Click "Discover Devices" to find Bluetooth audio devices
3. Connect to desired speakers/headphones
4. Click "Start Streaming" 
5. Play music from any app - it will stream to all connected devices!

### Requirements:
- Windows 10/11
- Bluetooth-enabled computer
- Bluetooth audio devices (speakers, headphones, etc.)

### Perfect For:
- House parties with multiple speakers
- Sharing music with friends' headphones
- Creating synchronized audio across rooms
- Group listening experiences

Enjoy sharing your music with everyone!

© 2024 Nadeemal. Universal Audio Streaming Solution.
'''
        
        readme_file = portable_dir / "README.txt"
        with open(readme_file, 'w') as f:
            f.write(readme_content)
            
        print(f"✅ Created portable package: {portable_dir}")
        
    def build_all(self):
        """Build everything."""
        print("🎵 Music Host by Nadeemal - Executable Builder")
        print("=" * 60)
        print("Creating standalone Windows application...")
        print("=" * 60)
        
        # Setup
        self.create_requirements_file()
        self.create_version_info()
        self.create_icon()
        
        # Build executable
        success = self.build_executable()
        
        # Create additional packages
        self.create_installer_script()
        self.create_portable_package()
        
        # Summary
        print("\n" + "=" * 60)
        print("BUILD SUMMARY")
        print("=" * 60)
        
        if success:
            print("✅ Build completed successfully!")
            print(f"📂 Output directory: {self.dist_dir}")
            
            # List created files
            print("📁 Created files:")
            for file in sorted(self.dist_dir.glob("*")):
                if file.is_file():
                    size = file.stat().st_size / (1024 * 1024)  # MB
                    print(f"   • {file.name} ({size:.1f} MB)")
                elif file.is_dir():
                    print(f"   📁 {file.name}/ (directory)")
                    
            print("\n🎉 Ready for distribution!")
            print("\nDistribution options:")
            print("1. 📱 Share MusicHostByNadeemal.exe - Standalone executable")
            print("2. 📦 Use installer.nsi to create professional installer")
            print("3. 🎒 Share MusicHost_Portable/ folder - Complete package")
            
        else:
            print("❌ Build failed. Check error messages above.")
            print("\n🔧 Troubleshooting:")
            print("1. Ensure Python and pip are working")
            print("2. Try installing PyInstaller manually: pip install pyinstaller")
            print("3. Check that all source files are present")
            
        return success


def main():
    """Main entry point."""
    builder = MusicHostBuilder()
    success = builder.build_all()
    
    if success:
        print("\n🎉 Success! Your Music Host application is ready for distribution.")
        print("\nYou can now:")
        print("• Share the .exe file with friends")
        print("• Install on any Windows computer")
        print("• Stream audio to multiple Bluetooth devices")
    else:
        print("\n❌ Build failed. Please check the error messages above.")
        
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()