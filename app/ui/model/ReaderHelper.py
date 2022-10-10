# -*- coding: utf-8 -*-

"""
@File    : ReaderHelper.py
@Time    : 2022/10/9 15:11
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 阅读器辅助工具
"""


class ReaderActions:
    """阅读器动作"""

    # 回到首页
    BackHome = 0

    # 刷新页面
    Refresh = 1

    # 切换自动阅读
    Scrollable = 2

    # 降低滚动速度
    SpeedDown = 3

    # 加快滚动速度
    SpeedUp = 4

    # 导出笔记
    ExportNote = 5

    # 切换主题
    NextTheme = 6

    # 启用页面选中状态监听
    Watching = 11

    # 启用页面滚动状态监听
    Scrolling = 12

    # 启用页面加载状态监听
    Loading = 13

    # 关闭自动阅读
    ScrollableOff = 20

    # 开启自动阅读
    ScrollableOn = 21
