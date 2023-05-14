# -*- coding: utf-8 -*-

"""
@File    : ApplicationController.py
@Time    : 2022/10/7 15:13
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 应用页面
"""

import sys
from os.path import join

from PySide6.QtCore import QLocale
from PySide6.QtWidgets import QApplication
from cefpython3 import cefpython as cef

from conf.Config import Config
from conf.Lang import LanguageKeys
from conf.ResMap import ResMap
from conf.Resources import qInitResources
from helper.Cmm import Cmm
from helper.GUI import GUI
from helper.I18n import I18n
from helper.Preferences import gPreferences
from ui.view.WindowView import WindowView


def applyCustomExceptionProxy():
    """使用自定义全局异常捕获"""
    # 这里直接用 CEF 的就好
    sys.excepthook = cef.ExceptHook


def main():
    # 调试模式?
    Config.DEBUG = '--DEBUG' in sys.argv

    # 设置异常代理
    applyCustomExceptionProxy()

    # 初始化资源
    qInitResources()

    # 设置语言
    QLocale.setDefault(QLocale(QLocale.Language.Chinese, QLocale.Country.China))

    # 初始化用户配置
    gPreferences.init()

    # 初始化 cef
    cef_module_at = cef.GetModuleDirectory()
    cef_settings = {
        "debug": Config.DEBUG,
        "locale": join(cef_module_at, Config.LocaleAt),
        "log_file": Cmm.appStorageAt(),
        "cache_path": Cmm.appStorageAt(),
        "context_menu": {"enabled": False},
    }
    cef_switches = {
        "disable-gpu": "",
        "disable-gpu-compositing": "",
    }
    cef.Initialize(settings=cef_settings, switches=cef_switches)

    # 创建应用
    app = QApplication(sys.argv)
    app.setStyleSheet(Cmm.readFile(ResMap.theme_default))
    app.setWindowIcon(GUI.icon(ResMap.icon_app))
    app.setApplicationName(Config.AppName)
    app.setApplicationDisplayName(I18n.text(LanguageKeys.app_name))

    # 创建应用主窗口
    win = WindowView()
    win.show()
    win.activateWindow()
    win.raise_()
    app.exec()

    # 释放 CEF
    del win
    del app
    cef.Shutdown()
    sys.exit(0)


if __name__ == "__main__":
    main()
