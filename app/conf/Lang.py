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
    tooltip_help = "tooltip_help"
    tooltip_refresh = "tooltip_refresh"
    tooltip_about = "tooltip_about"
    tooltip_profile = "tooltip_profile"
    tooltip_quit = "tooltip_quit"
    tooltip_hide = "tooltip_hide"
    tooltip_auto = "tooltip_auto"
    tooltip_export = "tooltip_export"
    tooltip_theme = "tooltip_theme"
    tooltip_fullscreen = "tooltip_fullscreen"
    tooltip_back_home = "tooltip_back_home"
    tooltip_speed_up = "tooltip_speed_up"
    tooltip_speed_dw = "tooltip_speed_dw"
    tooltip_sponsor = "tooltip_sponsor"
    tooltip_pinned = "tooltip_pinned"
    notice_btn_ok = "notice_btn_ok"
    notice_about = "notice_about"
    notice_help = "notice_help"
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


TIPS_READING_FINISHED = "tips:reading_finished"

ABOUT_CN = """
- 应用：微读自动阅读器
- 版本：2.0.0
- 作者：[DoooReyn](https://github.com/DoooReyn)
- 仓库：[WxReader](https://github.com/DoooReyn/WxReader)
"""

HELP_CN = """
<h3>一、前言</h3>
<p><strong>微读阅读器</strong>从<strong>2020.02.17</strong>开始立项，出发点原本就是一个意外，但东西出来之后，意外地收到了很多朋友的喜欢和关注。</p>
<p>从最初的网页版，衍变到后来基于<strong>Electron.js</strong>开发的PC版问世，自此之后<strong>微读阅读器</strong>的版本就一直停留在<strong>1.3.0</strong>。 因为它纯粹是我一时热血上头开发的一个小工具，所以不会让它太占用我的个人时间。
尽管后来收到了一些反馈和建议，但是 U Know，懒是阶段性的，热情下头之后就很难抬起手来继续了。</p>
<p>如今，时隔两年半，收到了不少用户反馈之后，<strong>微读阅读器2.0</strong> 终于发布啦！</p>
<p>相比 <strong>1.3</strong>，<strong>2.0</strong> 做了比较大的改进，主要包括：</p>
<ul>
<li>弃用 <strong>Electron.js</strong> 框架，改用 <strong>PyQt5</strong> 作为底层支持，大大减小了软件包体积;</li>
<li>所有操作都放在了工具栏，操作更加简单直接，大大提升用户体验；</li>
<li>修复大范围挂机暂停的问题：
<ul>
<li>
<strong>1.3</strong> 在切换页面之后就会进行滚动判定，如果内容未加载完毕，可能造成误判；<strong>2.0</strong> 只有当页面内容完全载入之后才会开启滚动；</li>
<li>
<strong>1.3</strong> 的页面滚动失效问题比较严重，<strong>2.0</strong> 使用应用级定时器来刷新滚动状态，目前测试来看还算比较稳定；</li>
</ul>
</li>
<li>优化自动阅读时暂停的条件：选中文本、打开目录、打开评论；</li>
<li>增加速度、步幅设置，放宽速度限制；</li>
<li>增加全文阅读完成时发送 <strong>GET</strong> 请求的功能；</li>
<li>
<strong>2.0</strong>将完全开源，但未经允许禁止投入商业使用。</li>
</ul>
<p>最后，<strong>微读阅读器2.0</strong>是基于 <strong>PyQy5</strong> 全新开发的，整个过程差不多花了一周 <em>（因为国庆罢工啦）</em>，时间上是比较仓促的，
因此很可能还存在一些问题或体验上的不足，后续会陆续跟进维护，也欢迎大家到<a href="https://github.com/DoooReyn/WxReader">官方仓库</a>提问题。</p>
<hr />
<h3>二、快捷键</h3>
<table>
<tbody>
<tr>
<td>F1</td>
<td>打开帮助</td>
</tr>
<tr>
<td>F2</td>
<td>打开关于</td>
</tr>
<tr>
<td>F3</td>
<td>回到首页</td>
</tr>
<tr>
<td>F5</td>
<td>刷新页面</td>
</tr>
<tr>
<td>F8</td>
<td>导出笔记</td>
</tr>
<tr>
<td>F9</td>
<td>切换主题</td>
</tr>
<tr>
<td>F10</td>
<td>自动阅读开关</td>
</tr>
<tr>
<td>F11</td>
<td>切换全屏</td>
</tr>
<tr>
<td>F12</td>
<td>更多选项</td>
</tr>
<tr>
<td>+</td>
<td>加快滚动速度</td>
</tr>
<tr>
<td>-</td>
<td>降低滚动速度</td>
</tr>
<tr>
<td>Home</td>
<td>回到顶部</td>
</tr>
<tr>
<td>End</td>
<td>滚到顶部</td>
</tr>
<tr>
<td>PgUp</td>
<td>向上滚动一个视图</td>
</tr>
<tr>
<td>PgDn</td>
<td>向下滚动一个视图</td>
</tr>
<tr>
<td>←</td>
<td>上一章(页)</td>
</tr>
<tr>
<td>→</td>
<td>下一章(页)</td>
</tr>
<tr>
<td>↑</td>
<td>向上滚动一行</td>
</tr>
<tr>
<td>↓</td>
<td>向下滚动一行</td>
</tr>
</tbody>
</table>
<hr />
<h3>三、常见问题</h3>
<ul>
<li>如果碰到开启自动阅读之后页面没有反应的情况，可以尝试刷新一下页面，基本可以解决问题；</li>
<li>如有其他问题或建议，请到<a href="https://github.com/DoooReyn/WxReader">官方仓库</a>进行讨论;</li>
<li>你也可以给我发邮件 <strong><a href="mailto:jl88744653@gmail.com">jl88744653@gmail.com</a></strong>，但请确保主题是<strong>我为微读提意见</strong>，不然可能会被我过滤掉。</li>
</ul>
"""


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
        "toolbar_hide": "静默",
        "toolbar_auto": "自动",
        "toolbar_export": "笔记",
        "toolbar_theme": "主题",
        "toolbar_fullscreen": "全屏",
        "toolbar_back_home": "首页",
        "toolbar_speed_up": "加速",
        "toolbar_speed_dw": "减速",
        "toolbar_sponsor": "赞助",
        "toolbar_pinned": "固定",

        "tooltip_help": "查看帮助",
        "tooltip_refresh": "刷新页面",
        "tooltip_about": "关于软件",
        "tooltip_profile": "更多选项",
        "tooltip_quit": "退出阅读",
        "tooltip_hide": "退到后台，静默阅读",
        "tooltip_auto": "切换自动阅读",
        "tooltip_theme": "切换主题",
        "tooltip_export": "导出阅读笔记",
        "tooltip_fullscreen": "切换全屏",
        "tooltip_back_home": "回到首页",
        "tooltip_speed_up": "加速",
        "tooltip_speed_dw": "减速",
        "tooltip_sponsor": "赞助一下，支持作者",
        "tooltip_pinned": "固定工具栏",

        # notice
        "notice_btn_ok": "好哒！",
        "notice_about": ABOUT_CN,
        "notice_help": HELP_CN,
        "notice_sponsor": "❤开发不易，请支持一下作者❤",

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
