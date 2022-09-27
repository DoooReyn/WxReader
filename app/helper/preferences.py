# -*- coding: utf-8 -*-

"""
@File    : preferences.py
@Time    : 2022/9/27 15:46
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 软件配置
"""
from os import makedirs
from os.path import join

from PyQt5.QtCore import QSettings, QStandardPaths


class Preferences:
    storage: QSettings = None

    class Path:
        AppName = 'WxReader'
        ConfigName = 'config.ini'

    @staticmethod
    def app_storage_at():
        return join(QStandardPaths.writableLocation(QStandardPaths.AppConfigLocation), Preferences.Path.AppName)

    @staticmethod
    def init():
        app_dir = Preferences.app_storage_at()
        makedirs(app_dir, exist_ok=True)
        config_path = join(app_dir, Preferences.Path.ConfigName)
        Preferences.storage = QSettings(config_path, QSettings.IniFormat)
