# -*- coding: utf-8 -*-

"""
@File    : WindowView.py
@Time    : 2022/10/7 15:09
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 主视图
"""
from typing import Optional

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QMenu,
    QStatusBar,
    QSystemTrayIcon,
    QToolBar, QApplication, QLineEdit
)

from conf.Lang import LanguageKeys
from conf.Menus import MainToolbar, MainTray
from conf.ResMap import ResMap
from conf.Views import Views
from helper.Cmm import Cmm
from helper.GUI import GUI
from helper.I18n import I18n
from helper.NetHelper import NetHelper
from helper.Preferences import UserKey, gPreferences
from helper.Signals import gSignals
from ui.model.CefModel import CefModel
from ui.view.CefView import CefView
from ui.view.NoticeView import NoticeView, ContentFillType
from ui.view.OptionsView import OptionsView
from ui.view.SponsorView import SponsorView
from ui.view.ToolbarAction import ScrollableAction, PinnedAction, SpeedDwAction, SpeedUpAction
from ui.view.ViewDelegate import ViewDelegate


class _View(ViewDelegate):
    """主视图 UI"""

    def __init__(self, win, code, key):
        super(_View, self).__init__(win, code, key)

        # 工具栏
        # noinspection PyTypeChecker
        self.ui_tool_bar = QToolBar(self.view)
        self.ui_tool_bar.setFloatable(False)
        self.ui_tool_bar.setMovable(False)
        self.ui_tool_bar.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.ui_tool_bar.setAllowedAreas(Qt.ToolBarArea.TopToolBarArea)
        self.ui_tool_bar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.ui_tool_bar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.ui_act_help = self.addActionBy(MainToolbar.ActionHelp, self.ui_tool_bar)
        self.ui_act_about = self.addActionBy(MainToolbar.ActionAbout, self.ui_tool_bar)
        self.ui_act_sponsor = self.addActionBy(MainToolbar.ActionSponsor, self.ui_tool_bar)
        self.ui_act_back_home = self.addActionBy(MainToolbar.ActionBackHome, self.ui_tool_bar)
        self.ui_act_refresh = self.addActionBy(MainToolbar.ActionRefresh, self.ui_tool_bar)
        self.ui_act_pinned = self.addActionBy(MainToolbar.ActionPinned, self.ui_tool_bar)
        self.ui_act_export = self.addActionBy(MainToolbar.ActionExport, self.ui_tool_bar)
        self.ui_act_theme = self.addActionBy(MainToolbar.ActionTheme, self.ui_tool_bar)
        self.ui_act_auto = self.addActionBy(MainToolbar.ActionAuto, self.ui_tool_bar)
        self.ui_act_screen = self.addActionBy(MainToolbar.ActionFullscreen, self.ui_tool_bar)
        self.ui_act_profile = self.addActionBy(MainToolbar.ActionProfile, self.ui_tool_bar)
        self.ui_act_speed_dw = self.addActionBy(MainToolbar.ActionSpeedDw, self.ui_tool_bar)
        self.ui_act_speed_up = self.addActionBy(MainToolbar.ActionSpeedUp, self.ui_tool_bar)
        self.ui_act_quit = self.addActionBy(MainToolbar.ActionQuit, self.ui_tool_bar)
        self.ui_act_back_home.setToolTip(I18n.text(LanguageKeys.tooltip_back_home))
        self.ui_act_refresh.setToolTip(I18n.text(LanguageKeys.tooltip_refresh))
        self.ui_act_auto.setToolTip(I18n.text(LanguageKeys.tooltip_auto))
        self.ui_act_speed_dw.setToolTip(I18n.text(LanguageKeys.tooltip_speed_dw))
        self.ui_act_speed_up.setToolTip(I18n.text(LanguageKeys.tooltip_speed_up))
        self.ui_act_theme.setToolTip(I18n.text(LanguageKeys.tooltip_theme))
        self.ui_act_export.setToolTip(I18n.text(LanguageKeys.tooltip_export))
        self.ui_act_screen.setToolTip(I18n.text(LanguageKeys.tooltip_fullscreen))
        self.ui_act_profile.setToolTip(I18n.text(LanguageKeys.tooltip_profile))
        self.ui_act_about.setToolTip(I18n.text(LanguageKeys.tooltip_about))
        self.ui_act_help.setToolTip(I18n.text(LanguageKeys.tooltip_help))
        self.ui_act_sponsor.setToolTip(I18n.text(LanguageKeys.tooltip_sponsor))
        self.ui_act_pinned.setToolTip(I18n.text(LanguageKeys.tooltip_pinned))
        self.ui_act_quit.setToolTip(I18n.text(LanguageKeys.tooltip_quit))
        self.ui_act_auto.setCheckable(True)
        self.ui_act_theme.setEnabled(False)

        # stateful actions
        self.stateful_act_auto = ScrollableAction(self.ui_act_auto)
        self.stateful_act_pinned = PinnedAction(self.ui_act_pinned, self.ui_tool_bar)
        self.stateful_act_speed_up = SpeedUpAction(self.ui_act_speed_up)
        self.stateful_act_speed_dw = SpeedDwAction(self.ui_act_speed_dw)

        # 状态栏
        # noinspection PyTypeChecker
        self.ui_status_bar = QStatusBar(self.view)
        self.ui_lab_status = QLabel('')
        self.ui_edit_url = QLineEdit('')
        self.ui_edit_url.setReadOnly(True)
        self.ui_edit_url.setStyleSheet("QLineEdit { border: none; background-color: #f0f0f0;}")
        self.ui_lab_speed = QLabel('')
        self.ui_status_bar.addPermanentWidget(self.ui_lab_status, 1)
        self.ui_status_bar.addPermanentWidget(self.ui_edit_url, 8)
        self.ui_status_bar.addPermanentWidget(self.ui_lab_speed, 1)

        # 系统托盘
        self.ui_tray = QSystemTrayIcon(self.view)
        self.ui_tray.setIcon(GUI.icon(ResMap.icon_app))
        self.ui_tray_menu = QMenu(self.view)
        self.addActionBy(MainTray.ActionHelp, self.ui_tray_menu)
        self.addActionBy(MainTray.ActionQuit, self.ui_tray_menu)
        self.ui_tray.setContextMenu(self.ui_tray_menu)
        self.ui_tray.setToolTip(I18n.text(LanguageKeys.app_name))
        self.ui_tray.show()

        # Webview
        self.ui_cef = CefView(self.view)


