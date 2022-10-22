# -*- coding: utf-8 -*-

"""
@File    : GUI.py
@Time    : 2022/9/27 17:21
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : GUI辅助工具
"""

from PySide6.QtCore import QSize
from PySide6.QtGui import QColor, QFont, QIcon
from PySide6.QtWidgets import QWidget


class GUI:
    """GUI辅助工具"""

    class Preferences:
        """默认值"""
        font_size = 14
        font_name = "微软雅黑"
        layout_spacing = 8
        line_height = 36
        view_size = QSize(640, 480)

    class GridItem:
        """网格子项"""

        def __init__(self, widget: QWidget, col_start: int, col_span: int):
            self.widget = widget
            self.col_start = col_start
            self.col_span = col_span

    @staticmethod
    def viewSize():
        """默认视图尺寸"""
        return GUI.Preferences.view_size

    @staticmethod
    def font():
        """默认字体"""
        font = QFont()
        font.setPointSize(GUI.Preferences.font_size)
        font.setFamily(GUI.Preferences.font_name)
        return font

    @staticmethod
    def icon(path: str):
        """创建图标"""
        return QIcon(path)

    @staticmethod
    def color(color: str):
        """创建色值"""
        return QColor(color)
