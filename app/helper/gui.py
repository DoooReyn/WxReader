# -*- coding: utf-8 -*-

"""
@File    : gui.py
@Time    : 2022/9/27 17:21
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : GUI辅助工具
"""
from typing import Union

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QColor, QFont, QIcon
from PyQt5.QtWidgets import QAction, QMenu, QToolBar, QWidget

from conf.menus import ActionInfo
from helper.i18n import I18n
from helper.preferences import Preferences
from helper.signals import Signals


class GUI:
    """GUI辅助工具"""

    class Preferences:
        layout_spacing = 8
        line_height = 36
        font_size = 11
        font_name = 'Microsoft YaHei'
        view_size = QSize(640, 480)

    class GridItem:
        def __init__(self, widget: QWidget, col_start: int, col_span: int):
            self.widget = widget
            self.col_start = col_start
            self.col_span = col_span

    class View(QWidget):
        window_code: int = 0
        rect_key: str = None

        def closeEvent(self, event):
            if self.rect_key is not None:
                self.save_win_rect()
            if self.window_code > 0:
                Signals().win_closed.emit(self.window_code)
            event.accept()
            super().closeEvent(event)

        def set_window_code(self, code: int):
            self.window_code = code

        def set_rect_key(self, kr: str):
            self.rect_key = kr
            tx, ty, w, h = self.get_win_rect()
            self.setGeometry(tx, ty, w, h)

        def get_win_rect(self):
            if self.rect_key is not None:
                return [int(v) for v in Preferences.storage.value(self.rect_key, '640,640,640,480', str).split(',')]
            else:
                r = self.geometry()
                return r.topLeft().x(), r.topLeft().y(), r.width(), r.height()

        def save_win_rect(self):
            if self.rect_key is not None:
                r = self.geometry()
                rect = [r.topLeft().x(), r.topLeft().y(), r.width(), r.height()]
                rect = ','.join([str(r) for r in rect])
                Preferences.storage.setValue(self.rect_key, rect)

        @staticmethod
        def menu_method_not_implemented(menu, name):
            msg = I18n.text("debug:method_not_implemented").format(menu, name)
            Signals().logger_warn.emit(msg)
            print(msg)

        def add_action(self, act_info: ActionInfo, parent: Union[QMenu, QToolBar]):
            name = I18n.text(act_info.name)
            act = QAction(name, parent)
            if act_info.icon:
                act.setIcon(GUI.icon(act_info.icon))
            if act_info.shortcut is not None:
                act.setShortcut(act_info.shortcut)
            if act_info.trigger is not None and hasattr(self, act_info.trigger):
                # noinspection PyUnresolvedReferences
                act.triggered.connect(lambda *args, t=self, g=act_info.trigger: getattr(t, g)())
            else:
                # noinspection PyUnresolvedReferences
                act.triggered.connect(lambda *args, m=parent.objectName(), n=name: self.menu_method_not_implemented(m, n))
            parent.addAction(act)
            return act

    @staticmethod
    def view_size():
        return GUI.Preferences.view_size

    @staticmethod
    def font():
        font = QFont()
        font.setPointSize(GUI.Preferences.font_size)
        font.setFamily(GUI.Preferences.font_name)
        return font

    @staticmethod
    def icon(path: str):
        return QIcon(path)

    @staticmethod
    def color(color: str):
        return QColor(color)