class WindowView(QMainWindow):
    """应用主窗口"""

    def __init__(self):
        super(WindowView, self).__init__()

        self.timer_cef: Optional[QTimer] = None
        self.timer_reading: Optional[QTimer] = None
        self.view = _View(self, Views.Main, UserKey.General.WinRect)

        self.setupUi()
        self.setupSignals()
        self.setupCefTimer()
        self.setupReadingTimer()

    def setupUi(self):
        """初始化 UI"""
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
        self.setAttribute(Qt.WidgetAttribute.WA_StaticContents, True)
        self.setMinimumSize(640, 480)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setWindowTitle(I18n.text(LanguageKeys.app_name))
        self.setWindowIcon(GUI.icon(ResMap.icon_app))
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.view.ui_tool_bar)
        self.setStatusBar(self.view.ui_status_bar)
        self.view.ui_cef.resize(self.size())
        self.view.ui_cef.embedBrowser()
        self.view.ui_edit_url.setText(gPreferences.get(UserKey.Reader.LatestUrl))
        self.view.stateful_act_auto.onLoad()
        self.view.stateful_act_pinned.onLoad()
        self.refreshSpeed()
        self.setCentralWidget(self.view.ui_cef)

    def setupSignals(self):
        """关联信号"""
        # noinspection PyUnresolvedReferences
        self.view.ui_tray.activated.connect(self.onTrayActivated)
        gSignals.cef_load_start.connect(self.onLoadPage)
        gSignals.cef_update_state.connect(self.onLoadPage)
        gSignals.cef_load_finished.connect(self.onLoadPage)
        gSignals.cef_short_cut.connect(self.onShortcutActivated)
        gSignals.reader_refresh_speed.connect(self.refreshSpeed)
        gSignals.reader_status_tip_updated.connect(self.refreshStatusTip)
        gSignals.reader_reading_finished.connect(self.onBookFinished)

    def refreshStatusTip(self, tip: str):
        """刷新状态栏提示"""
        self.view.ui_lab_status.setText(tip)

    def onBookFinished(self):
        """全书完"""
        self.view.ui_act_auto.setChecked(False)
        self.view.stateful_act_auto.onChanged()
        self.activateWindow()
        self.showNormal()
        Cmm.playBeep()
        NetHelper.httpGet(gPreferences.get(UserKey.Profile.NoticeUrl))

    def onShortcutActivated(self, shortcut: int):
        """
        快捷键响应
        - 因为 Cef 会吞噬 Qt 事件，所以触发不了快捷键
        - 所以，在 Cef 层监听快捷键再发送给 Qt 去执行
        """
        if shortcut == CefModel.ShortCut.Quit:
            self.onToolbarQuit()
        elif shortcut == CefModel.ShortCut.Reload:
            self.onToolbarReload()
        elif shortcut == CefModel.ShortCut.About:
            self.onToolbarAbout()
        elif shortcut == CefModel.ShortCut.Help:
            self.onToolbarHelp()
        elif shortcut == CefModel.ShortCut.Sponsor:
            self.onToolbarSponsor()
        elif shortcut == CefModel.ShortCut.Options:
            self.onToolbarProfile()
        elif shortcut == CefModel.ShortCut.SpeedUp:
            self.onToolbarSpeedUp()
        elif shortcut == CefModel.ShortCut.SpeedDown:
            self.onToolbarSpeedDown()
        elif shortcut == CefModel.ShortCut.Theme:
            self.onToolbarTheme()
        elif shortcut == CefModel.ShortCut.Export:
            self.onToolbarExport()
        elif shortcut == CefModel.ShortCut.Home:
            self.onToolbarBackHome()
        elif shortcut == CefModel.ShortCut.Fullscreen:
            self.onToolbarFullscreen()
        elif shortcut == CefModel.ShortCut.Auto:
            checked = self.view.ui_act_auto.isChecked()
            self.view.ui_act_auto.setChecked(not checked)
            self.onToolbarSetAuto()
        elif shortcut == CefModel.ShortCut.Pinned:
            self.onToolbarPinned()
        else:
            print(f'未知的快捷键: {shortcut}')

    def refreshSpeed(self):
        """刷新状态栏阅读速度"""
        speed = gPreferences.get(UserKey.Reader.Speed)
        self.view.ui_lab_speed.setText(I18n.text(LanguageKeys.tips_speed).format(speed))

    def onLoadPage(self):
        """更新页面网址"""
        self.view.ui_edit_url.setText(self.view.ui_cef.url())

    def setupCefTimer(self):
        """启动 CEF 更新定时器"""
        self.timer_cef = QTimer()
        # noinspection PyUnresolvedReferences
        self.timer_cef.timeout.connect(self.onRunCef)
        self.timer_cef.start(CefModel.MS_CEF)

    def setupReadingTimer(self):
        """启动阅读器更新定时器"""
        self.timer_reading = QTimer()
        # noinspection PyUnresolvedReferences
        self.timer_reading.timeout.connect(self.onAutoReading)
        self.timer_reading.start(CefModel.MS_AUTO)

    def onRunCef(self):
        """CEF 更新"""
        self.view.ui_cef.runLoop()

    def stopCef(self):
        """停止 CEF 更新"""
        self.timer_reading.stop()
        self.timer_cef.stop()
        self.view.ui_cef.quit()

    def onAutoReading(self):
        """阅读器更新"""
        self.view.ui_cef.doScroll()

    def closeEvent(self, event):
        """关闭事件：停止定时器、关闭 CEF、保存数据"""
        self.stopCef()
        self.view.closeEvent(event)
        super(WindowView, self).closeEvent(event)

    def resizeEvent(self, event):
        """视图尺寸变化事件"""
        self.view.resizeEvent(event)
        super(WindowView, self).resizeEvent(event)

    def onTrayActivated(self, reason: QSystemTrayIcon.ActivationReason):
        """系统托盘图标触发事件"""
        if reason in (QSystemTrayIcon.ActivationReason.DoubleClick,
                      QSystemTrayIcon.ActivationReason.MiddleClick,
                      QSystemTrayIcon.ActivationReason.Trigger):
            self.activateWindow()
            if self.isFullScreen():
                self.showFullScreen()
            else:
                if self.isMaximized():
                    self.showMaximized()
                else:
                    self.showNormal()

    def onToolbarQuit(self):
        """退出阅读"""
        self.close()
        QApplication.exit()

    def onToolbarBackHome(self):
        """回到首页"""
        self.view.ui_cef.doBackHome()

    def onToolbarReload(self):
        """重新加载"""
        self.view.ui_cef.doReload()

    def onToolbarExport(self):
        """导出笔记"""
        self.view.ui_cef.doExport()

    def onToolbarTheme(self):
        """切换主题"""
        self.view.ui_cef.doTheme()

    def onToolbarSetAuto(self):
        """切换自动阅读"""
        self.view.stateful_act_auto.onChanged()
        self.view.ui_cef.doAuto()
        if not self.view.ui_act_auto.isChecked():
            self.refreshStatusTip("")

    def onToolbarFullscreen(self):
        """切换全屏"""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def onToolbarSpeedUp(self):
        """提高速度"""
        self.view.stateful_act_speed_up.onChanged()
        self.view.ui_cef.doSpeed()
        self.refreshSpeed()

    def onToolbarSpeedDown(self):
        """降低速度"""
        self.view.stateful_act_speed_dw.onChanged()
        self.view.ui_cef.doSpeed()
        self.refreshSpeed()

    def onToolbarPinned(self):
        """收起工具栏"""
        self.view.stateful_act_pinned.onChanged()

    @staticmethod
    def onToolbarSponsor():
        """打开赞助视图"""
        SponsorView().exec()

    @staticmethod
    def onToolbarHelp():
        """打开帮助视图"""
        NoticeView(Views.Help,
                   UserKey.Help.WinRect,
                   I18n.text(LanguageKeys.toolbar_help),
                   Cmm.readFile(ResMap.html_help),
                   ContentFillType.Html
                   ).exec()

    @staticmethod
    def onToolbarAbout():
        """打开关于视图"""
        NoticeView(Views.About,
                   UserKey.About.WinRect,
                   I18n.text(LanguageKeys.toolbar_about),
                   Cmm.readFile(ResMap.html_about),
                   ContentFillType.Html
                   ).exec()

    @staticmethod
    def onToolbarProfile():
        """打开选项视图"""
        OptionsView().exec()
