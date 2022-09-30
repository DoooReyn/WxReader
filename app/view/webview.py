# -*- coding: utf-8 -*-

"""
@File    : webview.py
@Time    : 2022/9/28 15:28
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 微信读书网页视图
    - 初始化这个Web引擎比较复杂，具体有如下几个要求，缺一不可：
        - QWebEngineProfile 要指定名称
        - QWebEngineScript 要先准备好，再注入 QWebEngineProfile
            - `qwebchannel.js` 是 Qt 内置的，要用 QFile 去读取，再转换为 QWebEngineScript
            - 用户脚本可以放到 qrc 中，再转换为 QWebEngineScript
        - QWebEnginePage 要指定 QWebEngineProfile
        - QWebChannel 要关联到 QWebEnginePage
            - QWebChannel 要关联信号对象，其名称将被注册到 JavaScript 中的 QWebChannel 对象上
            - 利用信号可以让 Python 发消息给 JavaScript
            - JavaScript 可以调用 Python 信号对象上的槽方法，不过要注意参数一定要对应，否则是不会生效的
        - QWebEngineView 要指定 QWebEnginePage，之后的操作就都在这个页面对象上了
    - 微信读书网页版设定了开启开发者工具就会触发断点，可以在调试面板禁用所有断点
"""

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QFile, QIODevice, QObject, QUrl
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


class PjTransport(QObject):
    """Python/JS 消息交换中心"""

    # Python 调用 JS
    p2j = pyqtSignal(int)

    def __init__(self):
        super(PjTransport, self).__init__()
        # 页面是否有选中内容
        self.has_selection = False
        # 页面是否已滚动到底部
        self.scroll_to_end = False
        # 页面是否正在加载中
        self.loading = False

    @pyqtSlot(str)
    def j2p(self, msg):
        """js 给 python 发消息，方便测试"""
        print('Python 收到消息:', msg)
        Signals().status_tip_updated.emit(msg)
        pass

    @pyqtSlot(int)
    def setSelection(self, has):
        """设置页面是否有选中内容"""
        self.has_selection = has == 1

    @pyqtSlot(int)
    def setScrollToEnd(self, end):
        """设置页面是否已滚动到底部"""
        self.scroll_to_end = end == 1

    @pyqtSlot(int)
    def setPageLoading(self, loading):
        """设置页面是否正在加载中"""
        self.loading = loading == 1

    def trigger(self, act: int):
        """触发阅读器动作"""
        # noinspection PyUnresolvedReferences
        self.p2j.emit(act)

    def refresh_speed(self):
        """刷新页面滚动速度"""
        speed = Preferences.storage.value(UserKey.Reader.Speed, 1, int)
        # noinspection PyUnresolvedReferences
        self.p2j.emit(1000 + speed)


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
        self.loadProgress.connect(self._on_load_progressed)
        self.loadFinished.connect(self._on_load_finished)
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

    def check_scroll(self):
        self.pjTransport.trigger(ReaderActions.Loading)
        if self.pjTransport.loading:
            self.send_tip(I18n.text("tips:page_ready"))
            return
        else:
            if self.wait_next is True:
                self.pjTransport.trigger(ReaderActions.Watching)
                self.wait_next = False
                self.send_tip(I18n.text("tips:next_chapter_ready"))
                return
        if self.pjTransport.has_selection is True:
            self.send_tip(I18n.text("tips:has_selection"))
            return
        if self.wait_next is True:
            self.send_tip(I18n.text("tips:wait_for_next_chapter"))
            return
        if self.pjTransport.scroll_to_end is True:
            self.send_tip(I18n.text("tips:scroll_to_end"))
            self.pjTransport.scroll_to_end = False
            self.wait_next = True
            return
        if self.is_on_reading_page() is False:
            self.send_tip(I18n.text("tips:no_book_view"))
            return
        self.send_tip(I18n.text("tips:auto_read_on"), False)
        Signals().page_loading_progress.emit(0)
        self.pjTransport.trigger(ReaderActions.Scrolling)

    def _on_reader_action_triggered(self, act: int):
        if act == ReaderActions.BackHome:
            self.go_home()
            return
        elif act == ReaderActions.Refresh:
            self.goto_page(self.webpage.url())
            return
        elif act == ReaderActions.SpeedDown or act == ReaderActions.SpeedUp:
            self.pjTransport.refresh_speed()
            return

        if self.is_on_reading_page():
            self.pjTransport.trigger(act)

    def current_url(self):
        return self.page().url().toString()

    def send_tip(self, tip: str, output: bool = True):
        if output:
            print(tip, self.current_url())
        Signals().status_tip_updated.emit(tip)

    def _on_load_started(self):
        self.send_tip(I18n.text("tips:page_ready"))
        self.pjTransport.scroll_to_end = False
        self.pjTransport.has_selection = False
        self.pjTransport.trigger(ReaderActions.Watching)

    def _on_load_progressed(self, value):
        self.send_tip(I18n.text("tips:page_loading"))
        Signals().page_loading_progress.emit(value)

    def _on_load_finished(self, result: bool):
        if result:
            self.pjTransport.trigger(ReaderActions.Watching)
            Signals().reader_setting_changed.emit(ReaderActions.SpeedUp)
            Signals().page_loading_progress.emit(0)
            self.send_tip(I18n.text("tips:page_loaded_ok"))
        else:
            self.send_tip(I18n.text("tips:page_loaded_bad"))
            Notice(
                Views.Exception,
                UserKey.General.Exception,
                I18n.text("exception:name"),
                I18n.text("debug:network_error"),
                FillType.PlainText,
                True
            ).exec()
