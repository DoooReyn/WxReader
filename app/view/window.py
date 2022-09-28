# -*- coding: utf-8 -*-

"""
@File    : window.py
@Time    : 2022/9/27 17:47
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 主窗口
"""
from PyQt5.QtCore import QEvent, QObject, Qt, QUrl
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QSystemTrayIcon, QToolBar

from conf.menus import MainToolbar, MainTray
from conf.res_map import ResMap
from conf.user_key import UserKey
from conf.views import Views
from helper.gui import GUI
from helper.i18n import I18n
from helper.preferences import Preferences
from view.notice import Notice


class _View(GUI.View):
    """
    主窗口视窗基类
    """

    def __init__(self):
        super(_View, self).__init__()

        # 1. 创建控件

        # 1.1 工具栏
        self.ui_tool_bar = QToolBar(self)
        self.ui_tool_bar.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.ui_tool_bar.setAllowedAreas(Qt.ToolBarArea.AllToolBarAreas)
        self.ui_tool_bar.setFloatable(False)
        self.ui_tool_bar.setMovable(False)
        self.ui_tool_bar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.ui_act_back_home = self.add_action(MainToolbar.ActionBackHome, self.ui_tool_bar)
        self.ui_act_auto = self.add_action(MainToolbar.ActionAuto, self.ui_tool_bar)
        self.ui_act_speed_dw = self.add_action(MainToolbar.ActionSpeedDw, self.ui_tool_bar)
        self.ui_act_speed_up = self.add_action(MainToolbar.ActionSpeedUp, self.ui_tool_bar)
        self.ui_act_theme = self.add_action(MainToolbar.ActionExport, self.ui_tool_bar)
        self.ui_act_export = self.add_action(MainToolbar.ActionTheme, self.ui_tool_bar)
        self.ui_act_screen = self.add_action(MainToolbar.ActionFullscreen, self.ui_tool_bar)
        self.ui_act_profile = self.add_action(MainToolbar.ActionProfile, self.ui_tool_bar)
        self.ui_act_help = self.add_action(MainToolbar.ActionHelp, self.ui_tool_bar)
        self.ui_act_sponsor = self.add_action(MainToolbar.ActionSponsor, self.ui_tool_bar)
        self.ui_act_about = self.add_action(MainToolbar.ActionAbout, self.ui_tool_bar)
        self.ui_act_quit = self.add_action(MainToolbar.ActionQuit, self.ui_tool_bar)
        self.ui_act_pinned = self.add_action(MainToolbar.ActionPinned, self.ui_tool_bar)
        self.ui_act_auto.setCheckable(True)
        self.ui_act_pinned.setCheckable(True)

        # 1.2 内容
        self.ui_webview = QWebEngineView()
        self.ui_webview.setContextMenuPolicy(Qt.NoContextMenu)

        # 1.3 系统托盘
        self.ui_tray = QSystemTrayIcon(self)
        self.ui_tray.setIcon(GUI.icon(ResMap.icon_app))
        self.ui_tray_menu = QMenu(self)
        self.add_action(MainTray.ActionQuit, self.ui_tray_menu)
        self.ui_tray.setContextMenu(self.ui_tray_menu)
        self.ui_tray.show()


