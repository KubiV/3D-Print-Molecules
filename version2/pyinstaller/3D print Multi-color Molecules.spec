# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['../src/main.py'],
    pathex=[],
    binaries=[],
    datas=[('Settings.json', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PyQt6'],
    noarchive=True,
    optimize=2,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [('O', None, 'OPTION'), ('O', None, 'OPTION'), ('v', None, 'OPTION')],
    exclude_binaries=True,
    name='3D print Multi-color Molecules',
    debug=True,
    bootloader_ignore_signals=False,
    strip=True,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['../../graphical/default_icon.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=True,
    upx=False,
    upx_exclude=[],
    name='3D print Multi-color Molecules',
)
app = BUNDLE(
    coll,
    name='3D print Multi-color Molecules.app',
    icon='../../graphical/default_icon.icns',
    bundle_identifier=None,
)
