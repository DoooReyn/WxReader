# -*- coding: utf-8 -*-

"""
@File    : ApplicationView.py
@Time    : 2022/10/7 15:11
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : PyCharm
"""
import sys

from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import QApplication

from conf.res_map import ResMap
from conf.lang import LanguageKeys
from helper.gui import GUI
from helper.i18n import I18n
from view.window import Window


class ApplicationView(object):
    def __init__(self):
        # 尝试修复 QWebEngine WebGL 的问题
        QCoreApplication.setAttribute(Qt.AA_UseDesktopOpenGL)

        # 创建 Qt 窗口
        self.app = QApplication(sys.argv)

        # 使用高清 icon
        self.app.setAttribute(Qt.AA_UseHighDpiPixmaps)
        self.app.setApplicationName(I18n.text(LanguageKeys.app_name))
        self.app.setApplicationDisplayName(I18n.text(LanguageKeys.app_name))
        self.app.setStyleSheet(GUI.Theme.Default)
        self.app.setWindowIcon(GUI.icon(ResMap.icon_app))
        self.win = Window()

    def run(self):
        self.win.show()
        sys.exit(self.app.exec_())
