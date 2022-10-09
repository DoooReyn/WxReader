# -*- coding: utf-8 -*-

"""
@File    : Cmm.py
@Time    : 2022/9/27 17:25
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 通用
"""
import sys
from os import makedirs
from os.path import join
from traceback import format_exc, print_exc

from PyQt5.QtCore import QStandardPaths


class Cmm:
    """通用辅助工具集合"""

    AppName = 'WxReader'
    AppConfig = 'WxReader.json'

    class Decorator:
        """装饰器"""

        """ -------单例 region began -------"""
        @staticmethod
        def Singleton(cls):
            """单例"""
            _instance = {}

            def _singleton(*args, **kargs):
                if cls not in _instance:
                    _instance[cls] = cls(*args, **kargs)
                return _instance[cls]

            return _singleton

        """ ------- 单例 region ended -------"""

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
    def localCacheAt():
        return QStandardPaths.writableLocation(QStandardPaths.AppConfigLocation)

    @staticmethod
    def appStorageAt():
        return join(Cmm.localCacheAt(), Cmm.AppName)

    @staticmethod
    def appConfigAt():
        return join(Cmm.appStorageAt(), Cmm.AppConfig)

    @staticmethod
    def mkdir(directory: str):
        makedirs(directory, exist_ok=True)

    @staticmethod
    def saveAs(where: str, content: str):
        with open(where, 'w', encoding='utf-8') as f:
            f.write(content)
