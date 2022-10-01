# -*- coding: utf-8 -*-

"""
@File    : preferences.py
@Time    : 2022/9/27 15:46
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 软件配置
"""
from json import dumps, JSONDecodeError, loads
from os.path import exists

# QSettings 存在读取和保存无效的问题，自己写一个来代替
from helper.cmm import Cmm


class UserKey:
    """用户配置存储项"""

    class General:
        Lang = 'general.i18n_lang'
        WinRect = 'general.win_rect'
        Exception = 'general.exception_panel'

    class Reader:
        Scrollable = 'reader.scrollable'
        Pinned = 'reader.pinned'
        Speed = 'reader.speed'
        Step = 'reader.step'
        LatestUrl = 'reader.latest_url'

    class Help:
        WinRect = 'help.win_rect'

    class About:
        WinRect = 'about.win_rect'

    class Profile:
        WinRect = 'profile.win_rect'
        NoticeUrl = 'profile.notice_url'

    class Sponsor:
        WinRect = 'sponsor.win_rect'

    class Exception:
        WinRect = 'exception.win_rect'

    class ReadingFinished:
        WinRect = 'reading_finished.win_rect'


default_user_data = {
    UserKey.Reader.Speed: 1,
    UserKey.Reader.Step: 1,
    UserKey.Reader.Scrollable: False,
    UserKey.Reader.Pinned: True,
    UserKey.Reader.LatestUrl: 'https://weread.qq.com/',
    UserKey.General.Lang: 'CN',
    UserKey.General.WinRect: [0, 0, 640, 480],
    UserKey.Profile.WinRect: [0, 0, 640, 480],
    UserKey.About.WinRect: [0, 0, 640, 480],
    UserKey.Help.WinRect: [0, 0, 640, 480],
    UserKey.Exception.WinRect: [0, 0, 640, 480],
    UserKey.Sponsor.WinRect: [0, 0, 640, 480],
    UserKey.ReadingFinished.WinRect: [0, 0, 640, 480],
    UserKey.Profile.NoticeUrl: ''
}


@Cmm.Decorator.Singleton
class Preferences:
    def __init__(self):
        self._data = {}
        self.config_at = Cmm.app_config_at()

    def init(self):
        Cmm.mkdir(Cmm.app_storage_at())
        self._read()

    def _read(self):
        if exists(self.config_at):
            try:
                with open(self.config_at, 'r', encoding='utf-8') as f:
                    self._data = loads(f.read())
                    self._sync()
            except JSONDecodeError:
                self._save_default()
        else:
            self._save_default()

    def _save_default(self):
        self._data = default_user_data
        self.save()

    def _sync(self):
        for k, v in default_user_data.items():
            if self._data.get(k) is None:
                self._data.setdefault(k, v)

    def save(self):
        with open(self.config_at, 'w', encoding='utf-8') as f:
            f.write(dumps(self._data, indent=2))

    def get(self, key: str):
        return self._data[key]

    def set(self, key: str, value):
        self._data[key] = value
        self.save()
