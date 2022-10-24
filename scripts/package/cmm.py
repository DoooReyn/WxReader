from PyInstaller import log
from os import environ


class Cache:
    def __init__(self):
        self.debug = False
        self.upx = False
        self.production_version = "1.0.0.0"
        self.display_version = "1.0.0"
        self.manifest = {}
        self.env = environ

    def setVersion(self, version: [str]):
        self.display_version = '.'.join(version[:3])
        self.production_version = '.'.join(version)

    def setDebug(self, debug: bool):
        self.debug = debug
        self.setEnv('CEFPYTHON_PYINSTALLER_DEBUG', '1')

    def setUpx(self, upx: bool):
        self.upx = upx
        self.setEnv('CEFPYTHON_PYINSTALLER_UPX', '1')

    def setManifest(self, manifest):
        self.manifest = manifest

    @staticmethod
    def getEnv(key, default=None):
        return environ.get(key, default)

    @staticmethod
    def setEnv(key, value):
        environ[key] = value


cache = Cache()

logger = log.getLogger('Bundle')
