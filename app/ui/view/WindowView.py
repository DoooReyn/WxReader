# -*- coding: utf-8 -*-

"""
@File    : WindowView.py
@Time    : 2022/10/7 15:09
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 应用主窗口
"""
from PyQt5.QtCore import QEvent, QObject, Qt, QTimerEvent
from PyQt5.QtGui import QCloseEvent, QMouseEvent
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QLabel, QMainWindow, QMenu, QProgressBar, QStatusBar, QSystemTrayIcon, QToolBar

from conf.lang import LanguageKeys
from conf.menus import MainToolbar, MainTray
from conf.res_map import ResMap
from conf.views import Views
from helper.gui import GUI
from helper.i18n import I18n
from helper.preferences import Preferences, UserKey

# 鼠标移动事件
MOUSE_EVENT = [
    QEvent.MouseMove,
    QEvent.MouseTrackingChange,
    QEvent.NonClientAreaMouseMove,
    QEvent.Move,
    QEvent.HoverMove,
    QEvent.DragMove,
]

# 工具栏高度
TOOLBAR_HEIGHT = 53

# 工具栏显示偏移值
TOOLBAR_MOUSE_OFFSET_Y = 10

# 阅读器刷新频率
READER_TIMER_INTERVAL = 100


class WindowView(QMainWindow, GUI.View):
    """应用主窗口"""

    def __init__(self):
        super(WindowView, self).__init__()

        # 工具栏
        self.ui_tool_bar = QToolBar(self)
        self.ui_tool_bar.setFloatable(False)
        self.ui_tool_bar.setMovable(False)
        self.ui_tool_bar.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.ui_tool_bar.setAllowedAreas(Qt.ToolBarArea.AllToolBarAreas)
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

        # 状态栏
        self.ui_status_bar = QStatusBar(self)
        self.ui_progress = QProgressBar()
        self.ui_progress.setValue(0)
        self.ui_progress.setTextVisible(False)
        self.ui_lab_status = QLabel('')
        self.ui_lab_speed = QLabel('')
        self.ui_status_bar.addPermanentWidget(self.ui_lab_status, 1)
        self.ui_status_bar.addPermanentWidget(self.ui_progress, 8)
        self.ui_status_bar.addPermanentWidget(self.ui_lab_speed, 1)

        # 系统托盘
        self.ui_tray = QSystemTrayIcon(self)
        self.ui_tray.setIcon(GUI.icon(ResMap.icon_app))
        self.ui_tray_menu = QMenu(self)
        self.addActionBy(MainTray.ActionQuit, self.ui_tray_menu)
        self.ui_tray.setContextMenu(self.ui_tray_menu)
        self.ui_tray.show()

        # 中心内容
        self.ui_webview = QWebEngineView()
        self.ui_webview.setContextMenuPolicy(Qt.NoContextMenu)
        self.ui_webview.setContentsMargins(2, 2, 2, 2)

        # 准备
        self.setMinimumSize(640, 480)
        self.setWindowFlags(Qt.WindowTitleHint
                            | Qt.CustomizeWindowHint
                            | Qt.WindowSystemMenuHint
                            | Qt.WindowCloseButtonHint)
        self.setWindowTitle(I18n.text(LanguageKeys.app_name))
        self.setWindowIcon(GUI.icon(ResMap.icon_app))
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.ui_tool_bar)
        self.setStatusBar(self.ui_status_bar)
        self.setCentralWidget(self.ui_webview)
        self.installEventFilter(self)
        self.setMouseTracking(True)
        self.setWindowCode(Views.Main)
        self.setWinRectKey(UserKey.General.WinRect)
        self._timer = self.startTimer(READER_TIMER_INTERVAL, Qt.PreciseTimer)

    def timerEvent(self, timer: QTimerEvent):
        """
        定时器刷新事件
        - 在此更新阅读器页面状态
        """
        if timer.timerId() == self._timer:
            self.refreshPageStatus()
        super(WindowView, self).timerEvent(timer)

    def closeEvent(self, event: QCloseEvent):
        """
        关闭事件处理
        - 停止定时器
        - 保存用户数据
        """
        self.killTimer(self._timer)
        self._timer = -1
        self.saveWinRect()
        Preferences().set(UserKey.Reader.LatestUrl, self.ui_webview.url().toString())
        Preferences().save()
        event.accept()
        super(WindowView, self).closeEvent(event)

    def eventFilter(self, obj: QObject, event: QEvent):
        """
        事件过滤
        - 跟踪鼠标移动事件，检测鼠标与工具栏的距离，以实现工具栏的自动隐藏
        """
        et = event.type()
        if et in MOUSE_EVENT:
            self.mouseMoveEvent(event)
        return super(WindowView, self).eventFilter(obj, event)

    def mouseMoveEvent(self, event: QMouseEvent):
        """
        鼠标移动事件
        - 原本打算直接 hide 或 setEnabled(False) 工具栏，
        - 但这样做会导致其子控件关联的事件全部失效，
        - 因此通过控制 height 来实现自动隐藏工具栏的目的
        """
        if hasattr(event, 'pos') and self.ui_act_pinned.isChecked() is False:
            pos = event.pos()
            current = self.ui_tool_bar.height()
            if current == 0:
                height = TOOLBAR_HEIGHT if pos.y() <= TOOLBAR_MOUSE_OFFSET_Y else 0
            else:
                height = TOOLBAR_HEIGHT if pos.y() <= TOOLBAR_HEIGHT else 0
            if current != height:
                self.ui_tool_bar.setFixedHeight(height)
        super(WindowView, self).mouseMoveEvent(event)

    def refreshPageStatus(self):
        """更新 WebView 页面状态"""
        if self._timer <= 0:
            return
        if self.ui_act_auto.isChecked():
            # self.ui_webview.refreshPageStatus()
            pass
        else:
            # self.ui_webview.sendTip('', False)
            pass
