# -*- coding: utf-8 -*-

"""
@File    : Signals.py
@Time    : 2022/9/27 16:59
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 基础信号源
"""
from PySide6.QtCore import Signal, QObject

from helper.Cmm import Cmm


@Cmm.Decorator.Singleton
class Signals(QObject):
    """Qt信号"""

    # 日志
    logger_trace = Signal(str)
    logger_debug = Signal(str)
    logger_info = Signal(str)
    logger_warn = Signal(str)
    logger_error = Signal(str)
    logger_fatal = Signal(str)

    # 窗口
    win_closed = Signal(int)
    win_focus_main = Signal()

    # 多语言
    lang_changed = Signal(str)

    # 阅读器
    reader_setting_changed = Signal(int)
    reader_load_progress = Signal(int)
    reader_status_tip_updated = Signal(str)
    reader_download_note = Signal(str, str)
    reader_refresh_speed = Signal()
    reader_reading_finished = Signal()

    # API
    finished_api_done = Signal(bool)
