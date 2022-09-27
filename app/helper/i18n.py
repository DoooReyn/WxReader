# -*- coding: utf-8 -*-

"""
@File    : i18n.py
@Time    : 2022/9/27 17:15
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 多语言
"""
from conf.lang import LangPack
from conf.user_key import UserKey
from helper.preferences import Preferences
from helper.signals import Signals


class I18n:
    """语言包管理器"""

    @staticmethod
    def get_lang():
        """当前语言"""
        return Preferences.storage.value(UserKey.General.Lang, LangPack.CN.name, str)

    @staticmethod
    def set_lang(pack: LangPack):
        """切换语言"""
        if I18n.get_lang() != pack.name:
            Preferences.storage.setValue(UserKey.General.Lang, pack.name)
            # 语言包切换信号触发
            Signals().lang_changed.emit(pack.name)

    @staticmethod
    def text(key: str):
        """获取语言对应文本"""
        pack = LangPack[I18n.get_lang()].value
        return pack.get(key, '__unknown__')
