# -*- coding: utf-8 -*-

"""
@File    : ApplicationController.py
@Time    : 2022/10/7 15:13
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 应用页面
"""
import sys
from traceback import format_exception

from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import QApplication

from conf.Lang import LanguageKeys
from conf.ResMap import ResMap
from conf.Resources import qInitResources
from helper.GUI import GUI
from helper.I18n import I18n
from helper.Preferences import Preferences
from helper.Signals import Signals
from ui.view.WindowView import WindowView


class ErrorHookProxy:
    """全局异常捕获代理"""

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


class ApplicationView(ErrorHookProxy):
    """应用程序控制器"""

    def __init__(self):
        super(ApplicationView, self).__init__()

        # 尝试修复 QWebEngine WebGL 的问题
        QCoreApplication.setAttribute(Qt.AA_UseDesktopOpenGL)

        # 初始化 qrc 资源
        qInitResources()

        # 初始化用户配置
        Preferences().init()

        # 创建 Qt 窗口
        self.app = QApplication(sys.argv)

        # 使用高清 icon
        self.app.setAttribute(Qt.AA_UseHighDpiPixmaps)
        self.app.setWindowIcon(GUI.icon(ResMap.icon_app))

        # 设置应用名称
        self.app.setApplicationName(I18n.text(LanguageKeys.app_name))
        self.app.setApplicationDisplayName(I18n.text(LanguageKeys.app_name))

        # 设置主题
        self.app.setStyleSheet(GUI.Theme.Default)

        # 创建应用窗口
        self.win = WindowView()
        self.win.show()

        # 运行应用
        sys.exit(self.app.exec_())
