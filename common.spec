# -*- mode: python ; coding: utf-8 -*-
from kivymd import hooks_path as kivymd_hooks_path


block_cipher = None


customer_a = Analysis(
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
expert_a = Analysis(
    ['expert_main.py'],
    pathex=[],
    binaries=[],
    datas=[('expert.kv', '.'), ('img/*', 'img'), ("expert/kv_expert/*", "expert/kv_expert"), ("example_data/expert_responses/*", "example_data/expert_responses"), ("example_data/questions.json", "example_data")],
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
MERGE((customer_a, "customer_main", "customer_main"), (expert_a, "expert_main", "expert_main"))

customer_pyz = PYZ(customer_a.pure, customer_a.zipped_data, cipher=block_cipher)

customer_exe = EXE(
    customer_pyz,
    customer_a.scripts,
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
expert_pyz = PYZ(expert_a.pure, expert_a.zipped_data, cipher=block_cipher)

expert_exe = EXE(
    expert_pyz,
    expert_a.scripts,
    [],
    exclude_binaries=True,
    name='expert_main',
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
    customer_exe,
    customer_a.binaries,
    customer_a.zipfiles,
    customer_a.datas,
    expert_exe,
    expert_a.binaries,
    expert_a.zipfiles,
    expert_a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='decision_making',
)
