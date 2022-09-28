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
        """默认值"""
        layout_spacing = 8
        line_height = 36
        font_size = 14
        font_name = '微软雅黑'
        view_size = QSize(640, 480)

    class Theme:
        """主题"""
        Default = """
            QWidget 
            {
                font-family: "微软雅黑"; 
                font-size: 13px;
            }
            
            QMenuBar 
            {
                border: none;
                background: #ffffff;
                spacing: 2px;
            }
            
            QToolBar 
            {
                border: none;
                background: #ffffff;
                spacing: 2px;
            }
            
            QPushButton 
            {
                border: 2px solid #34a7ff;
                border-radius: 10px;
                background: #f4f8f8;
                font: 15px;
            }
            
            QPushButton::hover,pressed
            {
                font: bold;
                background: #f4f8f8;
            }
            
            QPushButton::pressed
            {
                font: bold;
                margin: 1px 4px 0 4px;
                background: #f4f8f8;
            }
            
            QToolButton::hover,pressed {
                border: 1px solid #8f8f8f;
                border-radius: 10px;
                background-color: #f1f1f1;
                font: bold;
            }

            QToolButton::checked {
                border: 1px solid #8f8f8f;
                border-radius: 10px;
                background-color: #f1f1f1;
            }

            QTextBrowser 
            { 
                border: none; 
                border-radius: 4px; 
                background-color: #fbfbfb; 
            }

            QScrollBar:vertical
            {
                background-color: #f1f1f1;
                width: 8px;
                margin: 0px 0px 0px 0px;
                border: 1px transparent #2A2929;
            }
        
            QScrollBar::handle:vertical
            {
                background-color: #c1c1c1;
                min-height: 5px;
                border-radius: 4px;
            }
        
            QScrollBar::sub-line:vertical
            {
                margin: 3px 0px 3px 0px;
                border-image: url(:/qss_icons/rc/up_arrow_disabled.png);
                height: 10px;
                width: 10px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
        
            QScrollBar::add-line:vertical
            {
                margin: 3px 0px 3px 0px;
                border-image: url(:/qss_icons/rc/down_arrow_disabled.png);
                height: 10px;
                width: 10px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
        
            QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on
            {
                border-image: url(:/qss_icons/rc/up_arrow.png);
                height: 10px;
                width: 10px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
        
            QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on
            {
                border-image: url(:/qss_icons/rc/down_arrow.png);
                height: 10px;
                width: 10px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
        
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
            {
                background: none;
            }
        
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
            {
                background: none;
            }
        """

    class GridItem:
        """网格子项"""
        def __init__(self, widget: QWidget, col_start: int, col_span: int):
            self.widget = widget
            self.col_start = col_start
            self.col_span = col_span

    class View(QWidget):
        """视窗基类"""
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
