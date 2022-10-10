# -*- coding: utf-8 -*-

"""
@File    : GUI.py
@Time    : 2022/9/27 17:21
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : GUI辅助工具
"""
from enum import Enum, unique
from typing import Union

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QColor, QFont, QIcon
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QAction, QMenu, QToolBar, QWidget

from conf.Lang import LanguageKeys
from conf.Menus import ActionInfo
from helper.Cmm import Cmm
from helper.I18n import I18n
from helper.Preferences import Preferences
from helper.Signals import Signals


class GUI:
    """GUI辅助工具"""

    @unique
    class WindowsSounds(Enum):
        """Windows系统音频"""
        Background = "Windows Background"
        Foreground = "Windows Foreground"
        Logon = "Windows Logon"
        MessageNudge = "Windows Message Nudge"
        NotifyCalendar = "Windows Notify Calendar"
        NotifyEmail = "Windows Notify Email"
        NotifyMessaging = "Windows Notify Messaging"
        NotifySystemGeneric = "Windows Notify System Generic"
        ProximityConnection = "Windows Proximity Connection"
        ProximityNotification = "Windows Proximity Notification"
        Unlock = "Windows Unlock"
        MenuCommand = "Windows Menu Command"
        Error = "Windows Error"
        PrintComplete = "Windows Print complete"
        NavigationStart = "Windows Navigation Start"
        BatteryLow = "Windows Battery Low"
        BatteryCritical = "Windows Battery Critical"
        CriticalStop = "Windows Critical Stop"
        Ringout = "Windows Ringout"
        Ringin = "Windows Ringin"
        Exclamation = "Windows Exclamation"
        Shutdown = "Windows Shutdown"
        Restore = "Windows Restore"
        Recycle = "Windows Recycle"
        Ding = "Windows Ding"
        Default = "Windows Default"
        Startup = "Windows Startup"
        Balloon = "Windows Balloon"
        Notify = "Windows Notify"
        InformationBar = "Windows Information Bar"
        FeedDiscovered = "Windows Feed Discovered"
        PopupBlocked = "Windows Pop-up Blocked"
        HardwareInsert = "Windows Hardware Insert"
        HardwareFail = "Windows Hardware Fail"
        HardwareRemove = "Windows Hardware Remove"
        UserAccountControl = "Windows User Account Control"
        LogoffSound = "Windows Logoff Sound"
        Minimize = "Windows Minimize"

    class Preferences:
        """默认值"""
        layout_spacing = 8
        line_height = 36
        font_size = 14
        font_name = '微软雅黑'
        view_size = QSize(640, 480)
        WindowsMediaAt = "C:/Windows/Media/{}.wav"

    class Theme:
        """主题"""
        Default = """
            QWidget 
            {
                font-family: "微软雅黑"; 
                font-size: 13px;
            }
            
            QProgressBar 
            {
                border: none;
                background-color: #f1f1f1;
            }
            
            QProgressBar::chunk 
            {
                background-color: #85caff;
                width: 4px;
                margin: 0.5px;
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
                border: 1px solid #34a7ff;
                border-radius: 4px;
                background: #f4f8f8;
                font: 15px;
                min-width: 64px;
                min-height: 32px;
            }
            
            QPushButton::hover,pressed
            {
                font: bold;
                background: #f4f8f8;
            }
            
            QPushButton::pressed
            {
                font: bold;
                margin: 0 4px 0 4px;
                background: #f4f8f8;
            }
            
            QToolButton::hover,pressed {
                border: 1px solid #8f8f8f;
                border-radius: 4px;
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
                self.saveWinRect()
            if self.window_code > 0:
                Signals().win_closed.emit(self.window_code)
            event.accept()
            super(GUI.View, self).closeEvent(event)

        def resizeEvent(self, event):
            if self.rect_key is not None:
                self.saveWinRect()
            event.accept()
            super().resizeEvent(event)

        def setWindowCode(self, code: int):
            self.window_code = code

        def setWinRectKey(self, kr: str):
            self.rect_key = kr
            tx, ty, w, h = self.getWinRect()
            self.setGeometry(tx, ty, w, h)

        def getWinRect(self):
            if self.rect_key is not None:
                return [int(v) for v in Preferences().get(self.rect_key)]
            else:
                r = self.geometry()
                return r.topLeft().x(), r.topLeft().y(), r.width(), r.height()

        def saveWinRect(self):
            if self.rect_key is not None:
                r = self.geometry()
                rect = [r.topLeft().x(), r.topLeft().y(), r.width(), r.height()]
                Preferences().set(self.rect_key, rect)

        @staticmethod
        def onMenuActionNotImplemented(menu, name):
            msg = I18n.text(LanguageKeys.debug_method_not_implemented).format(menu, name)
            Signals().logger_warn.emit(msg)
            print(msg)

        def addActionBy(self, act_info: ActionInfo, parent: Union[QMenu, QToolBar]):
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
                act.triggered.connect(
                    lambda *args, m=parent.objectName(), n=name: self.onMenuActionNotImplemented(m, n))
            parent.addAction(act)
            return act

    @staticmethod
    def viewSize():
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

    @staticmethod
    def playSound(sound_type: WindowsSounds):
        if Cmm.isWindows():
            sound_path = GUI.Preferences.WindowsMediaAt.format(sound_type.value)
            QSound.play(sound_path)
