# -*- coding: utf-8 -*-

"""
@File    : I18n.py
@Time    : 2022/9/27 17:15
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 多语言
"""
from conf.Lang import LangPack
from helper.Signals import gSignals
from helper.Preferences import gPreferences, UserKey


class I18n:
    """语言包管理器"""

    @staticmethod
    def getLang():
        """当前语言"""
        return gPreferences.get(UserKey.General.Lang)

    @staticmethod
    def setLang(pack: LangPack):
        """切换语言"""
        if I18n.getLang() != pack.name:
            gPreferences.set(UserKey.General.Lang, pack.name)
            # 语言包切换信号触发
            gSignals.lang_changed.emit(pack.name)

    @staticmethod
    def text(key: str):
        """获取语言对应文本"""
        lang = I18n.getLang()
        pack = LangPack[lang].value
        return pack.get(key, '__unknown__')
