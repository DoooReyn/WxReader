# -*- coding: utf-8 -*-

"""
@File    : Preferences.py
@Time    : 2022/9/27 15:46
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 软件配置
"""
from json import dumps, JSONDecodeError, loads
from os.path import exists

# QSettings 存在读取和保存无效的问题，自己写一个来代替
from helper.Cmm import Cmm


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

    class Timing:
        WinRect = 'timing.win_rect'
        EveryDay = 'timing.every_day'
        StartTime = 'timing.start_time'
        StopTime = 'timing.stop_time'



# 默认用户存储数据
default_user_data = {
    UserKey.Reader.Speed: 1,
    UserKey.Reader.Step: 1,
    UserKey.Reader.Scrollable: False,
    UserKey.Reader.Pinned: True,
    UserKey.Reader.LatestUrl: 'https://weread.qq.com/',
    UserKey.General.Lang: 'CN',
    UserKey.General.WinRect: [640, 480, 640, 480],
    UserKey.Profile.WinRect: [640, 480, 640, 480],
    UserKey.About.WinRect: [640, 480, 640, 480],
    UserKey.Help.WinRect: [640, 480, 640, 480],
    UserKey.Exception.WinRect: [640, 480, 640, 480],
    UserKey.Sponsor.WinRect: [640, 480, 640, 480],
    UserKey.ReadingFinished.WinRect: [640, 480, 640, 480],
    UserKey.Profile.NoticeUrl: '',
    UserKey.Timing.WinRect: [640,480,640,480],    
    UserKey.Timing.EveryDay : False,
    UserKey.Timing.StartTime: 0,
    UserKey.Timing.StopTime: 0
}


@Cmm.Decorator.Singleton
class Preferences:
    """用户存储管理器"""

    def __init__(self):
        self._data = {}
        self.config_at = Cmm.appConfigAt()

    def init(self):
        """初始化：创建配置、读取数据到内存"""
        Cmm.mkdir(Cmm.appStorageAt())
        self._read()

    def _read(self):
        """读取数据到内存"""
        if exists(self.config_at):
            try:
                with open(self.config_at, 'r', encoding='utf-8') as f:
                    self._data = loads(f.read())
                    self._sync()
            except JSONDecodeError:
                self._saveDefault()
        else:
            self._saveDefault()

    def _saveDefault(self):
        """保存默认数据"""
        self._data = default_user_data
        self.save()

    def _sync(self):
        """数据同步"""
        for k, v in default_user_data.items():
            if self._data.get(k) is None:
                self._data.setdefault(k, v)

    def save(self):
        """保存数据"""
        with open(self.config_at, 'w', encoding='utf-8') as f:
            f.write(dumps(self._data, indent=2))

    def get(self, key: str):
        """获取数据"""
        return self._data[key]

    def set(self, key: str, value):
        """修改数据"""
        self._data[key] = value
        self.save()


gPreferences = Preferences()
