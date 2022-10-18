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

    def __init__(self, name: str, icon: str = None, trigger: str = None, shortcut: str = None, tooltip: str = None):
        self.name = name
        self.icon = icon
        self.trigger = trigger
        self.shortcut = shortcut
        self.tooltip = tooltip or name


class MainToolbar:
    """工具栏"""
    ActionQuit = ActionInfo(
        name=LanguageKeys.toolbar_quit,
        icon=ResMap.icon_logout,
        trigger='onToolbarQuit',
        shortcut='Alt+Q',
        tooltip=LanguageKeys.tooltip_quit
    )
    ActionHide = ActionInfo(
        name=LanguageKeys.toolbar_hide,
        icon=ResMap.icon_eye_off,
        trigger='onToolbarHide',
        shortcut='Esc',
        tooltip=LanguageKeys.tooltip_hide
    )
    ActionHelp = ActionInfo(
        name=LanguageKeys.toolbar_help,
        icon=ResMap.icon_help,
        trigger='onToolbarHelp',
        shortcut='F1',
        tooltip=LanguageKeys.tooltip_help
    )
    ActionAbout = ActionInfo(
        name=LanguageKeys.toolbar_about,
        icon=ResMap.icon_brand_github,
        trigger='onToolbarAbout',
        shortcut='F2',
        tooltip=LanguageKeys.tooltip_about
    )
    ActionProfile = ActionInfo(
        name=LanguageKeys.toolbar_profile,
        icon=ResMap.icon_settings,
        trigger='onToolbarProfile',
        shortcut='F12',
        tooltip=LanguageKeys.tooltip_profile
    )
    ActionBackHome = ActionInfo(
        name=LanguageKeys.toolbar_back_home,
        icon=ResMap.icon_home_heart,
        trigger='onToolbarBackHome',
        shortcut='F3',
        tooltip=LanguageKeys.tooltip_back_home
    )
    ActionRefresh = ActionInfo(
        name=LanguageKeys.toolbar_refresh,
        icon=ResMap.icon_refresh,
        trigger='onToolbarReload',
        shortcut='F5',
        tooltip=LanguageKeys.tooltip_refresh
    )
    ActionExport = ActionInfo(
        name=LanguageKeys.toolbar_export,
        icon=ResMap.icon_markdown,
        trigger='onToolbarExport',
        shortcut='F8',
        tooltip=LanguageKeys.tooltip_export
    )
    ActionTheme = ActionInfo(
        name=LanguageKeys.toolbar_theme,
        icon=ResMap.icon_sun,
        trigger='onToolbarTheme',
        shortcut='F9',
        tooltip=LanguageKeys.tooltip_theme
    )
    ActionAuto = ActionInfo(
        name=LanguageKeys.toolbar_auto,
        icon=ResMap.icon_arrow_autofit_down,
        trigger='onToolbarSetAuto',
        shortcut='F10',
        tooltip=LanguageKeys.tooltip_auto
    )
    ActionFullscreen = ActionInfo(
        name=LanguageKeys.toolbar_fullscreen,
        icon=ResMap.icon_arrows_maximize,
        trigger='onToolbarFullscreen',
        shortcut='F11',
        tooltip=LanguageKeys.tooltip_fullscreen
    )
    ActionSpeedUp = ActionInfo(
        name=LanguageKeys.toolbar_speed_up,
        icon=ResMap.icon_chevrons_right,
        trigger='onToolbarSpeedUp',
        shortcut='=',
        tooltip=LanguageKeys.tooltip_speed_up
    )
    ActionSpeedDw = ActionInfo(
        name=LanguageKeys.toolbar_speed_dw,
        icon=ResMap.icon_chevrons_left,
        trigger='onToolbarSpeedDown',
        shortcut='-',
        tooltip=LanguageKeys.tooltip_speed_dw
    )
    ActionSponsor = ActionInfo(
        name=LanguageKeys.toolbar_sponsor,
        icon=ResMap.icon_coffee,
        trigger='onToolbarSponsor',
        tooltip=LanguageKeys.tooltip_sponsor
    )
    ActionPinned = ActionInfo(
        name=LanguageKeys.toolbar_pinned,
        icon=ResMap.icon_pinned_off,
        trigger='onToolbarPinned',
        tooltip=LanguageKeys.tooltip_pinned
    )


class MainTray:
    """系统托盘"""
    ActionQuit = ActionInfo(
        name=LanguageKeys.toolbar_quit,
        icon=ResMap.icon_logout,
        trigger='onToolbarQuit',
        tooltip=LanguageKeys.tooltip_quit
    )
