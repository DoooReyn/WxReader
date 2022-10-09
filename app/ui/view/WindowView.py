# -*- coding: utf-8 -*-

"""
@File    : WindowView.py
@Time    : 2022/10/7 15:09
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 应用主窗口
"""

from PyQt5.QtCore import QEvent, QObject, Qt, QTimerEvent, QUrl
from PyQt5.QtGui import QCloseEvent, QMouseEvent
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QFileDialog, QLabel, QMainWindow, QMenu, QProgressBar, QStatusBar, QSystemTrayIcon, QToolBar

from conf.Lang import LanguageKeys
from conf.Menus import MainToolbar, MainTray
from conf.ResMap import ResMap
from conf.Views import Views
from helper.Cmm import Cmm
from helper.GUI import GUI
from helper.I18n import I18n
from helper.Preferences import UserKey
from helper.Signals import Signals
from ui.model.ReaderHelper import ReaderActions
from ui.model.WebHelper import PjTransport, WebHelper
from ui.model.WindowModel import WindowModel
from ui.view.BadNotice import NetworkBadNotice, ReadingFinishedNotice
from ui.view.Notice import Notice
from ui.view.Options import Options


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
        self._transport = PjTransport("pjTransport")
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

        # 初始化 WebView
        WebHelper.newWebPage(
            self._model.BUILTIN_PROFILE,
            self._model.BUILTIN_SCRIPTS,
            self._transport,
            self.ui_webview
        )

        # 初始化配置
        self.refreshScrollable()
        self.refreshPinned()
        self.refreshSpeed()

        # 关联信号槽
        # noinspection PyUnresolvedReferences
        self.ui_tray.activated.connect(self.onTrayActivated)
        self.ui_webview.loadStarted.connect(self.onWebLoadStarted)
        self.ui_webview.loadProgress.connect(self.onWebLoadProgress)
        self.ui_webview.loadFinished.connect(self.onWebLoadFinished)
        Signals().reader_load_progress.connect(self.refreshProgress)
        Signals().reader_status_tip_updated.connect(self.refreshStatusTip)
        Signals().reader_refresh_speed.connect(self.refreshSpeed)
        Signals().reader_setting_changed.connect(self.onReaderActionTriggered)
        Signals().reader_reading_finished.connect(self.onReaderReadingFinished)
        Signals().reader_download_note.connect(self.onReaderSaveNote)

        # 启动定时器
        self._model.setTimerId(self.startTimer(self._model.READER_TIMER_INTERVAL, Qt.PreciseTimer))
        self.openUrl(self._model.latestUrl())

    def openUrl(self, url: str):
        """打开网址"""
        self.ui_webview.page().load(QUrl(url))

    def backHome(self):
        self.openUrl(self._model.HOME_PAGE)

    def currentUrl(self):
        """当前网址"""
        return self.ui_webview.page().url().toString()

    def refreshScrollable(self):
        """刷新工具栏自动阅读状态"""
        self.ui_act_auto.setChecked(self._model.scrollable())
        self._transport.refreshScrollable()

    def refreshPinned(self):
        """刷新工具栏固定此栏状态"""
        self.ui_act_pinned.setChecked(self._model.pinned())

    def refreshSpeed(self):
        """刷新状态栏阅读速度"""
        self.ui_lab_speed.setText(I18n.text(LanguageKeys.tips_speed).format(self._model.speed()))

    def refreshProgress(self, value: int):
        """刷新状态栏页面加载进度"""
        self.ui_progress.setValue(value)

    def refreshStatusTip(self, tip: str):
        """刷新状态栏提示"""
        self.ui_lab_status.setText(tip)

    def adjustSpeed(self, speed_up: bool):
        """调整阅读速度"""
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
            self.doPageScroll()
        else:
            self.refreshStatusTip('')

    def doPageScroll(self):
        """检查页面状态，执行页面滚动"""

        if self._model.scrollable() is False:
            return

        if self.isBookUrl() is False:
            # 非读书页面，返回
            self.showStatusTip(I18n.text(LanguageKeys.tips_no_book_view))
            return

        if self._transport.loading:
            # 页面正在加载中，返回
            self._transport.trigger(ReaderActions.Loading)
            self.showStatusTip(I18n.text(LanguageKeys.tips_page_ready))
            return
        else:
            if self._model.isWaitingNextChapter():
                self._transport.applyWatch()
                self._model.setWaitingNextChapter(False)
                # self.showStatusTip(I18n.text(LanguageKeys.tips_next_chapter_ready))
                return

        if self._transport.has_selection is True:
            # 有选中文本，返回
            self.showStatusTip(I18n.text(LanguageKeys.tips_has_selection))
            return

        if self._model.isWaitingNextChapter():
            # 正在等待下一章加载完成，返回
            # self.showStatusTip(I18n.text(LanguageKeys.tips_wait_for_next_chapter))
            return

        if self._transport.scroll_to_end is True:
            # 已滚动到底部，返回
            # self.showStatusTip(I18n.text(LanguageKeys.tips_scroll_to_end))
            self._transport.scroll_to_end = False
            self._model.setWaitingNextChapter(True)
            return

        # 执行页面滚动
        self.onWebPageLoaded()
        self.showStatusTip(I18n.text(LanguageKeys.tips_auto_read_on), False)
        Signals().reader_load_progress.emit(0)
        self._transport.trigger(ReaderActions.Scrolling)

    def showStatusTip(self, tip: str, output: bool = True):
        """更新状态栏提示"""
        if output:
            print(tip, self.currentUrl())
        self.refreshStatusTip(tip)

    def isBookUrl(self):
        """当前页面是否图书页"""
        return self.currentUrl().startswith(self._model.BOOK_PAGE)

    def onWebLoadStarted(self):
        """页面加载开始事件"""
        self.showStatusTip(I18n.text(LanguageKeys.tips_page_ready))
        self._transport.scroll_to_end = False
        self._transport.has_selection = False
        self._transport.applyWatch()

    def onWebLoadProgress(self, value: int):
        """页面加载中事件"""
        self.showStatusTip(I18n.text(LanguageKeys.tips_page_loading))
        Signals().reader_load_progress.emit(value)

    def onWebLoadFinished(self, result: bool):
        """页面加载结束事件"""
        if result:
            self.onWebPageLoaded()
            self.showStatusTip(I18n.text(LanguageKeys.tips_page_loaded_ok))
        else:
            self.showStatusTip(I18n.text(LanguageKeys.tips_page_loaded_bad))
            NetworkBadNotice().exec()

    def onWebPageLoaded(self):
        """页面加载完成"""
        self._transport.refreshScrollable()
        self._transport.refreshSpeed()
        self._transport.applyWatch()
        Signals().reader_load_progress.emit(0)

    def onReaderActionTriggered(self, act: int):
        """阅读器动作触发事件"""
        if act == ReaderActions.BackHome:
            self.backHome()
            return

        if act == ReaderActions.Refresh:
            self.openUrl(self.currentUrl())
            return

        if act == ReaderActions.SpeedDown or act == ReaderActions.SpeedUp:
            self._transport.refreshSpeed()
            return

        if act == ReaderActions.Scrollable:
            self._transport.refreshScrollable()
            return

        if self.isBookUrl():
            self._transport.trigger(act)

    def onReaderSaveNote(self, filename: str, content: str):
        """阅读器导出笔记动作触发事件"""
        where, _ = QFileDialog.getSaveFileName(self, I18n.text(LanguageKeys.tips_export_note), filename, filter='*.md')
        if len(where) > 0:
            Cmm.saveAs(where, content)
            self.showStatusTip(I18n.text(LanguageKeys.tips_note_exported_ok).format(filename))
        else:
            self.showStatusTip(I18n.text(LanguageKeys.tips_note_exported_bad).format(filename))

    def onReaderReadingFinished(self):
        """阅读器全文读完触发事件"""
        # TODO
        self.ui_act_auto.setChecked(False)
        ReadingFinishedNotice().exec()

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
        self._model.setLatestUrl(self.currentUrl())
        self._model.saveAll()
        event.accept()
        super(WindowView, self).closeEvent(event)

    def eventFilter(self, obj: QObject, event: QEvent):
        """
        事件过滤
        - 跟踪鼠标移动事件，检测鼠标与工具栏的距离，以实现工具栏的自动隐藏
        """
        if self._model.isMouseEvent(event.type()):
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
        """任务栏图标点击触发事件"""
        self.activateWindow()
        if self.isFullScreen():
            self.showFullScreen()
        else:
            if self.isMaximized():
                self.showMaximized()
            else:
                self.showNormal()
                # FIXME
                tx, ty, tw, th = self.getWinRect()
                self.setGeometry(tx, ty, tw, th)

    def onToolbarFullscreen(self):
        """全屏切换"""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def onToolbarPinned(self):
        """固定切换"""
        self._model.setPinned(self.ui_act_pinned.isChecked())

    def onToolbarSpeedUp(self):
        """加速"""
        self.adjustSpeed(True)

    def onToolbarSpeedDown(self):
        """减速"""
        self.adjustSpeed(False)

    def onToolbarQuit(self):
        """关闭窗口"""
        self.close()

    def onToolbarSetAuto(self):
        """切换自动阅读"""
        self._model.setScrollable(self.ui_act_auto.isChecked())
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
        """更多选项"""
        Options().exec()

    @staticmethod
    def onToolbarHelp():
        """使用帮助"""
        Notice(Views.Help,
               UserKey.Help.WinRect,
               I18n.text(LanguageKeys.toolbar_help),
               I18n.text(LanguageKeys.notice_help)
               ).exec()

    @staticmethod
    def onToolbarAbout():
        """关于应用"""
        Notice(Views.About,
               UserKey.About.WinRect,
               I18n.text(LanguageKeys.toolbar_about),
               I18n.text(LanguageKeys.notice_about)
               ).exec()

    @staticmethod
    def onToolbarSponsor():
        """赞助"""
        Notice(Views.Sponsor,
               UserKey.Help.WinRect,
               I18n.text(LanguageKeys.toolbar_sponsor),
               I18n.text(LanguageKeys.notice_sponsor)
               ).exec()

    @staticmethod
    def onToolbarExport():
        """导出笔记"""
        Signals().reader_setting_changed.emit(ReaderActions.ExportNote)

    @staticmethod
    def onToolbarBackHome():
        """回到首页"""
        Signals().reader_setting_changed.emit(ReaderActions.BackHome)

    @staticmethod
    def onToolbarTheme():
        """切换主题"""
        Signals().reader_setting_changed.emit(ReaderActions.NextTheme)

    @staticmethod
    def onToolbarReload():
        """重新加载"""
        Signals().reader_setting_changed.emit(ReaderActions.Refresh)
