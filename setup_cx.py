
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
