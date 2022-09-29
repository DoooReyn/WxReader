# -*- coding: utf-8 -*-

"""
@File    : user_key.py
@Time    : 2022/9/27 17:11
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 用户配置存储项定义
"""


class UserKey:
    """用户配置存储项"""

    class General:
        Lang = 'general:i18n_lang'
        WinRect = 'general:win_rect'
        Exception = 'general:exception_panel'

    class Reader:
        Scrollable = 'reader:scrollable'
        Pinned = 'reader:pinned'
        Speed = 'reader:speed'
        Step = 'reader:step'
        LatestUrl = 'reader:latest_url'

    class Help:
        WinRect = 'help:win_rect'

    class About:
        WinRect = 'about:win_rect'

    class Profile:
        WinRect = 'profile:win_rect'

    class Sponsor:
        WinRect = 'sponsor:win_rect'
