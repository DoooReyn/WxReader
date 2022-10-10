# -*- coding: utf-8 -*-

"""
@File    : Menus.py
@Time    : 2022/9/27 17:07
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 菜单
"""
from conf.Lang import LanguageKeys
from conf.ResMap import ResMap


class ActionInfo:
    """动作"""

    def __init__(self, name: str, icon: str = None, trigger: str = None, shortcut: str = None):
        self.name = name
        self.icon = icon
        self.trigger = trigger
        self.shortcut = shortcut


class MainToolbar:
    """工具栏"""
    ActionQuit = ActionInfo(LanguageKeys.toolbar_quit, ResMap.icon_logout, 'onToolbarQuit', 'Alt+Q')
    ActionHide = ActionInfo(LanguageKeys.toolbar_hide, ResMap.icon_eye_off, 'onToolbarHide', 'Esc')
    ActionHelp = ActionInfo(LanguageKeys.toolbar_help, ResMap.icon_help, 'onToolbarHelp', 'F1')
    ActionAbout = ActionInfo(LanguageKeys.toolbar_about, ResMap.icon_brand_github, 'onToolbarAbout', 'F2')
    ActionProfile = ActionInfo(LanguageKeys.toolbar_profile, ResMap.icon_settings, 'onToolbarProfile', 'F12')
    ActionBackHome = ActionInfo(LanguageKeys.toolbar_back_home, ResMap.icon_home_heart, 'onToolbarBackHome', 'F3')
    ActionRefresh = ActionInfo(LanguageKeys.toolbar_refresh, ResMap.icon_refresh, 'onToolbarReload', 'F5')
    ActionExport = ActionInfo(LanguageKeys.toolbar_export, ResMap.icon_markdown, 'onToolbarExport', 'F8')
    ActionTheme = ActionInfo(LanguageKeys.toolbar_theme, ResMap.icon_sun, 'onToolbarTheme', 'F9')
    ActionAuto = ActionInfo(LanguageKeys.toolbar_auto, ResMap.icon_arrow_autofit_down, 'onToolbarSetAuto', 'F10')
    ActionFullscreen = ActionInfo(LanguageKeys.toolbar_fullscreen, ResMap.icon_arrows_maximize, 'onToolbarFullscreen',
                                  'F11')
    ActionSpeedUp = ActionInfo(LanguageKeys.toolbar_speed_up, ResMap.icon_chevrons_right, 'onToolbarSpeedUp', '=')
    ActionSpeedDw = ActionInfo(LanguageKeys.toolbar_speed_dw, ResMap.icon_chevrons_left, 'onToolbarSpeedDown', '-')
    ActionSponsor = ActionInfo(LanguageKeys.toolbar_sponsor, ResMap.icon_coffee, 'onToolbarSponsor')
    ActionPinned = ActionInfo(LanguageKeys.toolbar_pinned, ResMap.icon_pinned_off, 'onToolbarPinned')


class MainTray:
    """系统托盘"""
    ActionQuit = ActionInfo(LanguageKeys.toolbar_quit, ResMap.icon_logout, 'onToolbarQuit')
