# -*- coding: utf-8 -*-

"""
@File    : Cmm.py
@Time    : 2022/9/27 17:25
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 通用
"""
import platform
from os import makedirs
from os.path import join
from traceback import format_exc, print_exc

from PySide6.QtCore import QStandardPaths, QFile, QIODevice, QUrl, QCoreApplication
from PySide6.QtMultimedia import QSoundEffect

from conf.Config import Config
from conf.Sound import WindowsSounds


class Cmm:
    """通用辅助工具集合"""

    class Decorator:
        """装饰器"""

        @staticmethod
        def Singleton(cls):
            """单例"""
            _instance = {}

            def _singleton(*args, **kargs):
                if cls not in _instance:
                    _instance[cls] = cls(*args, **kargs)
                return _instance[cls]

            return _singleton

    # noinspection PyBroadException
    @staticmethod
    def trace(on_start, on_error=None, on_final=None):
        """跟踪运行，自动捕获错误"""
        try:
            return on_start()
        except Exception:
            print_exc()
            if on_error:
                return on_error(format_exc())
        finally:
            if on_final:
                return on_final()

    @staticmethod
    def app():
        return QCoreApplication.instance()

    @staticmethod
    def localCacheAt():
        """本地缓存路径"""
        return QStandardPaths.writableLocation(QStandardPaths.GenericConfigLocation)

    @staticmethod
    def appStorageAt():
        """应用缓存路径"""
        return join(Cmm.localCacheAt(), Config.AppName)

    @staticmethod
    def appConfigAt():
        """应用配置路径"""
        return join(Cmm.appStorageAt(), Config.AppConfig)

    @staticmethod
    def mkdir(directory: str):
        """创建目录"""
        makedirs(directory, exist_ok=True)

    @staticmethod
    def saveAs(where: str, content: str):
        """另存为"""
        with open(where, 'w', encoding='utf-8') as f:
            f.write(content)

    @staticmethod
    def isWindows():
        """是否Windows系统"""
        return platform.system() == 'Windows'

    @staticmethod
    def isWindows10():
        """是否Windows10系统"""
        return Cmm.isWindows() and platform.release() == '10'

    @staticmethod
    def readFile(filepath: str):
        """读取文件内容"""
        js = QFile(filepath)
        if js.open(QIODevice.ReadOnly) is True:
            source = js.readAll().data().decode('utf-8')
            return source
        return None

    @staticmethod
    def playSound(sound_type: WindowsSounds):
        """播放音乐"""
        if Cmm.isWindows():
            sound_path = Config.MediaAt.format(sound_type.value)
            effect = QSoundEffect(Cmm.app())
            effect.setSource(QUrl.fromLocalFile(sound_path))
            effect.setVolume(1.0)
            effect.play()

    @staticmethod
    def playBeep():
        Cmm.playSound(WindowsSounds.Unlock)