class Window(QMainWindow, _View):
    """
    主窗口
        - 继承自视窗基类
        - 继承自 QMainWindow
    """
    HOME_PAGE = QUrl('https://weread.qq.com/')

    def __init__(self):
        super(Window, self).__init__()

        self.set_window_code(Views.Main)
        self.set_rect_key(UserKey.General.WinRect)
        self.setup_signals()
        self.setup_preferences()
        self.setup_ui()

    def setup_ui(self):
        self.setMinimumSize(640, 480)
        self.setWindowTitle(I18n.text('app:name'))
        self.setWindowIcon(GUI.icon(ResMap.icon_app))
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.ui_tool_bar)
        self.setCentralWidget(self.ui_webview)
        self.ui_webview.load(Window.HOME_PAGE)

    def setup_preferences(self):
        self.ui_act_auto.setChecked(Preferences.storage.value(UserKey.Reader.Scrollable, False, bool))
        self.ui_act_pinned.setChecked(Preferences.storage.value(UserKey.Reader.Pinned, True, bool))

    def setup_signals(self):
        self.installEventFilter(self)
        self.setMouseTracking(True)
        # noinspection PyUnresolvedReferences
        self.ui_tray.activated.connect(self.on_tray_activated)

    def eventFilter(self, obj: 'QObject', event: QEvent) -> bool:
        et = event.type()
        # event.
        # display = True
        # if et in [QEvent.Enter, QEvent.WindowActivate, QEvent.HoverEnter, QEvent.HoverMove, QEvent.MouseMove]:
        #     display = True
        # if self.isFullScreen():
        #     self.ui_tool_bar.hide()
        # else:
        #     self.ui_tool_bar.show() if display else self.ui_tool_bar.hide()
        # print(event.type(), display)
        moved = et in [
            QEvent.MouseMove,
            QEvent.MouseTrackingChange,
            QEvent.NonClientAreaMouseMove,
            QEvent.GraphicsSceneMouseMove,
            QEvent.Move,
            QEvent.HoverMove,
            QEvent.GraphicsSceneDragMove,
            QEvent.DragMove,
            QEvent.GraphicsSceneHoverMove,
            QEvent.GraphicsSceneMove,
            QEvent.TabletMove,
        ]
        # print(et, moved)
        if moved:
            self.mouseMoveEvent(event)
        return super(Window, self).eventFilter(obj, event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """
        自动隐藏工具栏
        - 使用 hide 会导致控件不可用，连带其子控件关联的事件都失效了，因此使用 height 来控制它的
        """
        if hasattr(event, 'pos') and self.ui_act_pinned.isChecked() is False:
            pos = event.pos()
            current = self.ui_tool_bar.height()
            if current == 0:
                height = 53 if pos.y() <= 10 else 0
            else:
                height = 53 if pos.y() <= 53 else 0
            if current != height:
                self.ui_tool_bar.setFixedHeight(height)

    def on_tray_activated(self):
        self.activateWindow()
        self._show()

    def _show(self):
        if self.isFullScreen():
            self.showFullScreen()
        else:
            if self.isMaximized():
                self.showMaximized()
            else:
                self.showNormal()

    @staticmethod
    def on_main_menu_help():
        Notice(Views.Help,
               UserKey.Help.WinRect,
               I18n.text("main_menu:more:help"),
               I18n.text("notice:help")
               ).exec()

    @staticmethod
    def on_main_menu_about():
        Notice(Views.About,
               UserKey.About.WinRect,
               I18n.text("main_menu:more:about"),
               I18n.text("notice:about")
               ).exec()

    def on_main_menu_profile(self):
        print('on_main_menu_profile')
        pass

    def on_toolbar_sponsor(self):
        print('on_toolbar_sponsor')

    def on_toolbar_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def on_toolbar_speed_up(self):
        print('on_toolbar_speed_up')
        pass

    def on_toolbar_speed_dw(self):
        print('on_toolbar_speed_dw')
        pass

    def on_toolbar_export(self):
        print('on_toolbar_export')
        pass

    def on_toolbar_back_home(self):
        self.ui_webview.load(Window.HOME_PAGE)

    def on_toolbar_set_auto(self):
        Preferences.storage.setValue(UserKey.Reader.Scrollable, self.ui_act_auto.isChecked())

    def on_toolbar_theme(self):
        print('on_toolbar_theme')
        pass

    def on_toolbar_pinned(self):
        Preferences.storage.setValue(UserKey.Reader.Pinned, self.ui_act_pinned.isChecked())

    @staticmethod
    def on_main_menu_quit():
        QApplication.exit()
