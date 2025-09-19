# -*- mode: python ; coding: utf-8 -*-

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
