# -*- coding: utf-8 -*-

"""
@File    : bad_notice.py
@Time    : 2022/9/30 22:12
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 错误通知
"""
from conf.views import Views
from helper.i18n import I18n
from helper.preferences import UserKey
from view.notice import FillType, Notice


class BadNotice(Notice):
    """错误通知"""

    def __init__(self, tips: str):
        super(BadNotice, self).__init__(
            Views.Exception,
            UserKey.Exception.WinRect,
            I18n.text("exception:name"),
            tips,
            FillType.PlainText,
            True
        )
        self.setMinimumSize(320, 240)


class NetworkBadNotice(BadNotice):
    """网络错误通知"""

    def __init__(self):
        tips = I18n.text("debug:network_error")
        super(NetworkBadNotice, self).__init__(tips)


class InjectBadNotice(BadNotice):
    """注入脚本失败通知"""

    def __init__(self, filepath: str):
        tips = I18n.text("debug:inject_script_failed").format(filepath)
        super(InjectBadNotice, self).__init__(tips)
