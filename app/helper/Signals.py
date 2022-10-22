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

    # 窗口
    win_closed = Signal(int)

    # 多语言
    lang_changed = Signal(str)

    # 阅读器
    reader_status_tip_updated = Signal(str)
    reader_refresh_speed = Signal()
    reader_reading_finished = Signal()

    # API
    finished_api_done = Signal(bool)

    # Cef Browser
    cef_update_state = Signal()
    cef_load_start = Signal()
    cef_load_finished = Signal()
    cef_short_cut = Signal(int)


gSignals = Signals()
