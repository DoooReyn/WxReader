# -*- coding: utf-8 -*-

"""
@File    : webview.py
@Time    : 2022/9/28 15:28
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 微信读书网页视图
"""
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineProfile, QWebEngineView

from conf.user_key import UserKey
from helper.gui import GUI
from helper.preferences import Preferences
from helper.signals import Signals


class ReaderActions:
    BackHome = 0
    Scrollable = 1
    SpeedDown = 2
    SpeedUp = 3
    ExportNote = 4
    NextTheme = 5


class Webview(QWebEngineView, GUI.View):
    HOME_PAGE = 'https://weread.qq.com/'
    BOOK_PAGE = "https://weread.qq.com/web/reader/"

    def __init__(self):
        super(Webview, self).__init__()

        self.profile = QWebEngineProfile.defaultProfile()
        self.setup_signals()
        self.restore_latest_page()

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

    def _on_reader_action_triggered(self, act: int):
        if act == ReaderActions.BackHome:
            self.go_home()
            return
        if self.is_on_reading_page():
            if act == ReaderActions.Scrollable:
                pass
            elif act == ReaderActions.SpeedDown:
                pass
            elif act == ReaderActions.SpeedUp:
                pass
            elif act == ReaderActions.ExportNote:
                pass
            elif act == ReaderActions.NextTheme:
                pass

    def current_url(self):
        return self.page().url().toString()

    def _on_load_started(self):
        print('load started', self.current_url())

    def _on_load_finished(self, result: bool):
        self._on_load_finished_ok() if result else self._on_load_finished_bad()

    def _on_load_finished_ok(self):
        print('load finished ok', self.current_url())

    def _on_load_finished_bad(self):
        print('load finished bad', self.current_url())

    def _on_url_changed(self, url: QUrl):
        print('url changed', self.current_url(), url.toString())
