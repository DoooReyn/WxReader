# -*- mode: python -*-
# -*- coding: utf-8 -*-

"""
This is a PyInstaller spec file.
"""

import os

from PyInstaller.building.api import PYZ, EXE, COLLECT
from PyInstaller.building.build_main import Analysis


def getEnv(key, default):
    return os.environ.get(key, default)


# Constants
APP_NAME = "#{app_name}"
APP_ENTRY = "#{app_entry}"
APP_DIR = "#{app_dir}"
APP_ICON = "#{app_icon}"
HOOKS_PATH = "."
BLOCK_CIPHER = None
IS_DEBUG = getEnv("CEFPYTHON_PYINSTALLER_DEBUG", False)
USE_UPX = getEnv("CEFPYTHON_PYINSTALLER_UPX", False)

# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

a = Analysis(
    [APP_ENTRY],
    pathex=[APP_DIR],
    hookspath=[HOOKS_PATH],
    cipher=BLOCK_CIPHER,
    win_private_assemblies=True,
    win_no_prefer_redirects=True,
)

if not getEnv("PYINSTALLER_CEFPYTHON3_HOOK_SUCCEEDED", None):
    raise SystemExit("Error: Pyinstaller hook-cefpython3.py script was not executed or it failed")

pyz = PYZ(a.pure,
          a.zipped_data,
          cipher=BLOCK_CIPHER)

exe = EXE(pyz,
          a.scripts,
          [('v', None, 'OPTION')],
          exclude_binaries=True,
          strip=False,
          name=APP_NAME,
          debug=IS_DEBUG,
          upx=USE_UPX,
          console=IS_DEBUG,
          icon=[APP_ICON])

COLLECT(exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=False,
        upx=USE_UPX,
        name=APP_NAME)
