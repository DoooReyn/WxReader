# -*- coding: utf-8 -*-

"""
@File    : lang.py
@Time    : 2022/9/27 16:20
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 语言包
  - 可以根据需要配置语言包
"""

from enum import Enum, unique


class LanguageKeys:
    app_name = "app_name"
    toolbar_help = "toolbar_help"
    toolbar_refresh = "toolbar_refresh"
    toolbar_about = "toolbar_about"
    toolbar_profile = "toolbar_profile"
    toolbar_quit = "toolbar_quit"
    toolbar_hide = "toolbar_hide"
    toolbar_auto = "toolbar_auto"
    toolbar_export = "toolbar_export"
    toolbar_theme = "toolbar_theme"
    toolbar_fullscreen = "toolbar_fullscreen"
    toolbar_back_home = "toolbar_back_home"
    toolbar_speed_up = "toolbar_speed_up"
    toolbar_speed_dw = "toolbar_speed_dw"
    toolbar_sponsor = "toolbar_sponsor"
    toolbar_pinned = "toolbar_pinned"
    notice_btn_ok = "notice_btn_ok"
    notice_about = "notice_about"
    notice_help = "notice_help"
    notice_profile = "notice_profile"
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


TIPS_READING_FINISHED = "tips:reading_finished"

ABOUT_CN = """
### Hi, there! 🤠 I'm DoooReyn.

-   🐼  A game developer from China
-   👷‍️ A repeat wheel maker
-   😘  A faithful fan of PyQt
-   🧙‍️ Currently focusing on `Cocos2d-x / Cocos Creator`


### Projects

-   📘 [微信读书自动阅读器 Web版](https://github.com/DoooReyn/WxRead-WebAutoReader) 
-   📗 [微信读书自动阅读器 PC版](https://github.com/DoooReyn/WxRead-PC-AutoReader)
-   👌 [手势识别与训练模型](https://wu57.cn/Game/gestures/)
-   🖕 [Cocos Creator 手势识别](https://github.com/DoooReyn/ccc-gesture-recognition) > [在线演示](https://wu57.cn/games/gesture/web-desktop/)
-   😎 [Cocos2d-x 目录监视器](https://github.com/DoooReyn/cocos2d-x-dir-monitor)
-   🛤️ [Cocos2d-x 内置 WebSocket 服务器](https://github.com/DoooReyn/cocos2d-x-lws)
-   💻 [Cocos2d-x 内置 HTTP 服务器](https://github.com/DoooReyn/cocos2d-x-lhs)
-   🎸 [Cocos2d-x Fmod 集成指南](https://github.com/DoooReyn/fmod-for-cocos2dx)
-   📓 [Cocos2d-x 使用 spdlog](https://github.com/DoooReyn/cocos2d-x-spdlog)
-   🌕 [Cocos2d-x 接入 lua-protobuf](https://github.com/DoooReyn/cocos2d-x-lua-protobuf)
-   🕹️ [Console for Cocos2d-x based on PyQt5](https://github.com/DoooReyn/Console)
-   🧰 [位图字体工具箱 BMFontToolbox](https://github.com/DoooReyn/BMFontToolbox)
-   💰 [给人事的工资明细助手](https://wu57.cn/Game/SalaryBook/)
-   ⚔️ [Lua 字符串插值](https://github.com/DoooReyn/lua-string-interpolate)
-   📬 [Formatted log for Lua](https://github.com/DoooReyn/lua_format_log)
-   📚 [IT 电子书收藏夹](https://github.com/DoooReyn/dbooks-links.git)
-   📒 [微信/支付宝账单转换器](https://github.com/DoooReyn/wechat-alipay-bill-converter)
-   👾 [虾虾虾鼓捣的 Web Game Demo](https://wu57.cn/Game/games/)

### Find Me

-   ✍️ [Blog](https://wu57.cn/)
-   📚 [简书](https://www.jianshu.com/u/5b3708fe7f63)
-   💌 jl88744653@gmail.com

"""

HELP_CN = """
### 帮助
"""


class _Languages:
    """
    语言包列表
    """
    CN = {
        # general
        "app_name": "微读自动阅读器",

        # toolbar
        "toolbar_help": "查看帮助",
        "toolbar_refresh": "刷新一下",
        "toolbar_about": "关于作者",
        "toolbar_profile": "更多选项",
        "toolbar_quit": "退出阅读",
        "toolbar_hide": "退到后台",
        "toolbar_auto": "自动阅读",
        "toolbar_export": "导出笔记",
        "toolbar_theme": "切换主题",
        "toolbar_fullscreen": "切换全屏",
        "toolbar_back_home": "回到首页",
        "toolbar_speed_up": "神行太保",
        "toolbar_speed_dw": "凌波微步",
        "toolbar_sponsor": "一杯咖啡",
        "toolbar_pinned": "固定此栏",

        # notice
        "notice_btn_ok": "好哒！",
        "notice_about": ABOUT_CN,
        "notice_help": HELP_CN,
        "notice_profile": HELP_CN,
        "notice_sponsor": HELP_CN,

        # exception
        "exception_name": "异常通知",

        # debug
        "debug_method_not_implemented": "[ {0} > {1} ] 方法未实现",
        "debug_inject_script_failed": "注入脚本{}失败",
        "debug_network_error": "网络似乎有点问题呢~",

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
        "tips_reading_finished": "<p style='font-size:24px;color:#5d646e;text-align:center;'>全书已读完</p>",
    }


@unique
class LangPack(Enum):
    """语言包可选项"""
    CN = _Languages.CN
