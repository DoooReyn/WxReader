"""
This is an example of using PyInstaller packager to build
executable from one of CEF Python's examples (wxpython.py).

See README-pyinstaller.md for installing required packages.

To package example type: `python pyinstaller.py`.
"""

import os
import platform
import shutil
import sys
from subprocess import Popen

try:
    import PyInstaller
except ImportError:
    PyInstaller = None
    raise SystemExit("Error: PyInstaller package missing. "
                     "To install type: pip install --upgrade pyinstaller")

EXE_EXT = ""
if platform.system() == "Windows":
    EXE_EXT = ".exe"
elif platform.system() == "Darwin":
    EXE_EXT = ".app"
elif platform.system() == "Linux":
    EXE_EXT = ""

NAME = "WxReader"

Redundancies = [
    "devtools_resources.pak",
    "PySide6/Qt6Qml.dll",
    "PySide6/Qt6QmlModels.dll",
    "PySide6/Qt6Quick.dll",
    "cefpython3/chrome_elf.dll",
    "cefpython3/libcef.dll",
    "cefpython3/msvcp90.dll",
    "cefpython3/msvcp100.dll",
    "cefpython3/msvcp140.dll",
    "PySide6/translations",
    "locales"
]

LocaleReserve = 'zh-CN.pak'


def main():
    # Platforms supported
    if platform.system() not in ["Windows", "Darwin", "Linux"]:
        raise SystemExit("Error: Only Windows, Linux and Darwin platforms are "
                         "currently supported. See Issue #135 for details.")

    # Make sure nothing is cached from previous build.
    # Delete the build/ and dist/ directories.
    if os.path.exists("build/"):
        shutil.rmtree("build/")
    if os.path.exists("dist/"):
        shutil.rmtree("dist/")

    # Execute pyinstaller.
    # Note: the "--clean" flag passed to PyInstaller will delete
    #       global global cache and temporary files from previous
    #       runs. For example on Windows this will delete the
    #       "%appdata%/roaming/pyinstaller/bincache00_py27_32bit"
    #       directory.
    env = os.environ
    if "--debug" in sys.argv:
        env["CEFPYTHON_PYINSTALLER_DEBUG"] = "1"
    if "--upx" in sys.argv:
        env["CEFPYTHON_PYINSTALLER_UPX"] = "1"
    sub = Popen(["pyinstaller", "--clean", "pyinstaller.spec"], env=env)
    sub.communicate()
    rcode = sub.returncode
    if rcode != 0:
        print("Error: PyInstaller failed, code=%s" % rcode)
        # Delete distribution directory if created
        if os.path.exists("dist/"):
            shutil.rmtree("dist/")
        sys.exit(1)

    # Make sure everything went fine
    curdir = os.path.dirname(os.path.abspath(__file__))
    cefapp_dir = os.path.join(curdir, "dist", NAME)
    executable = os.path.join(cefapp_dir, NAME + EXE_EXT)
    if not os.path.exists(executable):
        print("Error: PyInstaller failed, main executable is missing: %s"
              % executable)
        sys.exit(1)

    # Done
    print("OK. Created dist/ directory.")

    # 删除冗余
    for entry in Redundancies:
        filepath = os.path.join(cefapp_dir, entry)
        if os.path.isfile(filepath):
            os.remove(filepath)
        elif os.path.isdir(filepath):
            for sub_entry in os.listdir(filepath):
                if sub_entry != LocaleReserve:
                    os.remove(os.path.join(filepath, sub_entry))

    # On Windows open folder in explorer or when --debug is passed
    # run the result binary using "cmd.exe /k cefapp.exe", so that
    # console window doesn't close.
    if platform.system() == "Windows":
        if "--debug" in sys.argv:
            os.system("start cmd /k \"%s\"" % executable)
        else:
            # SYSTEMROOT = C:/Windows
            os.system("%s/explorer.exe /n,/e,%s" % (
                os.environ["SYSTEMROOT"], cefapp_dir))


if __name__ == "__main__":
    main()
