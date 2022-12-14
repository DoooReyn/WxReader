from json import dumps

from PyInstaller import log
from os import environ


class Cache:
    """缓存"""
    def __init__(self):
        self.debug = False
        self.upx = False
        self.production_version = "1.0.0.0"
        self.display_version = "1.0.0"
        self.disable_cache = False
        self.manifest = {}
        self.env = environ

    def setVersion(self, version: [str]):
        """设置版本号"""
        self.display_version = '.'.join(version[:3])
        self.production_version = '.'.join(version)

    def setDebug(self, debug: bool):
        """设置调试模式"""
        self.debug = debug
        if debug:
            self.setEnv('CEFPYTHON_PYINSTALLER_DEBUG', '1')

    def setUpx(self, upx: bool):
        """设置是否使用upx压缩"""
        self.upx = upx
        if upx:
            self.setEnv('CEFPYTHON_PYINSTALLER_UPX', '1')

    def setDisableCache(self, disable):
        """设置是否禁用缓存"""
        self.disable_cache = disable

    def setManifest(self, manifest):
        """设置项目配置"""
        self.manifest = manifest

    def saveManifest(self):
        """保存项目配置"""
        self.manifest['display_version'] = self.display_version
        self.manifest['production_version'] = self.production_version
        with open('./package.json', 'w', encoding='utf-8') as f:
            f.write(dumps(self.manifest, ensure_ascii=False, indent=4))

    @staticmethod
    def getEnv(key, default=None):
        """获取环境变量"""
        return environ.get(key, default)

    @staticmethod
    def setEnv(key, value):
        """设置环境变量"""
        environ[key] = value


cache = Cache()
logger = log.getLogger('Bundle')
