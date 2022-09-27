# -*- coding: utf-8 -*-

"""
@File    : menus.py
@Time    : 2022/9/27 17:07
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 菜单
"""

from res_map import ResMap


class _MenuInfo:
    def __init__(self, name: str, icon: str = None, trigger: str = None, shortcut: str = None):
        self.name = name
        self.icon = icon
        self.trigger = trigger
        self.shortcut = shortcut


class MainMenu:
    class File:
        Name = 'main_menu:file'
        Actions = (
            _MenuInfo('main_menu:file:help', ResMap.icon_app, 'on_main_menu_help', 'F1'),
            _MenuInfo('main_menu:file:about', ResMap.icon_app, 'on_main_menu_about', 'F2'),
            _MenuInfo('main_menu:file:fullscreen', ResMap.icon_app, 'on_main_menu_fullscreen', 'F11'),
            _MenuInfo('main_menu:file:profile', ResMap.icon_app, 'on_main_menu_profile', 'F12'),
            _MenuInfo('main_menu:file:quit', ResMap.icon_app, 'on_main_menu_quit', 'Alt+Escape'),
        )
