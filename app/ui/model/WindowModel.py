# -*- coding: utf-8 -*-

"""
@File    : WindowModel.py
@Time    : 2022/10/8 16:55
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : PyCharm
"""

from PyQt5.QtCore import QEvent

from conf.ResMap import ResMap
from helper.Preferences import Preferences, UserKey
from ui.model.WebHelper import JsScriptInfo


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

    # 内置脚本
    BUILTIN_SCRIPTS = [JsScriptInfo("WebContent", ":/qtwebchannel/qwebchannel.js"),
                       JsScriptInfo("WxReader", ResMap.js_reader)]

    # 网页配置的名称
    BUILTIN_PROFILE = "WxReader.Default"

    def __init__(self):
        self._reader_timer_id = -1
        self._wait_next_chapter = False

    def timerId(self):
        return self._reader_timer_id

    def setTimerId(self, tid: int):
        self._reader_timer_id = tid

    def clearTimerId(self):
        self._reader_timer_id = -1

    def isValidTimer(self):
        return self._reader_timer_id > -1

    def isWaitingNextChapter(self):
        return self._wait_next_chapter

    def setWaitingNextChapter(self, waiting: bool):
        self._wait_next_chapter = waiting

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
