# -*- coding: utf-8 -*-

"""
@File    : menus.py
@Time    : 2022/9/27 17:07
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 菜单
"""

from conf.res_map import ResMap


class ActionInfo:
    def __init__(self, name: str, icon: str = None, trigger: str = None, shortcut: str = None):
        self.name = name
        self.icon = icon
        self.trigger = trigger
        self.shortcut = shortcut


class MainMenu:
    class File:
        Name = 'main_menu:file'
        ActionHelp = ActionInfo('main_menu:file:help', ResMap.icon_app, 'on_main_menu_help', 'F1')
        ActionAbout = ActionInfo('main_menu:file:about', ResMap.icon_app, 'on_main_menu_about', 'F2')
        ActionProfile = ActionInfo('main_menu:file:profile', ResMap.icon_app, 'on_main_menu_profile', 'F12')
        ActionQuit = ActionInfo('main_menu:file:quit', ResMap.icon_app, 'on_main_menu_quit', 'Alt+Q')


class MainToolbar:
    Name = '工具栏'
    ActionBackHome = ActionInfo('toolbar:back_home', ResMap.icon_app, 'on_toolbar_back_home', 'F5')
    ActionExport = ActionInfo('toolbar:export', ResMap.icon_app, 'on_toolbar_export', 'F8')
    ActionTheme = ActionInfo('toolbar:theme', ResMap.icon_app, 'on_toolbar_theme', 'F9')
    ActionAuto = ActionInfo('toolbar:auto', ResMap.icon_app, 'on_toolbar_set_auto', 'F10')
    ActionFullscreen = ActionInfo('toolbar:fullscreen', ResMap.icon_app, 'on_toolbar_fullscreen', 'F11')
    ActionSpeedUp = ActionInfo('toolbar:speed_up', ResMap.icon_app, 'on_toolbar_speed_up', '+')
    ActionSpeedDw = ActionInfo('toolbar:speed_dw', ResMap.icon_app, 'on_toolbar_speed_dw', '-')
