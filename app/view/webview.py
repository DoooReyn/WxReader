# -*- coding: utf-8 -*-

"""
@File    : webview.py
@Time    : 2022/9/28 15:28
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 微信读书网页视图
@Todo    :
    - ":/qtwebchannel/qwebchannel.js" 要用 QFile去读取，可将其放入 qrc 中
    - QWebEngineProfile 要指定名称
    - QWebEnginePage 要指定 QWebEngineProfile
    - QWebChannel 要关联到 QWebEnginePage
    - 最后，QWebEngineView 要指定 QWebEnginePage
    - 微信读书网页版设定了开启开发者工具就会触发断点，可以在调试面板禁用所有断点
"""
from typing import Callable

from PyQt5.QtCore import pyqtSignal as QSignal, pyqtSlot, QFile, QIODevice, QObject, QUrl
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineProfile, QWebEngineScript, QWebEngineView

from conf.res_map import ResMap
from conf.user_key import UserKey
from conf.views import Views
from helper.gui import GUI
from helper.i18n import I18n
from helper.preferences import Preferences
from helper.signals import Signals
from view.notice import FillType, Notice


class ReaderActions:
    """阅读器动作"""
    BackHome = 0
    Refresh = 1
    Scrollable = 2
    SpeedDown = 3
    SpeedUp = 4
    ExportNote = 5
    NextTheme = 6
    WatchSelection = 11
    Scrolling = 12
    CheckLoading = 13


class PjTransport(QObject):
    """Python/JS 消息交换中心"""

    # Python 调用 JS
    p2j = QSignal(int)

    def __init__(self):
        super(PjTransport, self).__init__()
        self.has_selection = False
        self.scroll_to_end = False
        self.loading = False

    # JS 调用 Python
    @pyqtSlot(str)
    def j2p(self, msg):
        # print('Python 收到消息:', msg)
        pass

    @pyqtSlot(int)
    def setSelection(self, has):
        self.has_selection = has == 1
        # print('有选中' if self.has_selection else '无选中')

    @pyqtSlot(int)
    def setScrollToEnd(self, end):
        self.scroll_to_end = end == 1
        # print('已滚动到底部' if self.scroll_to_end else '还没滚到底')

    @pyqtSlot(int)
    def setPageLoading(self, loading):
        self.loading = loading == 1
        # print('页面加载中' if self.loading else '页面已加载')

    def trigger(self, act: int):
        # noinspection PyUnresolvedReferences
        self.p2j.emit(act)


class Webview(QWebEngineView, GUI.View):
    """微信读书网页视图"""

    # 主页网址
    HOME_PAGE = 'https://weread.qq.com/'

    # 阅读页网址
    BOOK_PAGE = "https://weread.qq.com/web/reader/"

    # 内置 WebContent 脚本的存放位置
    SCRIPT_WEB_CONTENT = ":/qtwebchannel/qwebchannel.js"

    # 网页配置的名称
    PROFILE = "WxReader"

    # WebContent 中使用的对象名称
    PJ_TRANSPORT = "pjTransport"

    def __init__(self):
        super(Webview, self).__init__()

        self.wait_next = False
        self.profile = QWebEngineProfile(Webview.PROFILE, self)
        self.inject_js_script(Webview.SCRIPT_WEB_CONTENT, "WebContent")
        self.inject_js_script(ResMap.js_reader, "WxReader")
        self.webpage = QWebEnginePage(self.profile, self)
        self.channel = QWebChannel(self.webpage)
        self.pjTransport = PjTransport()
        self.channel.registerObject(Webview.PJ_TRANSPORT, self.pjTransport)
        self.webpage.setWebChannel(self.channel)
        self.setPage(self.webpage)
        self.setup_signals()
        self.restore_latest_page()

    def inject_js_script(self, filepath: str, name: str):
        """注入JS脚本"""
        js = QFile(filepath)
        if js.open(QIODevice.ReadOnly) is True:
            source = js.readAll().data().decode('utf-8')
            script = QWebEngineScript()
            script.setName(name)
            script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
            script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentReady)
            script.setRunsOnSubFrames(True)
            script.setSourceCode(source)
            self.profile.scripts().insert(script)
        else:
            Notice(
                Views.Exception,
                UserKey.General.Exception,
                I18n.text("exception:name"),
                I18n.text("debug:inject_script_failed").format(filepath),
                FillType.PlainText,
                True
            ).exec()

    def setup_signals(self):
        self.loadStarted.connect(self._on_load_started)
        self.loadFinished.connect(self._on_load_finished)
        self.urlChanged.connect(self._on_url_changed)
        Signals().reader_setting_changed.connect(self._on_reader_action_triggered)

    def restore_latest_page(self):
        page = Preferences.storage.value(UserKey.Reader.LatestUrl, Webview.HOME_PAGE, str)
        self.goto_page(page)

    def goto_page(self, url: str):
        self.load(QUrl(url))

    def go_home(self):
        self.goto_page(Webview.HOME_PAGE)

    def is_on_reading_page(self):
        url = self.current_url()
        return url.startswith(Webview.BOOK_PAGE)

    def run_js(self, script: str, callback: Callable = None):
        def _pass(_):
            pass

        callback = callback or _pass
        self.page().runJavaScript(script, callback)

    def check_scroll(self):
        self.pjTransport.trigger(ReaderActions.CheckLoading)
        if self.pjTransport.loading:
            print("页面加载中")
            return
        else:
            if self.wait_next is True:
                self.pjTransport.trigger(ReaderActions.WatchSelection)
                self.wait_next = False
                print("下一章加载完成")
                return
        if self.pjTransport.has_selection is True:
            print("有选中文本")
            return
        if self.wait_next is True:
            print("等待跳转下一章")
            return
        if self.pjTransport.scroll_to_end is True:
            print("滚动到底部了")
            self.pjTransport.scroll_to_end = False
            self.wait_next = True
            return
        if self.is_on_reading_page() is False:
            print("不在阅读页面")
            return
        self.pjTransport.trigger(ReaderActions.Scrolling)

    def _on_reader_action_triggered(self, act: int):
        if act == ReaderActions.BackHome:
            self.go_home()
            return
        elif act == ReaderActions.Refresh:
            self.goto_page(self.webpage.url())
            return

        if self.is_on_reading_page():
            self.pjTransport.trigger(act)

    def current_url(self):
        return self.page().url().toString()

    def _on_load_started(self):
        print('[开始加载]', self.current_url())
        self.pjTransport.scroll_to_end = False
        self.pjTransport.has_selection = False
        self.pjTransport.trigger(ReaderActions.WatchSelection)

    def _on_load_finished(self, result: bool):
        self._on_load_finished_ok() if result else self._on_load_finished_bad()

    def _on_load_finished_ok(self):
        print('[加载完成]', self.current_url())
        self.pjTransport.trigger(ReaderActions.WatchSelection)

    def _on_load_finished_bad(self):
        print('[加载失败]', self.current_url())
        Notice(
            Views.Exception,
            UserKey.General.Exception,
            I18n.text("exception:name"),
            I18n.text("debug:network_error"),
            FillType.PlainText,
            True
        ).exec()

    def _on_url_changed(self, url: QUrl):
        print('[页面切换]', url.toString())
