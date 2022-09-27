# -*- coding: utf-8 -*-

"""
@File    : window.py
@Time    : 2022/9/27 17:47
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 主窗口
"""
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QSystemTrayIcon, QToolBar

from conf.menus import MainMenu, MainToolbar, MainTray
from conf.res_map import ResMap
from conf.user_key import UserKey
from conf.views import Views
from helper.gui import GUI
from helper.i18n import I18n
from view.notice import Notice


class _View(GUI.View):
    """
    主窗口视窗基类
    """

    def __init__(self):
        super(_View, self).__init__()

        # 1. 创建控件

        # 1.1 菜单栏
        self.ui_menu_bar = QMenuBar(self)

        menu_name = I18n.text(MainMenu.More.Name)
        self.ui_menu_file = QMenu(menu_name, self)
        self.ui_menu_bar.addMenu(self.ui_menu_file)
        self.ui_act_help = self.add_action(MainMenu.More.ActionHelp, self.ui_menu_file)
        self.ui_act_about = self.add_action(MainMenu.More.ActionAbout, self.ui_menu_file)
        self.ui_act_profile = self.add_action(MainMenu.More.ActionProfile, self.ui_menu_file)
        self.ui_act_quit = self.add_action(MainMenu.More.ActionQuit, self.ui_menu_file)

        # 1.2 工具栏
        self.ui_tool_bar = QToolBar('工具栏', self)
        self.ui_tool_bar.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.ui_tool_bar.setAllowedAreas(Qt.ToolBarArea.AllToolBarAreas)
        self.ui_tool_bar.setFloatable(False)
        self.ui_tool_bar.setMovable(False)
        self.ui_tool_bar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.ui_act_back_home = self.add_action(MainToolbar.ActionBackHome, self.ui_tool_bar)
        self.ui_act_theme = self.add_action(MainToolbar.ActionExport, self.ui_tool_bar)
        self.ui_act_export = self.add_action(MainToolbar.ActionTheme, self.ui_tool_bar)
        self.ui_act_screen = self.add_action(MainToolbar.ActionFullscreen, self.ui_tool_bar)
        self.ui_act_auto = self.add_action(MainToolbar.ActionAuto, self.ui_tool_bar)
        self.ui_act_speed_dw = self.add_action(MainToolbar.ActionSpeedDw, self.ui_tool_bar)
        self.ui_act_speed_up = self.add_action(MainToolbar.ActionSpeedUp, self.ui_tool_bar)
        self.ui_act_sponsor = self.add_action(MainToolbar.ActionSponsor, self.ui_tool_bar)

        # 1.3 内容
        self.ui_webview = QWebEngineView()
        self.ui_webview.setContextMenuPolicy(Qt.NoContextMenu)

        # 1.4 系统托盘
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
        self.setup_ui()

    def setup_ui(self):
        self.setMinimumSize(640, 480)
        self.setWindowTitle(I18n.text('app:name'))
        self.setWindowIcon(GUI.icon(ResMap.icon_app))
        self.setMenuBar(self.ui_menu_bar)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.ui_tool_bar)
        self.setCentralWidget(self.ui_webview)
        self.ui_webview.load(Window.HOME_PAGE)

    def setup_signals(self):
        # noinspection PyUnresolvedReferences
        self.ui_tray.activated.connect(self.on_tray_activated)

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
        print('on_toolbar_set_auto')
        pass

    def on_toolbar_theme(self):
        print('on_toolbar_theme')
        pass

    @staticmethod
    def on_main_menu_quit():
        QApplication.exit()
