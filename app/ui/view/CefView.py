from typing import Optional

from PySide6.QtWidgets import QWidget, QFileDialog
from cefpython3 import cefpython as cef

from conf.Lang import LanguageKeys
from conf.ResMap import ResMap
from helper.Cmm import Cmm
from helper.I18n import I18n
from helper.Preferences import UserKey, gPreferences
from helper.Signals import gSignals
from ui.model.CefModel import CefModel


class ClientHandler(object):
    """CEF浏览器事件监听"""

    def __init__(self, target: QWidget):
        self.cef_widget = target
        self.is_ready = False
        self.js_inject = Cmm.readFile(ResMap.js_inject)

    # noinspection PyUnusedLocal
    # noinspection PyMethodMayBeStatic
    def OnLoadingProgressChange(self, browser, progress):
        """页面加载进度事件"""
        # print('=> DisplayHandler::OnLoadingProgressChange()')
        # print("     progress: ", progress)
        return True

    # noinspection PyUnusedLocal
    # noinspection PyMethodMayBeStatic
    def OnAddressChange(self, browser, frame, url):
        """页面URL切换事件"""
        # print('=> DisplayHandler:OnAddressChange()')
        # print("     url: ", url)
        gSignals.cef_update_state.emit()

    # noinspection PyUnusedLocal
    # noinspection PyMethodMayBeStatic
    def OnLoadStart(self, browser, frame):
        """页面加载开始事件"""
        self.is_ready = False
        # print('=> LoadHandler::OnLoadStart()')
        # print("     url: ", browser.GetUrl())
        browser.GetMainFrame().ExecuteJavascript(self.js_inject)
        gSignals.cef_load_start.emit()

    # noinspection PyUnusedLocal
    # noinspection PyMethodMayBeStatic
    def OnLoadEnd(self, browser, frame, http_code):
        """页面加载结束事件"""
        # print("=> LoadHandler::OnLoadEnd()")
        # print("     http code: ", http_code)
        if 200 <= http_code < 300:
            gSignals.cef_load_finished.emit()
            self.is_ready = True
        else:
            self.is_ready = False

    # noinspection PyUnusedLocal
    # noinspection PyMethodMayBeStatic
    def OnLoadError(self, browser, frame, error_code, error_text_out, failed_url):
        """页面加载失败事件"""
        self.is_ready = False
        reason = "".join(error_text_out)
        reason = I18n.text(LanguageKeys.debug_network_error).format(error_code, reason)
        # print("=> LoadHandler::OnLoadError()")
        # print("     url : ", failed_url)
        # print("     code: ", error_code)
        # print("     text: ", reason)
        frame.ExecuteFunction(CefModel.JsMethod.Alert, reason)
        Cmm.playBeep()

    # noinspection PyUnusedLocal
    # noinspection PyMethodMayBeStatic
    def OnKeyEvent(self, browser, event, event_handle):
        """页面快捷键捕捉"""
        if Cmm.isWindows() and event.get("type") == 2:
            mod = event.get("modifiers")
            key = event.get("windows_key_code")
            if (mod == 0 and key in CefModel.ShortCut.values) or \
                    (mod == 8 and key == CefModel.ShortCut.Quit):
                gSignals.cef_short_cut.emit(key)
            return False


