# -*- coding: utf-8 -*-

"""
@File    : WindowModel.py
@Time    : 2022/10/8 16:55
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : PyCharm
"""
from typing import List

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QEvent, QFile, QIODevice, QObject
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineProfile, QWebEngineScript, QWebEngineView

from conf.ResMap import ResMap
from helper.Preferences import Preferences, UserKey
from helper.Signals import Signals


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

    def __init__(self, name: str):
        super(PjTransport, self).__init__()
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


class JsScriptInfo:
    def __init__(self, name: str, where: str):
        self.name = name
        self.where = where


class WebHelper:
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
    def newWebPage(profile_name: str, scripts: List[JsScriptInfo], transport: PjTransport,
                   webview: QWebEngineView):
        web_profile = QWebEngineProfile(profile_name, webview)
        web_profile.scripts().clear()
        [WebHelper.injectJsToPage(script.where, script.name, web_profile) for script in scripts]
        web_page = QWebEnginePage(web_profile, webview)
        web_channel = QWebChannel(web_page)
        web_channel.registerObject(transport.name, transport)
        web_page.setWebChannel(web_channel)
        webview.setPage(web_page)


class WindowModel:
    # 工具栏高度
    TOOLBAR_HEIGHT = 53

    # 工具栏显示偏移值
    TOOLBAR_MOUSE_OFFSET_Y = 10

    # 阅读器刷新频率
    READER_TIMER_INTERVAL = 100

    # 阅读器最小速度
    READER_MIN_SPEED = 1

    # 阅读器最大速度
    READER_MAX_SPEED = 100

    # 鼠标移动事件
    MOUSE_EVENT = [
        QEvent.MouseMove,
        QEvent.MouseTrackingChange,
        QEvent.NonClientAreaMouseMove,
        QEvent.Move,
        QEvent.HoverMove,
        QEvent.DragMove,
    ]

    # 主页网址
    HOME_PAGE = 'https://weread.qq.com/'

    # 阅读页网址
    BOOK_PAGE = "https://weread.qq.com/web/reader/"

    # 内置 WebContent 脚本的存放位置
    BUILTIN_SCRIPT = ":/qtwebchannel/qwebchannel.js"

    # 网页配置的名称
    DEFAULT_PAGE_PROFILE = "WxReader.Default"

    # WebContent 中使用的对象名称
    PJ_TRANSPORT = "pjTransport"

    def __init__(self):
        self._reader_timer_id = -1
        self.wait_next = False
        self.pjTransport = PjTransport(WindowModel.PJ_TRANSPORT)

    @staticmethod
    def scripts():
        return [JsScriptInfo("WebContent", WindowModel.BUILTIN_SCRIPT), JsScriptInfo("WxReader", ResMap.js_reader)]

    def timerId(self):
        return self._reader_timer_id

    def setTimerId(self, tid: int):
        self._reader_timer_id = tid

    def clearTimerId(self):
        self._reader_timer_id = -1

    def isValidTimer(self):
        return self._reader_timer_id > -1

    def nextSpeed(self, speed_up: bool):
        step = self.step()
        speed = self.speed() + step * (1 if speed_up else -1)
        return self.checkSpeed(speed)

    @staticmethod
    def checkSpeed(speed):
        return min(WindowModel.READER_MAX_SPEED, max(WindowModel.READER_MIN_SPEED, speed))

    @staticmethod
    def scrollable():
        return Preferences().get(UserKey.Reader.Scrollable)

    @staticmethod
    def latestUrl():
        return Preferences().get(UserKey.Reader.LatestUrl)

    @staticmethod
    def pinned():
        return Preferences().get(UserKey.Reader.Pinned)

    @staticmethod
    def step():
        return Preferences().get(UserKey.Reader.Step)

    @staticmethod
    def speed():
        return Preferences().get(UserKey.Reader.Speed)

    @staticmethod
    def setScrollable(scrollable: bool):
        Preferences().set(UserKey.Reader.Scrollable, scrollable)

    @staticmethod
    def setPinned(pinned: bool):
        Preferences().set(UserKey.Reader.Pinned, pinned)

    @staticmethod
    def setLatestUrl(url: str):
        Preferences().set(UserKey.Reader.LatestUrl, url)

    @staticmethod
    def setStep(step: int):
        step = min(10, min(1, step))
        Preferences().set(UserKey.Reader.Step, step)

    @staticmethod
    def setSpeed(speed: int):
        Preferences().set(UserKey.Reader.Speed, WindowModel.checkSpeed(speed))

    @staticmethod
    def saveAll():
        Preferences().save()

    @staticmethod
    def checkToolbarHeight(current_height: int, mouse_pos_y: int):
        hidden = current_height == 0
        inside = (mouse_pos_y <= WindowModel.TOOLBAR_MOUSE_OFFSET_Y) if hidden else (
                mouse_pos_y <= WindowModel.TOOLBAR_HEIGHT)
        return WindowModel.TOOLBAR_HEIGHT if inside else 0

    @staticmethod
    def isMouseEvent(et: int):
        return et in WindowModel.MOUSE_EVENT
