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
        "app:name": "微读自动阅读器"
    }


@unique
class LangPack(Enum):
    """语言包可选项"""
    CN = _Languages.CN
