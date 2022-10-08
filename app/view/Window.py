# -*- coding: utf-8 -*-

"""
@File    : Window.py
@Time    : 2022/9/27 17:47
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 主窗口
"""
from PyQt5.QtCore import QEvent, QObject, Qt, QTimerEvent
from PyQt5.QtGui import QCloseEvent, QMouseEvent
from PyQt5.QtWidgets import QLabel, QMainWindow, QMenu, QProgressBar, QStatusBar, QSystemTrayIcon, \
    QToolBar

from conf.Lang import LanguageKeys
from conf.Menus import MainToolbar, MainTray
from conf.ResMap import ResMap
from conf.Views import Views
from helper.Gui import GUI
from helper.I18n import I18n
from helper.Preferences import Preferences, UserKey
from helper.Signals import Signals
from view.Notice import Notice
from view.Options import Options
from view.Webview import ReaderActions, Webview


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
        self.ui_tool_bar.setContextMenuPolicy(Qt.NoContextMenu | Qt.PreventContextMenu)
        self.ui_tool_bar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.ui_act_back_home = self.addActionBy(MainToolbar.ActionBackHome, self.ui_tool_bar)
        self.ui_act_refresh = self.addActionBy(MainToolbar.ActionRefresh, self.ui_tool_bar)
        self.ui_act_auto = self.addActionBy(MainToolbar.ActionAuto, self.ui_tool_bar)
        self.ui_act_speed_dw = self.addActionBy(MainToolbar.ActionSpeedDw, self.ui_tool_bar)
        self.ui_act_speed_up = self.addActionBy(MainToolbar.ActionSpeedUp, self.ui_tool_bar)
        self.ui_act_theme = self.addActionBy(MainToolbar.ActionExport, self.ui_tool_bar)
        self.ui_act_export = self.addActionBy(MainToolbar.ActionTheme, self.ui_tool_bar)
        self.ui_act_screen = self.addActionBy(MainToolbar.ActionFullscreen, self.ui_tool_bar)
        self.ui_act_profile = self.addActionBy(MainToolbar.ActionProfile, self.ui_tool_bar)
        self.ui_act_help = self.addActionBy(MainToolbar.ActionHelp, self.ui_tool_bar)
        self.ui_act_sponsor = self.addActionBy(MainToolbar.ActionSponsor, self.ui_tool_bar)
        self.ui_act_about = self.addActionBy(MainToolbar.ActionAbout, self.ui_tool_bar)
        self.ui_act_hide = self.addActionBy(MainToolbar.ActionHide, self.ui_tool_bar)
        self.ui_act_quit = self.addActionBy(MainToolbar.ActionQuit, self.ui_tool_bar)
        self.ui_act_pinned = self.addActionBy(MainToolbar.ActionPinned, self.ui_tool_bar)
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
        self.ui_webview.setContentsMargins(4, 4, 4, 4)

        # 1.3 系统托盘
        self.ui_tray = QSystemTrayIcon(self)
        self.ui_tray.setIcon(GUI.icon(ResMap.icon_app))
        self.ui_tray_menu = QMenu(self)
        self.addActionBy(MainTray.ActionQuit, self.ui_tray_menu)
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
        self.setWindowCode(Views.Main)
        self.setWinRectKey(UserKey.General.WinRect)
        self.setupSignals()
        self.setupPreferences()
        self.setupUi()
        self.scroller = self.startTimer(100, Qt.PreciseTimer)

    def timerEvent(self, timer: QTimerEvent):
        if timer.timerId() == self.scroller:
            self.checkScroll()

    def setupUi(self):
        self.setMinimumSize(640, 480)
        self.setWindowTitle(I18n.text(LanguageKeys.app_name))
        self.setWindowIcon(GUI.icon(ResMap.icon_app))
        self.setStatusBar(self.ui_status_bar)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.ui_tool_bar)
        self.setCentralWidget(self.ui_webview)

    def checkScroll(self):
        if self.scroller <= 0:
            return
        if self.ui_act_auto.isChecked():
            self.ui_webview.checkScroll()
        else:
            self.ui_webview.sendTip('', False)

    def setupPreferences(self):
        """初始化配置相关"""
        self.ui_act_auto.setChecked(Preferences().get(UserKey.Reader.Scrollable))
        self.ui_act_pinned.setChecked(Preferences().get(UserKey.Reader.Pinned))
        self.ui_lab_speed.setText(I18n.text(LanguageKeys.tips_speed).format(Preferences().get(UserKey.Reader.Speed)))

    def setupSignals(self):
        """关联信号和槽"""
        self.installEventFilter(self)
        self.setMouseTracking(True)
        # noinspection PyUnresolvedReferences
        self.ui_tray.activated.connect(self.onTrayActivated)
        Signals().reader_load_progress.connect(self.onRefreshProgress)
        Signals().reader_status_tip_updated.connect(self.onRefreshStatusTip)
        Signals().reader_refresh_speed.connect(self.onRefreshSpeed)

    def closeEvent(self, event: QCloseEvent):
        self.killTimer(self.scroller)
        self.scroller = -1
        Preferences().set(UserKey.Reader.LatestUrl, self.ui_webview.currentUrl())
        self.saveWinRect()
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

    def onTrayActivated(self):
        self.activateWindow()
        if self.isFullScreen():
            self.showFullScreen()
        else:
            if self.isMaximized():
                self.showMaximized()
            else:
                self.showNormal()
                tx, ty, tw, th = self.getWinRect()
                self.setGeometry(tx, ty, tw, th)

    def onRefreshProgress(self, value: int):
        self.ui_progress.setValue(value)

    def onRefreshStatusTip(self, tip: str):
        self.ui_lab_status.setText(tip)

    def onToolbarFullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def onToolbarPinned(self):
        Preferences().set(UserKey.Reader.Pinned, self.ui_act_pinned.isChecked())

    def onToolbarSpeedUp(self):
        self.adjustSpeed(True)

    def onToolbarSpeedDown(self):
        self.adjustSpeed(False)

    def adjustSpeed(self, speed_up: bool):
        step = Preferences().get(UserKey.Reader.Step)
        speed = Preferences().get(UserKey.Reader.Speed)
        now = min(100, max(1, speed + step * (1 if speed_up else -1)))
        if now != speed:
            Preferences().set(UserKey.Reader.Speed, now)
            Signals().reader_setting_changed.emit(ReaderActions.SpeedDown)
            self.onRefreshSpeed()

    def onRefreshSpeed(self):
        now = Preferences().get(UserKey.Reader.Speed)
        self.ui_lab_speed.setText(I18n.text(LanguageKeys.tips_speed).format(now))

    def onToolbarQuit(self):
        self.close()

    def onToolbarSetAuto(self):
        Preferences().set(UserKey.Reader.Scrollable, self.ui_act_auto.isChecked())
        Signals().reader_setting_changed.emit(ReaderActions.Scrollable)

    def onToolbarHide(self):
        rect = self.geometry()
        self.setGeometry(-rect.x(), -rect.y(), rect.width(), rect.height())

    @staticmethod
    def onToolbarHelp():
        Notice(Views.Help,
               UserKey.Help.WinRect,
               I18n.text(LanguageKeys.toolbar_help),
               I18n.text(LanguageKeys.notice_help)
               ).exec()

    @staticmethod
    def onToolbarAbout():
        Notice(Views.About,
               UserKey.About.WinRect,
               I18n.text(LanguageKeys.toolbar_about),
               I18n.text(LanguageKeys.notice_about)
               ).exec()

    @staticmethod
    def onToolbarProfile():
        Options().exec()

    @staticmethod
    def onToolbarSponsor():
        Notice(Views.Sponsor,
               UserKey.Help.WinRect,
               I18n.text(LanguageKeys.toolbar_sponsor),
               I18n.text(LanguageKeys.notice_sponsor)
               ).exec()

    @staticmethod
    def onToolbarExport():
        Signals().reader_setting_changed.emit(ReaderActions.ExportNote)

    @staticmethod
    def onToolbarBackHome():
        Signals().reader_setting_changed.emit(ReaderActions.BackHome)

    @staticmethod
    def onToolbarTheme():
        Signals().reader_setting_changed.emit(ReaderActions.NextTheme)

    @staticmethod
    def onToolbarReload():
        Signals().reader_setting_changed.emit(ReaderActions.Refresh)
