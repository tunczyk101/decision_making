# -*- mode: python ; coding: utf-8 -*-
from kivymd import hooks_path as kivymd_hooks_path


block_cipher = None


a = Analysis(
    ['customer_main.py'],
    pathex=[],
    binaries=[],
    datas=[('customer.kv', '.'), ('img/*', 'img'), ("customer/kv_customer/*", "customer/kv_customer"), ("example_data/expert_responses/*", "example_data/expert_responses"), ("example_data/questions.json", "example_data")],
    hiddenimports=[],
    hookspath=[kivymd_hooks_path],
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
    [],
    exclude_binaries=True,
    name='customer_main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='customer_main',
)
