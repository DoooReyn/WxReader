# -*- coding: utf-8 -*-

"""
@File    : cmm.py
@Time    : 2022/9/27 17:25
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 通用
"""
from traceback import format_exc, print_exc


class Cmm:
    """通用辅助工具集合"""

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
