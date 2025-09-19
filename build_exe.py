"""
Build Script for Creating Executable
Uses PyInstaller to create a standalone Windows executable
"""

import os
import sys
import subprocess
import shutil

def check_pyinstaller():
    """Check if PyInstaller is installed and install if needed."""
    try:
        import PyInstaller
        print("✓ PyInstaller is already installed")
        return True
    except ImportError:
        print("Installing PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✓ PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("✗ Failed to install PyInstaller")
            return False

def create_spec_file():
    """Create a PyInstaller spec file for better control."""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('README.md', '.'),
        ('SETUP_GUIDE.md', '.'),
        ('PROJECT_SUMMARY.md', '.'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'threading',
        'subprocess',
        'time',
        'os',
        'sys',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='BluetoothMusicPlayer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
'''
    
    with open('bluetooth_music_player.spec', 'w') as f:
        f.write(spec_content)
    
    print("✓ Created PyInstaller spec file")

def build_executable():
    """Build the executable using PyInstaller."""
    print("Building executable...")
    print("This may take several minutes...")
    
    try:
        # Build using spec file for better control
        cmd = [sys.executable, "-m", "PyInstaller", "--clean", "bluetooth_music_player.spec"]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Executable built successfully!")
            return True
        else:
            print("✗ Build failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"✗ Build error: {e}")
        return False

def create_simple_executable():
    """Create executable with simpler approach."""
    print("Trying simplified build...")
    
    try:
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--name=BluetoothMusicPlayer",
            "--add-data=README.md;.",
            "--add-data=demo.py;.",
            "main.py"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Simple executable built successfully!")
            return True
        else:
            print("✗ Simple build failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"✗ Simple build error: {e}")
        return False

def create_demo_executable():
    """Create executable for demo version (more likely to work)."""
    print("Building demo executable...")
    
    try:
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--name=BluetoothMusicPlayerDemo",
            "demo.py"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Demo executable built successfully!")
            return True
        else:
            print("✗ Demo build failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"✗ Demo build error: {e}")
        return False

def create_installer():
    """Create an installer using Inno Setup script."""
    inno_script = '''[Setup]
AppName=Bluetooth Multi-Device Music Player
AppVersion=1.0
DefaultDirName={autopf}\\BluetoothMusicPlayer
DefaultGroupName=Bluetooth Music Player
OutputDir=installer
OutputBaseFilename=BluetoothMusicPlayerSetup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\\BluetoothMusicPlayer.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "SETUP_GUIDE.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "PROJECT_SUMMARY.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\\Bluetooth Music Player"; Filename: "{app}\\BluetoothMusicPlayer.exe"
Name: "{group}\\{cm:UninstallProgram,Bluetooth Music Player}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\\Bluetooth Music Player"; Filename: "{app}\\BluetoothMusicPlayer.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\\BluetoothMusicPlayer.exe"; Description: "{cm:LaunchProgram,Bluetooth Music Player}"; Flags: nowait postinstall skipifsilent
'''
    
    with open('installer_script.iss', 'w') as f:
        f.write(inno_script)
    
    print("✓ Created Inno Setup installer script")
    print("To create installer:")
    print("1. Install Inno Setup from https://jrsoftware.org/isinfo.php")
    print("2. Open installer_script.iss in Inno Setup")
    print("3. Click Build -> Compile to create the installer")

def cleanup_build_files():
    """Clean up temporary build files."""
    dirs_to_remove = ['build', '__pycache__']
    files_to_remove = ['bluetooth_music_player.spec']
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✓ Removed {dir_name}")
    
    for file_name in files_to_remove:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"✓ Removed {file_name}")

def main():
    """Main build process."""
    print("=" * 60)
    print("Bluetooth Music Player - Executable Builder")
    print("=" * 60)
    
    # Check and install PyInstaller
    if not check_pyinstaller():
        print("Cannot proceed without PyInstaller")
        return False
    
    # Create output directory
    os.makedirs('dist', exist_ok=True)
    
    success = False
    
    # Try different build approaches
    print("\\n1. Trying demo executable (most likely to succeed)...")
    if create_demo_executable():
        success = True
    
    print("\\n2. Trying simple main executable...")
    if create_simple_executable():
        success = True
    
    if not success:
        print("\\n3. Trying advanced build with spec file...")
        create_spec_file()
        if build_executable():
            success = True
    
    # Create installer script
    print("\\n4. Creating installer script...")
    create_installer()
    
    # Results
    print("\\n" + "=" * 60)
    print("Build Results:")
    print("=" * 60)
    
    if os.path.exists('dist/BluetoothMusicPlayerDemo.exe'):
        print("✓ Demo executable: dist/BluetoothMusicPlayerDemo.exe")
    
    if os.path.exists('dist/BluetoothMusicPlayer.exe'):
        print("✓ Main executable: dist/BluetoothMusicPlayer.exe")
    
    if os.path.exists('installer_script.iss'):
        print("✓ Installer script: installer_script.iss")
    
    print("\\nNext Steps:")
    print("1. Test the executable(s) in the 'dist' folder")
    print("2. If you want an installer, install Inno Setup and compile installer_script.iss")
    print("3. The demo version is more likely to work on systems without Python")
    
    # Ask about cleanup
    cleanup = input("\\nClean up build files? (y/n): ").lower().strip()
    if cleanup == 'y':
        cleanup_build_files()
    
    return success

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\\nBuild cancelled by user")
    except Exception as e:
        print(f"\\nBuild failed: {e}")