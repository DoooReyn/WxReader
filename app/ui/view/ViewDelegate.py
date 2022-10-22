# -*- coding: utf-8 -*-

"""
@File    : ViewDelegate.py
@Time    : 2022/10/22 15:33
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 视图代理
"""
from typing import Union

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget, QMenu, QToolBar

from conf.Lang import LanguageKeys
from conf.Menus import ActionInfo
from helper.GUI import GUI
from helper.I18n import I18n
from helper.Preferences import gPreferences
from helper.Signals import gSignals


class ViewDelegate(object):
    """视图代理"""

    def __init__(self, win: QWidget, code: int, key: str):
        """
        视图
        :param win: 视图对象
        :param code: 视图代码
        :param key: 视图尺寸存储项
        """
        self.view: QWidget = win
        self.code: int = code
        self.key: str = key
        self.setWindowCode(code)
        self.setWinRectKey(key)

    def closeEvent(self, event):
        """视图关闭事件"""
        if self.key is not None:
            self.saveWinRect()
        if self.code > 0:
            gSignals.win_closed.emit(self.code)
        event.accept()

    def resizeEvent(self, event):
        """视图尺寸变化事件"""
        if self.key is not None:
            self.saveWinRect()
        event.accept()

    def setWindowCode(self, code: int):
        """设置视图代码"""
        self.code = code

    def setWinRectKey(self, kr: str):
        """设置视图尺寸存储项"""
        self.key = kr
        tx, ty, w, h = self.getWinRect()
        self.view.setGeometry(tx, ty, w, h)

    def getWinRect(self):
        """获取视图尺寸"""
        if self.key is not None:
            return [int(v) for v in gPreferences.get(self.key)]
        else:
            r = self.view.geometry()
            return r.topLeft().x(), r.topLeft().y(), r.width(), r.height()

    def saveWinRect(self):
        """保存视图尺寸"""
        if self.key is not None:
            r = self.view.geometry()
            r = [r.topLeft().x(), r.topLeft().y(), r.width(), r.height()]
            gPreferences.set(self.key, r)

    @staticmethod
    def onMenuActionNotImplemented(prefix, name):
        """动作的触发器未实现"""
        msg = I18n.text(LanguageKeys.debug_method_not_implemented).format(prefix, name)
        gSignals.logger_warn.emit(msg)
        print(msg)

    def addActionBy(self, info: ActionInfo, host: Union[QMenu, QToolBar]):
        """
        添加动作
        :param info: 动作信息
        :param host: 动作持有对象
        :return: 动作对象
        """
        name = I18n.text(info.name)
        act = QAction(name, host)
        if info.icon:
            act.setIcon(GUI.icon(info.icon))
        if info.shortcut:
            act.setShortcut(info.shortcut)
        if info.trigger and hasattr(self.view, info.trigger):
            # noinspection PyUnresolvedReferences
            act.triggered.connect(lambda *args, t=self.view, g=info.trigger: getattr(t, g)())
        else:
            prefix = host.objectName()
            # noinspection PyUnresolvedReferences
            act.triggered.connect(lambda *args, m=prefix, n=name: self.onMenuActionNotImplemented(m, n))
        host.addAction(act)
        return act
