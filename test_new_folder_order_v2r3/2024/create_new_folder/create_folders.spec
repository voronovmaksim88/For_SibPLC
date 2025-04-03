# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['new_folder_order_v2.py'],  # Укажите имя вашего основного скрипта
    pathex=[],
    binaries=[],
    datas=[
        ('ТЗ.odt', '.'),  # Добавляем шаблон ТЗ
        ('КП.xls', '.'),  # Добавляем шаблон КП
    ],
    hiddenimports=[
        'mysql.connector',
        'mysql.connector.locales',
        'mysql.connector.locales.eng',
        'colorama',
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
    name='create_folders',  # Имя выходного exe-файла
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