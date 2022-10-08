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

from conf.Lang import LanguageKeys
from conf.Menus import MainToolbar, MainTray
from conf.ResMap import ResMap
from conf.Views import Views
from helper.Gui import GUI
from helper.I18n import I18n
from helper.Preferences import Preferences, UserKey
from helper.Signals import Signals
from ui.model.WindowModel import WindowModel
from view.Notice import Notice
from view.Options import Options

# 鼠标移动事件
MOUSE_EVENT = [
    QEvent.MouseMove,
    QEvent.MouseTrackingChange,
    QEvent.NonClientAreaMouseMove,
    QEvent.Move,
    QEvent.HoverMove,
    QEvent.DragMove,
]


class ReaderActions:
    """阅读器动作"""

    # 回到首页
    BackHome = 0
    # 刷新页面
    Refresh = 1
    # 切换自动阅读
    Scrollable = 2
    # 降低滚动速度
    SpeedDown = 3
    # 加快滚动速度
    SpeedUp = 4
    # 导出笔记
    ExportNote = 5
    # 切换主题
    NextTheme = 6
    # 启用页面选中状态监听
    Watching = 11
    # 启用页面滚动状态监听
    Scrolling = 12
    # 启用页面加载状态监听
    Loading = 13
    # 关闭自动阅读
    ScrollableOff = 20
    # 开启自动阅读
    ScrollableOn = 21


class _View(GUI.View):
    def __init__(self):
        super(_View, self).__init__()
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


class WindowView(QMainWindow, _View):
    """应用主窗口"""

    def __init__(self):
        super(WindowView, self).__init__()

        self._model = WindowModel()
        self.start()

    def start(self):
        """准备"""
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
        self.setWindowCode(Views.Main)
        self.setWinRectKey(UserKey.General.WinRect)

        # 初始化配置
        self.refreshScrollable()
        self.refreshPinned()
        self.refreshSpeed()

        # 关联信号槽
        # noinspection PyUnresolvedReferences
        self.ui_tray.activated.connect(self.onTrayActivated)
        Signals().page_loading_progress.connect(self.onRefreshProgress)
        Signals().status_tip_updated.connect(self.onRefreshStatusTip)
        Signals().reader_refresh_speed.connect(self.refreshSpeed)

        # 启动定时器
        self._model.setTimerId(self.startTimer(self._model.READER_TIMER_INTERVAL, Qt.PreciseTimer))

    def refreshScrollable(self):
        self.ui_act_auto.setChecked(self._model.scrollable())

    def refreshPinned(self):
        self.ui_act_pinned.setChecked(self._model.pinned())

    def refreshSpeed(self):
        self.ui_lab_speed.setText(I18n.text(LanguageKeys.tips_speed).format(self._model.speed()))

    def adjustSpeed(self, speed_up: bool):
        pre = self._model.speed()
        now = self._model.nextSpeed(speed_up)
        if now != pre:
            self._model.setSpeed(now)
            self.refreshSpeed()
            Signals().reader_setting_changed.emit(ReaderActions.SpeedDown)

    def refreshPageStatus(self):
        """更新 WebView 页面状态"""
        if self._model.isValidTimer() is False:
            return

        if self.ui_act_auto.isChecked():
            # self.ui_webview.refreshPageStatus()
            pass
        else:
            # self.ui_webview.sendTip('', False)
            pass

    def timerEvent(self, timer: QTimerEvent):
        """
        定时器刷新事件
        - 在此更新阅读器页面状态
        """
        if timer.timerId() == self._model.timerId():
            self.refreshPageStatus()
        super(WindowView, self).timerEvent(timer)

    def closeEvent(self, event: QCloseEvent):
        """
        关闭事件处理
        - 停止定时器
        - 保存用户数据
        """
        if self._model.isValidTimer():
            self.killTimer(self._model.timerId())
            self._model.clearTimerId()
        self.saveWinRect()
        self._model.setLatestUrl(self.ui_webview.url().toString())
        self._model.saveAll()
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
            pre = self.ui_tool_bar.height()
            cur = self._model.checkToolbarHeight(pre, pos.y())
            if cur != pre:
                self.ui_tool_bar.setFixedHeight(cur)

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

    def onToolbarQuit(self):
        self.close()

    def onToolbarSetAuto(self):
        Preferences().set(UserKey.Reader.Scrollable, self.ui_act_auto.isChecked())
        Signals().reader_setting_changed.emit(ReaderActions.Scrollable)

    def onToolbarHide(self):
        """
        退到后台
        - FIXME: 在 Win7 上不会移动到不可见区域
        """
        rect = self.geometry()
        self.setGeometry(-rect.x(), -rect.y(), rect.width(), rect.height())

    @staticmethod
    def onToolbarProfile():
        Options().exec()

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
