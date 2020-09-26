# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

import os, sys
root_dir = "C:\\Users\\61980\\Desktop\\aa\\pcr"
sys.path.append(root_dir)

a = Analysis(['C:\\Users\\61980\\Desktop\\aa\\pcr\\FW_PCR\\manage.py'],
             pathex=['C:\\Users\\61980\\Desktop\\aa\\pcr'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='PCR',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon= root_dir + "\\FW_PCR\\resources\\icon\\pcr.ico"
           )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='PCR')