class CefView(QWidget):
    """Qt CEF 部件"""

    def __init__(self, host: QWidget):
        """
        创建 CEF 部件
        :param host: 宿主部件
        """
        super(CefView, self).__init__(host)

        self.host = host
        self.browser: Optional[cef.PyBrowser] = None
        self.handler: Optional[ClientHandler] = None

    def embedBrowser(self):
        """嵌入 CEF 窗体"""
        window_info = cef.WindowInfo()
        rect = [0, 0, self.width(), self.height()]
        window_info.SetAsChild(self.handleId(), rect)

        # 创建 Webview
        url = gPreferences.get(UserKey.Reader.LatestUrl)
        if url == "chrome-error://chromewebdata/":
            # fix [issue#19](https://github.com/DoooReyn/WxReader/issues/19)
            url = CefModel.HOME_PAGE
        self.handler = ClientHandler(self)
        self.browser = cef.CreateBrowserSync(window_info, url=url)
        self.browser.SetClientHandler(self.handler)

        # 绑定 JS -> Py 接口
        jsb = cef.JavascriptBindings(bindToFrames=True)
        jsb.SetFunction(CefModel.PyMethod.UpdateState, self.updateState)
        jsb.SetFunction(CefModel.PyMethod.SendAction, self.sendAction)
        jsb.SetFunction(CefModel.PyMethod.SavedNotes, self.savedNotes)
        self.browser.SetJavascriptBindings(jsb)

    def sendAction(self, act: int):
        """执行 JS -> Py 动作"""
        if act in CefModel.Action.values:
            if act == CefModel.Action.ScrollToEnd:
                self.doPageTurning()
            elif act == CefModel.Action.ReadingFinished:
                self.doReadingFinished()
        else:
            print(f"[未知的动作] {act}")

    def savedNotes(self, filename, content):
        """执行导出笔记"""
        title = I18n.text(LanguageKeys.tips_export_note)
        where, _ = QFileDialog.getSaveFileName(self, title, filename, filter='*.md')
        if len(where) > 0:
            Cmm.saveAs(where, content)

    def handleId(self):
        """CEF 窗口ID"""
        return int(self.winId())

    def quit(self):
        """退出 CEF"""
        if self.browser:
            gPreferences.set(UserKey.Reader.LatestUrl, self.browser.GetUrl())
            self.browser.CloseBrowser(True)
            self.browser = None

    def isReading(self):
        """是否在阅读页面"""
        return CefModel.isBookUrl(self.url())

    def url(self):
        """当前页面网址"""
        return self.browser.GetUrl()

    def focusInEvent(self, event):
        """Webview 焦点进入事件"""
        if self.browser:
            cef.WindowUtils().OnSetFocus(self.handleId(), 0, 0, 0)
            self.browser.SetFocus(True)

    def focusOutEvent(self, event):
        """Webview 焦点移出事件"""
        if self.browser:
            self.browser.SetFocus(False)

    def moveEvent(self, _):
        """Webview 移动同步"""
        if self.browser:
            cef.WindowUtils().OnSize(self.handleId(), 0, 0, 0)
            self.browser.NotifyMoveOrResizeStarted()

    def resizeEvent(self, event):
        """窗口尺寸同步"""
        if self.browser:
            cef.WindowUtils().OnSize(self.handleId(), 0, 0, 0)
            self.browser.NotifyMoveOrResizeStarted()

    def executeFunction(self, *args):
        """调用 Js Function"""
        self.page().ExecuteFunction(*args)

    def doBackHome(self):
        """回到首页"""
        self.browser.LoadUrl(CefModel.HOME_PAGE)

    def doReload(self):
        """刷新页面"""
        self.browser.Reload()

    def page(self):
        """当前页面 Frame"""
        return self.browser.GetMainFrame()

    def doPageTurning(self):
        """翻页/下一章"""
        if self.isReading() and self.scrollable() and self.handler.is_ready:
            self.executeFunction(CefModel.JsMethod.NextChapter)

    # noinspection PyMethodMayBeStatic
    def doReadingFinished(self):
        """全书完"""
        gSignals.reader_reading_finished.emit()

    def doExport(self):
        """导出笔记"""
        if self.isReading() and self.handler.is_ready:
            self.executeFunction(CefModel.JsMethod.ExportNotes)

    def doTheme(self):
        """切换主题"""
        if self.isReading() and self.handler.is_ready:
            self.executeFunction(CefModel.JsMethod.ChangeTheme)

    def doAuto(self):
        """切换自动阅读"""
        self.doScroll()

    def doSpeed(self):
        """更新阅读速度"""
        self.doScroll()

    def doScroll(self):
        """执行页面滚动"""
        if self.scrollable() and self.isReading() and self.handler.is_ready:
            self.executeFunction(CefModel.JsMethod.DoScroll, self.speed())

    @staticmethod
    def updateState(state: str):
        """更新状态"""
        gSignals.reader_status_tip_updated.emit(state)

    @staticmethod
    def runLoop():
        """CEF事件循环"""
        cef.MessageLoopWork()

    @staticmethod
    def scrollable():
        """是否自动阅读"""
        return gPreferences.get(UserKey.Reader.Scrollable)

    @staticmethod
    def speed():
        """当前阅读速度"""
        return gPreferences.get(UserKey.Reader.Speed)
