# -*- coding: utf-8 -*-

"""
@File    : lang.py
@Time    : 2022/9/27 16:20
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 语言包
  - 可以根据需要配置语言包
"""

from enum import Enum, unique


class _Languages:
    """
    语言包列表
    """
    CN = {
        # general
        "app:name": "微读自动阅读器",

        # main menu
        "main_menu:file": "更多",
        "main_menu:file:help": "帮助",
        "main_menu:file:about": "关于",
        "main_menu:file:profile": "选项",
        "main_menu:file:quit": "退出",

        # toolbar
        "toolbar:auto": "自动阅读",
        "toolbar:export": "导出笔记",
        "toolbar:theme": "切换主题",
        "toolbar:fullscreen": "切换全屏",
        "toolbar:back_home": "回到首页",
        "toolbar:speed_up": "加速",
        "toolbar:speed_dw": "减速",

        # debug
        "debug:method_not_implemented": "[ {0} > {1} ] 方法未实现",
    }


@unique
class LangPack(Enum):
    """语言包可选项"""
    CN = _Languages.CN