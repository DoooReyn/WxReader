"""
This is PyInstaller hook file for CEF Python. This file
helps PyInstaller find CEF Python dependencies that are
required to run final executable.

See PyInstaller docs for hooks:
https://pyinstaller.readthedocs.io/en/stable/hooks.html
"""

import glob
import os
import platform
import re
import sys

import PyInstaller
from PyInstaller import log as logging
from PyInstaller.compat import is_win, is_darwin, is_linux
from PyInstaller.utils.hooks import is_module_satisfies, get_package_paths
from pkg_resources import Requirement

try:
    # PyInstaller >= 4.0 doesn't support Python 2.7
    from PyInstaller.compat import is_py2
except ImportError:
    is_py2 = None

# Constants
CEFPYTHON_MIN_VERSION = "57.0"
PYINSTALLER_MIN_VERSION = "3.2.1"
CEFPYTHON3_DIR = get_package_paths("cefpython3")[1]
CYTHON_MODULE_EXT = ".pyd" if is_win else ".so"
CEF_EXTENSIONS = [".exe", ".dll", ".pak", ".dat", ".bin", ".txt", ".so", ".plist"]

# Globals
logger = logging.getLogger(__name__)


# Functions
def check_platforms():
    if not is_win and not is_darwin and not is_linux:
        raise SystemExit("Error: Currently only Windows, Linux and Darwin platforms are supported, see Issue #135.")


def check_pyinstaller_version():
    version = PyInstaller.__version__
    match = re.search(r"^\d+\.\d+(\.\d+)?", version)
    if not (match.group(0) >= PYINSTALLER_MIN_VERSION):
        raise SystemExit(f"Error: pyinstaller {PYINSTALLER_MIN_VERSION} or higher is required")


def check_cefpython3_version():
    if not is_module_satisfies(Requirement(f"cefpython3 >= {CEFPYTHON_MIN_VERSION}")):
        raise SystemExit(f"Error: cefpython3 {CEFPYTHON_MIN_VERSION} or higher is required")


def get_cefpython_modules():
    pyds = glob.glob(os.path.join(CEFPYTHON3_DIR, "cefpython_py*" + CYTHON_MODULE_EXT))
    assert len(pyds) > 1, "Missing cefpython3 Cython modules"
    modules = []
    for path in pyds:
        filename = os.path.basename(path)
        mod = filename.replace(CYTHON_MODULE_EXT, "")
        modules.append(mod)
    return modules


def get_excluded_cefpython_modules():
    pyver = "".join(map(str, sys.version_info[:2]))
    pyver_string = f"py{pyver}"
    modules = get_cefpython_modules()
    excluded = []
    for mod in modules:
        if pyver_string in mod:
            continue
        excluded.append(f"cefpython3.{mod}")
        logger.info(f"Exclude cefpython3 module: {excluded[-1]}")
    return excluded


def get_cefpython3_datas():
    ret = list()

    if is_win:
        cef_data_dir = "."
    elif is_darwin or is_linux:
        cef_data_dir = "."
    else:
        assert False, f"Unsupported system {platform.system()}"

    # Binaries, licenses and readmes in the cefpython3/ directory
    for filename in os.listdir(CEFPYTHON3_DIR):
        # Ignore Cython modules which are already handled by pyinstaller automatically.
        if filename[:-len(CYTHON_MODULE_EXT)] in get_cefpython_modules():
            continue

        # CEF binaries and datas
        extension = os.path.splitext(filename)[1]
        if extension in CEF_EXTENSIONS or filename.lower().startswith("license"):
            logger.info(f"Include cefpython3 data: {filename}")
            ret.append((os.path.join(CEFPYTHON3_DIR, filename), cef_data_dir))

    if is_darwin:
        resources_subdir = os.path.join("Chromium Embedded Framework.framework", "Resources")
        base_path = os.path.join(CEFPYTHON3_DIR, resources_subdir)
        assert os.path.exists(base_path), f"{resources_subdir} dir not found in cefpython3"
        for path, dirs, files in os.walk(base_path):
            for file in files:
                absolute_file_path = os.path.join(path, file)
                dest_path = os.path.relpath(path, CEFPYTHON3_DIR)
                ret.append((absolute_file_path, dest_path))
                logger.info(f"Include cefpython3 data: {dest_path}")
    elif is_win or is_linux:
        # The .pak files in cefpython3/locales/ directory
        locales_dir = os.path.join(CEFPYTHON3_DIR, "locales")
        assert os.path.exists(locales_dir), "locales/ dir not found in cefpython3"
        for filename in os.listdir(locales_dir):
            logger.info(f"Include cefpython3 data: {os.path.basename(locales_dir)}/{filename}")
            ret.append((os.path.join(locales_dir, filename), os.path.join(cef_data_dir, "locales")))

        # Optional .so/.dll files in cefpython3/swiftshader/ directory
        swift_shader_dir = os.path.join(CEFPYTHON3_DIR, "swiftshader")
        if os.path.isdir(swift_shader_dir):
            for filename in os.listdir(swift_shader_dir):
                logger.info(f"Include cefpython3 data: {os.path.basename(swift_shader_dir)}/{filename}")
                ret.append((os.path.join(swift_shader_dir, filename),
                            os.path.join(cef_data_dir, "swiftshader")))
    return ret


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

# Checks
check_platforms()
check_pyinstaller_version()
check_cefpython3_version()

# Info
logger.info(f"CEF Python package directory: {CEFPYTHON3_DIR}")

# Hidden imports.
hidden_imports = [
    "codecs",
    "copy",
    "datetime",
    "inspect",
    "json",
    "os",
    "platform",
    "random",
    "re",
    "sys",
    "time",
    "traceback",
    "types",
    "urllib",
    "weakref",
]
if is_py2:
    hidden_imports += [
        "urlparse",
    ]

# Excluded modules
excluded_imports = get_excluded_cefpython_modules()

# Include binaries requiring to collect its dependencies
if is_darwin or is_linux:
    binaries = [(os.path.join(CEFPYTHON3_DIR, "subprocess"), ".")]
elif is_win:
    binaries = [(os.path.join(CEFPYTHON3_DIR, "subprocess.exe"), ".")]
else:
    binaries = []

# Include datas
datas = get_cefpython3_datas()

# Notify pyinstaller.spec code that this hook was executed
# and that it succeeded.
os.environ["PYINSTALLER_CEFPYTHON3_HOOK_SUCCEEDED"] = "1"
