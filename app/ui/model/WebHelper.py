# -*- coding: utf-8 -*-

"""
@File    : WebHelper.py
@Time    : 2022/10/9 15:12
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 网页交互辅助工具
"""
from typing import List

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QFile, QIODevice, QObject
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineProfile, QWebEngineScript, QWebEngineView

from helper.Preferences import Preferences, UserKey
from helper.Signals import Signals
from ui.model.ReaderHelper import ReaderActions


class PjTransport(QObject):
    """Python/JS 消息交换中心"""

    def __init__(self, name: str):
        super(PjTransport, self).__init__()
        # 注册名称
        self.name = name
        # 页面是否有选中内容
        self.has_selection = False
        # 页面是否已滚动到底部
        self.scroll_to_end = False
        # 页面是否正在加载中
        self.loading = False

    # Python 调用 JS
    p2j = pyqtSignal(int)

    @pyqtSlot(str)
    def j2p(self, msg):
        """js 给 python 发消息，方便测试"""
        print('j2p:', msg)
        # Signals().reader_status_tip_updated.emit(msg)

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


class JsScriptInfo:
    """JS脚本信息"""
    def __init__(self, name: str, where: str):
        """
        JS脚本注册信息

        :param name: 注册名称
        :param where: 文件位置
        """
        self.name = name
        self.where = where


class WebHelper:
    """Web辅助工具类"""

    @staticmethod
    def injectJsToPage(filepath: str, name: str, profile: QWebEngineProfile):
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
            profile.scripts().insert(script)

    @staticmethod
    def newWebPage(profile_name: str,
                   scripts: List[JsScriptInfo],
                   transport: PjTransport,
                   webview: QWebEngineView):
        """新建web页面"""
        web_profile = QWebEngineProfile(profile_name, webview)
        web_profile.scripts().clear()
        [WebHelper.injectJsToPage(script.where, script.name, web_profile) for script in scripts]
        web_page = QWebEnginePage(web_profile, webview)
        web_channel = QWebChannel(web_page)
        web_channel.registerObject(transport.name, transport)
        web_page.setWebChannel(web_channel)
        webview.setPage(web_page)
