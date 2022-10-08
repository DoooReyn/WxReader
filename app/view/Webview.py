# -*- coding: utf-8 -*-

"""
@File    : Webview.py
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
from PyQt5.QtWidgets import QFileDialog

from conf.Lang import LanguageKeys
from conf.ResMap import ResMap
from helper.Cmm import Cmm
from helper.Gui import GUI
from helper.I18n import I18n
from helper.Preferences import Preferences, UserKey
from helper.Signals import Signals
from view.BadNotice import InjectBadNotice, NetworkBadNotice


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
        Signals().reader_status_tip_updated.emit(msg)

    @pyqtSlot()
    def readingFinished(self):
        """全书已读完"""
        Signals().reader_reading_finished.emit()

    @pyqtSlot(str, str)
    def downloadNote(self, filename, content):
        """下载笔记"""
        Signals().reader_download_note.emit(filename, content)

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

    def refreshSpeed(self):
        """刷新页面滚动速度"""
        # noinspection PyUnresolvedReferences
        self.trigger(1000 + Preferences().get(UserKey.Reader.Speed))

    def refreshScrollable(self):
        """刷新自动阅读状态"""
        scrollable = Preferences().get(UserKey.Reader.Scrollable)
        code = ReaderActions.ScrollableOn if scrollable else ReaderActions.ScrollableOff
        self.trigger(code)

    def applyWatch(self):
        """应用滚动、选中监听"""
        self.trigger(ReaderActions.Watching)


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
        self.injectJsScript(Webview.SCRIPT_WEB_CONTENT, "WebContent")
        self.injectJsScript(ResMap.js_reader, "WxReader")
        self.webpage = QWebEnginePage(self.profile, self)
        self.channel = QWebChannel(self.webpage)
        self.pjTransport = PjTransport()
        self.channel.registerObject(Webview.PJ_TRANSPORT, self.pjTransport)
        self.webpage.setWebChannel(self.channel)
        self.setPage(self.webpage)
        self.setupSignals()
        self.restoreLatestPage()

    def injectJsScript(self, filepath: str, name: str):
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
            InjectBadNotice(filepath).exec()

    def setupSignals(self):
        self.loadStarted.connect(self.onLoadStarted)
        self.loadProgress.connect(self.onLoadProgress)
        self.loadFinished.connect(self.onLoadFinished)
        Signals().reader_setting_changed.connect(self.onReaderActionTriggered)
        Signals().reader_download_note.connect(self.onSaveNote)
        Signals().reader_reading_finished.connect(self.onReadingFinished)

    def restoreLatestPage(self):
        self.goToPage(Preferences().get(UserKey.Reader.LatestUrl))

    def goToPage(self, url: str):
        self.load(QUrl(url))

    def goToHome(self):
        self.goToPage(Webview.HOME_PAGE)

    def isReadingPage(self):
        url = self.currentUrl()
        return url.startswith(Webview.BOOK_PAGE)

    def checkScroll(self):
        self.pjTransport.trigger(ReaderActions.Loading)
        if self.pjTransport.loading:
            self.sendTip(I18n.text(LanguageKeys.tips_page_ready))
            return
        else:
            if self.wait_next is True:
                self.pjTransport.applyWatch()
                self.wait_next = False
                self.sendTip(I18n.text(LanguageKeys.tips_next_chapter_ready))
                return
        if self.pjTransport.has_selection is True:
            self.sendTip(I18n.text(LanguageKeys.tips_has_selection))
            return
        if self.wait_next is True:
            self.sendTip(I18n.text(LanguageKeys.tips_wait_for_next_chapter))
            return
        if self.pjTransport.scroll_to_end is True:
            self.sendTip(I18n.text(LanguageKeys.tips_scroll_to_end))
            self.pjTransport.scroll_to_end = False
            self.wait_next = True
            return
        if self.isReadingPage() is False:
            self.sendTip(I18n.text(LanguageKeys.tips_no_book_view))
            return

        self.sendTip(I18n.text(LanguageKeys.tips_auto_read_on), False)
        Signals().reader_load_progress.emit(0)
        self.pjTransport.trigger(ReaderActions.Scrolling)

    def onReaderActionTriggered(self, act: int):
        if act == ReaderActions.BackHome:
            self.goToHome()
            return
        elif act == ReaderActions.Refresh:
            self.goToPage(self.webpage.url())
            return
        elif act == ReaderActions.SpeedDown or act == ReaderActions.SpeedUp:
            self.pjTransport.refreshSpeed()
            return
        elif act == ReaderActions.Scrollable:
            self.pjTransport.refreshScrollable()
            return

        if self.isReadingPage():
            self.pjTransport.trigger(act)

    def onSaveNote(self, filename: str, content: str):
        where, _ = QFileDialog.getSaveFileName(self, I18n.text(LanguageKeys.tips_export_note), filename, filter='*.md')
        if len(where) > 0:
            Cmm.saveAs(where, content)
            self.sendTip(I18n.text(LanguageKeys.tips_note_exported_ok).format(filename))
        else:
            self.sendTip(I18n.text(LanguageKeys.tips_note_exported_bad).format(filename))

    @staticmethod
    def onReadingFinished():
        # ReadingFinishedNotice().exec()
        pass

    def currentUrl(self):
        return self.page().url().toString()

    def sendTip(self, tip: str, output: bool = True):
        if output:
            print(tip, self.currentUrl())
        Signals().reader_status_tip_updated.emit(tip)

    def onLoadStarted(self):
        self.sendTip(I18n.text(LanguageKeys.tips_page_ready))
        self.pjTransport.scroll_to_end = False
        self.pjTransport.has_selection = False
        self.pjTransport.applyWatch()

    def onLoadProgress(self, value):
        self.sendTip(I18n.text(LanguageKeys.tips_page_loading))
        Signals().reader_load_progress.emit(value)

    def onLoadFinished(self, result: bool):
        if result:
            self.pjTransport.applyWatch()
            self.pjTransport.refreshSpeed()
            self.pjTransport.refreshScrollable()
            Signals().reader_load_progress.emit(0)
            self.sendTip(I18n.text(LanguageKeys.tips_page_loaded_ok))
        else:
            self.sendTip(I18n.text(LanguageKeys.tips_page_loaded_bad))
            NetworkBadNotice().exec()