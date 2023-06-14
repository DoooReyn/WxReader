# -*- coding: utf-8 -*-

"""
@File    : Lang.py
@Time    : 2022/9/27 16:20
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 语言包
  - 可以根据需要配置语言包
"""

from enum import Enum, unique


class LanguageKeys:
    """语言键值映射"""

    app_name = "app_name"
    toolbar_help = "toolbar_help"
    toolbar_refresh = "toolbar_refresh"
    toolbar_about = "toolbar_about"
    toolbar_profile = "toolbar_profile"
    toolbar_quit = "toolbar_quit"
    toolbar_auto = "toolbar_auto"
    toolbar_export = "toolbar_export"
    toolbar_theme = "toolbar_theme"
    toolbar_fullscreen = "toolbar_fullscreen"
    toolbar_back_home = "toolbar_back_home"
    toolbar_speed_up = "toolbar_speed_up"
    toolbar_speed_dw = "toolbar_speed_dw"
    toolbar_sponsor = "toolbar_sponsor"
    toolbar_pinned = "toolbar_pinned"
    tooltip_help = "tooltip_help"
    tooltip_refresh = "tooltip_refresh"
    tooltip_about = "tooltip_about"
    tooltip_profile = "tooltip_profile"
    tooltip_quit = "tooltip_quit"
    tooltip_auto = "tooltip_auto"
    tooltip_export = "tooltip_export"
    tooltip_theme = "tooltip_theme"
    tooltip_fullscreen = "tooltip_fullscreen"
    tooltip_back_home = "tooltip_back_home"
    tooltip_speed_up = "tooltip_speed_up"
    tooltip_speed_dw = "tooltip_speed_dw"
    tooltip_sponsor = "tooltip_sponsor"
    tooltip_pinned = "tooltip_pinned"
    tooltip_open_view = "tooltip_open_view"
    notice_btn_ok = "notice_btn_ok"
    notice_sponsor = "notice_sponsor"
    exception_name = "exception_name"
    debug_method_not_implemented = "debug_method_not_implemented"
    debug_inject_script_failed = "debug_inject_script_failed"
    debug_network_error = "debug_network_error"
    tips_speed = "tips_speed"
    tips_page_ready = "tips_page_ready"
    tips_page_loading = "tips_page_loading"
    tips_next_chapter_ready = "tips_next_chapter_ready"
    tips_has_selection = "tips_has_selection"
    tips_wait_for_next_chapter = "tips_wait_for_next_chapter"
    tips_scroll_to_end = "tips_scroll_to_end"
    tips_no_book_view = "tips_no_book_view"
    tips_auto_read_on = "tips_auto_read_on"
    tips_page_loaded_ok = "tips_page_loaded_ok"
    tips_page_loaded_bad = "tips_page_loaded_bad"
    tips_export_note = "tips_export_note"
    tips_note_exported_ok = "tips_note_exported_ok"
    tips_note_exported_bad = "tips_note_exported_bad"
    tips_notice = "tips_notice"
    tips_reading_finished = "tips_reading_finished"
    options_speed = "options_speed"
    options_tooltip_speed = "options_tooltip_speed"
    options_step = "options_step"
    options_tooltip_step = "options_tooltip_step"
    options_finished_notice = "options_finished_notice"
    options_finished_placeholder = "options_finished_placeholder"
    options_api_test = "options_api_test"


class _Languages:
    """
    语言包列表
    """
    CN = {
        # general
        "app_name": "微读自动阅读器",

        # toolbar
        "toolbar_help": "帮助",
        "toolbar_refresh": "刷新",
        "toolbar_about": "关于",
        "toolbar_profile": "选项",
        "toolbar_quit": "退出",
        "toolbar_auto": "自动",
        "toolbar_export": "笔记",
        "toolbar_theme": "主题",
        "toolbar_fullscreen": "全屏",
        "toolbar_back_home": "首页",
        "toolbar_speed_up": "加速",
        "toolbar_speed_dw": "减速",
        "toolbar_sponsor": "赞助",
        "toolbar_pinned": "收起",

        "tooltip_help": "查看帮助    F1",
        "tooltip_about": "关于软件    F2",
        "tooltip_sponsor": "赞助一下，支持作者    F3",
        "tooltip_back_home": "回到首页    F4",
        "tooltip_refresh": "刷新页面    F5",
        "tooltip_pinned": "收起工具栏    F6",
        "tooltip_export": "导出阅读笔记    F8",
        "tooltip_theme": "切换主题 (暂不可用) F9",
        "tooltip_auto": "切换自动阅读    F10",
        "tooltip_fullscreen": "切换全屏    F11",
        "tooltip_profile": "更多选项    F12",
        "tooltip_quit": "退出阅读    Alt+Q",
        "tooltip_speed_up": "加速    +",
        "tooltip_speed_dw": "减速    -",

        # notice
        "notice_btn_ok": "好哒！",
        "notice_sponsor": "❤开发不易，请支持一下作者❤",

        # exception
        "exception_name": "异常通知",

        # debug
        "debug_method_not_implemented": "[ {0} > {1} ] 方法未实现",
        "debug_inject_script_failed": "注入脚本{}失败",
        "debug_network_error": "网络似乎有点问题呢~\n错误代码: {0}\n错误信息: {1}",

        # tips
        "tips_speed": "阅读速度:{}",
        "tips_page_ready": "准备加载页面",
        "tips_page_loading": "正在加载页面",
        "tips_next_chapter_ready": "下一章加载完成",
        "tips_has_selection": "有选中文本",
        "tips_wait_for_next_chapter": "等待跳转下一章",
        "tips_scroll_to_end": "滚动到底部了",
        "tips_no_book_view": "未打开书籍",
        "tips_auto_read_on": '自动阅读中...',
        "tips_page_loaded_ok": '页面加载完成',
        "tips_page_loaded_bad": '页面加载失败',
        "tips_export_note": '保存笔记',
        "tips_note_exported_ok": '【{}】已保存',
        "tips_note_exported_bad": '【{}】未保存',
        "tips_notice": "通知",
        "tips_reading_finished": "全书已读完",

        # options
        "options_speed": "滚动速度",
        "options_tooltip_speed": "直接修改阅读速度 (1-100)",
        "options_step": "调节步幅",
        "options_tooltip_step": "调整速度增量 (1-10)",
        "options_finished_notice": "读完通知",
        "options_finished_placeholder": "你可以在此填入一个GET接口",
        "options_api_test": "测试",
    }


@unique
class LangPack(Enum):
    """语言包可选项"""
    CN = _Languages.CN
