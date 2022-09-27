# -*- coding: utf-8 -*-

"""
@File    : menus.py
@Time    : 2022/9/27 17:07
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 菜单
"""

from conf.res_map import ResMap


class ActionInfo:
    """动作"""
    def __init__(self, name: str, icon: str = None, trigger: str = None, shortcut: str = None):
        self.name = name
        self.icon = icon
        self.trigger = trigger
        self.shortcut = shortcut


class MainMenu:
    """菜单栏"""
    class More:
        Name = 'main_menu:more'
        ActionHelp = ActionInfo('main_menu:more:help', ResMap.icon_help, 'on_main_menu_help', 'F1')
        ActionAbout = ActionInfo('main_menu:more:about', ResMap.icon_brand_github, 'on_main_menu_about', 'F2')
        ActionProfile = ActionInfo('main_menu:more:profile', ResMap.icon_settings, 'on_main_menu_profile', 'F12')
        ActionQuit = ActionInfo('main_menu:more:quit', ResMap.icon_logout, 'on_main_menu_quit', 'Alt+Q')


class MainToolbar:
    """工具栏"""
    ActionBackHome = ActionInfo('toolbar:back_home', ResMap.icon_home_heart, 'on_toolbar_back_home', 'F5')
    ActionExport = ActionInfo('toolbar:export', ResMap.icon_markdown, 'on_toolbar_export', 'F8')
    ActionTheme = ActionInfo('toolbar:theme', ResMap.icon_sun, 'on_toolbar_theme', 'F9')
    ActionAuto = ActionInfo('toolbar:auto', ResMap.icon_player_play, 'on_toolbar_set_auto', 'F10')
    ActionFullscreen = ActionInfo('toolbar:fullscreen', ResMap.icon_arrows_maximize, 'on_toolbar_fullscreen', 'F11')
    ActionSpeedUp = ActionInfo('toolbar:speed_up', ResMap.icon_plus, 'on_toolbar_speed_up', '+')
    ActionSpeedDw = ActionInfo('toolbar:speed_dw', ResMap.icon_minus, 'on_toolbar_speed_dw', '-')
    ActionSponsor = ActionInfo('toolbar:sponsor', ResMap.icon_coffee, 'on_toolbar_sponsor', '-')


class MainTray:
    """系统托盘"""
    ActionQuit = ActionInfo('main_menu:more:quit', ResMap.icon_logout, 'on_main_menu_quit')
