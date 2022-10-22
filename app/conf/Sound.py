# -*- coding: utf-8 -*-

"""
@File    : Sound.py
@Time    : 2022/10/22 16:08
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 音效配置
"""
from enum import unique, Enum


@unique
class WindowsSounds(Enum):
    """Windows系统音频"""
    Background = "Windows Background"
    Foreground = "Windows Foreground"
    Logon = "Windows Logon"
    MessageNudge = "Windows Message Nudge"
    NotifyCalendar = "Windows Notify Calendar"
    NotifyEmail = "Windows Notify Email"
    NotifyMessaging = "Windows Notify Messaging"
    NotifySystemGeneric = "Windows Notify System Generic"
    ProximityConnection = "Windows Proximity Connection"
    ProximityNotification = "Windows Proximity Notification"
    Unlock = "Windows Unlock"
    MenuCommand = "Windows Menu Command"
    Error = "Windows Error"
    PrintComplete = "Windows Print complete"
    NavigationStart = "Windows Navigation Start"
    BatteryLow = "Windows Battery Low"
    BatteryCritical = "Windows Battery Critical"
    CriticalStop = "Windows Critical Stop"
    Ringout = "Windows Ringout"
    Ringin = "Windows Ringin"
    Exclamation = "Windows Exclamation"
    Shutdown = "Windows Shutdown"
    Restore = "Windows Restore"
    Recycle = "Windows Recycle"
    Ding = "Windows Ding"
    Default = "Windows Default"
    Startup = "Windows Startup"
    Balloon = "Windows Balloon"
    Notify = "Windows Notify"
    InformationBar = "Windows Information Bar"
    FeedDiscovered = "Windows Feed Discovered"
    PopupBlocked = "Windows Pop-up Blocked"
    HardwareInsert = "Windows Hardware Insert"
    HardwareFail = "Windows Hardware Fail"
    HardwareRemove = "Windows Hardware Remove"
    UserAccountControl = "Windows User Account Control"
    LogoffSound = "Windows Logoff Sound"
    Minimize = "Windows Minimize"
