# -*- coding: utf-8 -*-

"""
@File    : window.py
@Time    : 2022/9/27 17:47
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 主窗口
"""
from PyQt5.QtCore import QEvent, QObject, Qt, QTimerEvent
from PyQt5.QtGui import QCloseEvent, QMouseEvent
from PyQt5.QtWidgets import QLabel, QMainWindow, QMenu, QProgressBar, QStatusBar, QSystemTrayIcon, \
    QToolBar

from conf.menus import MainToolbar, MainTray
from conf.res_map import ResMap
from conf.views import Views
from helper.gui import GUI
from helper.i18n import I18n
from helper.preferences import Preferences, UserKey
from helper.signals import Signals
from view.notice import Notice
from view.options import Options
from view.webview import ReaderActions, Webview


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
        self.ui_act_refresh = self.add_action(MainToolbar.ActionRefresh, self.ui_tool_bar)
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
        self.ui_act_hide = self.add_action(MainToolbar.ActionHide, self.ui_tool_bar)
        self.ui_act_quit = self.add_action(MainToolbar.ActionQuit, self.ui_tool_bar)
        self.ui_act_pinned = self.add_action(MainToolbar.ActionPinned, self.ui_tool_bar)
        self.ui_act_auto.setCheckable(True)
        self.ui_act_pinned.setCheckable(True)

        self.ui_status_bar = QStatusBar(self)
        self.ui_progress = QProgressBar()
        self.ui_progress.setValue(0)
        self.ui_progress.setTextVisible(False)
        self.ui_lab_status = QLabel('')
        self.ui_lab_speed = QLabel('')
        self.ui_status_bar.addPermanentWidget(self.ui_lab_status, 1)
        self.ui_status_bar.addPermanentWidget(self.ui_progress, 8)
        self.ui_status_bar.addPermanentWidget(self.ui_lab_speed, 1)

        # 1.2 内容
        self.ui_webview = Webview()
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

    def __init__(self):
        super(Window, self).__init__()

        self.setWindowFlags(Qt.WindowTitleHint
                            | Qt.CustomizeWindowHint
                            | Qt.WindowSystemMenuHint
                            | Qt.WindowCloseButtonHint)
        self.set_window_code(Views.Main)
        self.set_rect_key(UserKey.General.WinRect)
        self.setup_signals()
        self.setup_preferences()
        self.setup_ui()
        self.scroller = self.startTimer(100, Qt.PreciseTimer)

    def timerEvent(self, timer: QTimerEvent):
        if timer.timerId() == self.scroller:
            self._check_scroll()

    def setup_ui(self):
        self.setMinimumSize(640, 480)
        self.setWindowTitle(I18n.text('app:name'))
        self.setWindowIcon(GUI.icon(ResMap.icon_app))
        self.setStatusBar(self.ui_status_bar)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.ui_tool_bar)
        self.setCentralWidget(self.ui_webview)

    def _check_scroll(self):
        if self.scroller <= 0:
            return
        if self.ui_act_auto.isChecked():
            self.ui_webview.check_scroll()
        else:
            self.ui_webview.send_tip('', False)

    def setup_preferences(self):
        """初始化配置相关"""
        self.ui_act_auto.setChecked(Preferences().get(UserKey.Reader.Scrollable))
        self.ui_act_pinned.setChecked(Preferences().get(UserKey.Reader.Pinned))
        self.ui_lab_speed.setText(I18n.text("tips:speed").format(Preferences().get(UserKey.Reader.Speed)))

    def setup_signals(self):
        """关联信号和槽"""
        self.installEventFilter(self)
        self.setMouseTracking(True)
        # noinspection PyUnresolvedReferences
        self.ui_tray.activated.connect(self.on_tray_activated)
        Signals().page_loading_progress.connect(self.on_update_progress)
        Signals().status_tip_updated.connect(self.on_update_status_tip)
        Signals().reader_refresh_speed.connect(self.on_refresh_speed)

    def closeEvent(self, event: QCloseEvent):
        self.killTimer(self.scroller)
        self.scroller = -1
        Preferences().set(UserKey.Reader.LatestUrl, self.ui_webview.current_url())
        self.save_win_rect()
        Preferences().save()
        event.accept()
        super(Window, self).closeEvent(event)

    def eventFilter(self, obj: QObject, event: QEvent):
        et = event.type()

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
        if moved:
            self.mouseMoveEvent(event)
        return super(Window, self).eventFilter(obj, event)

    def mouseMoveEvent(self, event: QMouseEvent):
        """
        自动隐藏工具栏
        - 使用 hide 会导致控件不可用，连带其子控件关联的事件都失效了，因此使用 height 来控制
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
        if self.isFullScreen():
            self.showFullScreen()
        else:
            if self.isMaximized():
                self.showMaximized()
            else:
                self.showNormal()
                tx, ty, tw, th = self.get_win_rect()
                self.setGeometry(tx, ty, tw, th)

    def on_update_progress(self, value: int):
        self.ui_progress.setValue(value)

    def on_update_status_tip(self, tip: str):
        self.ui_lab_status.setText(tip)

    def on_toolbar_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def on_toolbar_pinned(self):
        Preferences().set(UserKey.Reader.Pinned, self.ui_act_pinned.isChecked())

    def on_toolbar_speed_up(self):
        self.adjust_speed(True)

    def on_toolbar_speed_dw(self):
        self.adjust_speed(False)

    def adjust_speed(self, speed_up: bool):
        step = Preferences().get(UserKey.Reader.Step)
        speed = Preferences().get(UserKey.Reader.Speed)
        now = min(100, max(1, speed + step * (1 if speed_up else -1)))
        if now != speed:
            Preferences().set(UserKey.Reader.Speed, now)
            Signals().reader_setting_changed.emit(ReaderActions.SpeedDown)
            self.on_refresh_speed()

    def on_refresh_speed(self):
        now = Preferences().get(UserKey.Reader.Speed)
        self.ui_lab_speed.setText(I18n.text("tips:speed").format(now))

    def on_toolbar_quit(self):
        self.close()

    def on_toolbar_set_auto(self):
        Preferences().set(UserKey.Reader.Scrollable, self.ui_act_auto.isChecked())
        Signals().reader_setting_changed.emit(ReaderActions.Scrollable)

    def on_toolbar_hide(self):
        rect = self.geometry()
        self.setGeometry(-rect.x(), -rect.y(), rect.width(), rect.height())

    @staticmethod
    def on_toolbar_help():
        Notice(Views.Help,
               UserKey.Help.WinRect,
               I18n.text("toolbar:help"),
               I18n.text("notice:help")
               ).exec()

    @staticmethod
    def on_toolbar_about():
        Notice(Views.About,
               UserKey.About.WinRect,
               I18n.text("toolbar:about"),
               I18n.text("notice:about")
               ).exec()

    @staticmethod
    def on_toolbar_profile():
        Options().exec()

    @staticmethod
    def on_toolbar_sponsor():
        Notice(Views.Sponsor,
               UserKey.Help.WinRect,
               I18n.text("toolbar:sponsor"),
               I18n.text("notice:sponsor")
               ).exec()

    @staticmethod
    def on_toolbar_export():
        Signals().reader_setting_changed.emit(ReaderActions.ExportNote)

    @staticmethod
    def on_toolbar_back_home():
        Signals().reader_setting_changed.emit(ReaderActions.BackHome)

    @staticmethod
    def on_toolbar_theme():
        Signals().reader_setting_changed.emit(ReaderActions.NextTheme)

    @staticmethod
    def on_toolbar_refresh():
        Signals().reader_setting_changed.emit(ReaderActions.Refresh)
