# -*- coding: utf-8 -*-

"""
@File    : BadNotice.py
@Time    : 2022/9/30 22:12
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 错误通知
"""
from PyQt5.QtCore import Qt

from conf.Lang import LanguageKeys
from conf.Views import Views
from helper.I18n import I18n
from helper.Preferences import UserKey
from ui.view.Notice import FillType, Notice


class BadNotice(Notice):
    """错误通知"""

    def __init__(self, tips: str):
        super(BadNotice, self).__init__(
            Views.Exception,
            UserKey.Exception.WinRect,
            I18n.text(LanguageKeys.exception_name),
            tips,
            FillType.PlainText,
            True
        )
        self.setMinimumSize(320, 240)


class NetworkBadNotice(BadNotice):
    """网络错误通知"""

    def __init__(self):
        tips = I18n.text(LanguageKeys.debug_network_error)
        super(NetworkBadNotice, self).__init__(tips)


class InjectBadNotice(BadNotice):
    """注入脚本失败通知"""

    def __init__(self, filepath: str):
        tips = I18n.text(LanguageKeys.debug_inject_script_failed).format(filepath)
        super(InjectBadNotice, self).__init__(tips)


class ReadingFinishedNotice(Notice):
    """全文完通知"""

    def __init__(self):
        super(ReadingFinishedNotice, self).__init__(
            Views.ReadingFinished,
            UserKey.ReadingFinished.WinRect,
            I18n.text(LanguageKeys.tips_notice),
            I18n.text(LanguageKeys.tips_reading_finished),
            FillType.PlainText,
            True
        )

        self.setFixedSize(320, 80)

        font = self.ui_msg_box.font()
        font.setBold(True)
        font.setPointSize(16)
        self.ui_msg_box.setFont(font)
        self.ui_msg_box.setAlignment(Qt.AlignCenter)
        self.ui_msg_box.document().setDocumentMargin(10)
        self.ui_msg_box.setFixedHeight(int(self.ui_msg_box.document().size().height()))
