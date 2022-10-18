# -*- coding: utf-8 -*-

"""
@File    : ApplicationController.py
@Time    : 2022/10/7 15:13
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 应用页面
"""

import sys
from traceback import format_exception

from PySide6.QtCore import QCoreApplication, Qt, QObject
from PySide6.QtWidgets import QApplication

from conf.Lang import LanguageKeys
from conf.ResMap import ResMap
from conf.Resources import qInitResources
from helper.GUI import GUI
from helper.I18n import I18n
from helper.Preferences import Preferences
from helper.Signals import Signals
from ui.view.WindowView import WindowView


def applyCustomExceptionProxy():
    _old_hook = sys.excepthook

    def customExceptionHook(error_type, error_target, error_stack):
        """自定义全局异常捕获"""
        traceback_format = format_exception(error_type, error_target, error_stack)
        traceback_msg = "".join(traceback_format)
        Signals().logger_error.emit(traceback_msg)
        _old_hook(error_type, error_target, error_stack)

    sys.excepthook = customExceptionHook


class Application(QObject):
    """应用程序入口"""

    def __init__(self):
        super().__init__()

        # 设置异常代理
        applyCustomExceptionProxy()

        # 初始化资源
        qInitResources()

        # 初始化用户配置
        Preferences().init()

        # 设置应用基础属性

        QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_UseOpenGLES)
        QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)

        # 创建应用
        self.app = QApplication(sys.argv)
        self.app.setStyleSheet(GUI.Theme.Default)
        self.app.setWindowIcon(GUI.icon(ResMap.icon_app))
        self.app.setApplicationName(I18n.text(LanguageKeys.app_name))
        self.app.setApplicationDisplayName(I18n.text(LanguageKeys.app_name))

        # 创建应用主窗口
        self.win = WindowView()

    def run(self):
        self.win.show()
        sys.exit(self.app.exec())


if __name__ == "__main__":
    Application().run()
