# -*- coding: utf-8 -*-

"""
@File    : ApplicationCtroller.py
@Time    : 2022/10/7 15:13
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : PyCharm
"""
import sys
from traceback import format_exception

from conf.resources import qInitResources
from helper.preferences import Preferences
from helper.signals import Signals
from ui.controller.Controller import Controller
from ui.view.ApplicationView import ApplicationView


class ErrorHookProxy:
    # 异常捕获备份
    ERROR_HOOK_BAK = sys.excepthook

    def __init__(self):
        sys.excepthook = self.onErrorOccurs

    @staticmethod
    def onErrorOccurs(error_type, error_target, error_stack):
        """全局异常捕获"""
        traceback_format = format_exception(error_type, error_target, error_stack)
        traceback_msg = "".join(traceback_format)
        Signals().logger_error.emit(traceback_msg)
        ErrorHookProxy.ERROR_HOOK_BAK(error_type, error_target, error_stack)


class ApplicationController(Controller, ErrorHookProxy):
    """应用程序控制器"""

    def __init__(self):
        super(ApplicationController, self).__init__()
        # 初始化 qrc 资源
        qInitResources()

        # 初始化用户配置
        Preferences().init()

        # 创建应用视图
        self._view = ApplicationView()

        # 启动应用
        self._view.run()
