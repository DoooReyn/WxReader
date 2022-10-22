# -*- coding: utf-8 -*-

"""
@File    : GUI.py
@Time    : 2022/10/22 16:30
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 工具栏动作对象
"""
from abc import abstractmethod, ABC

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QToolBar

from helper.Preferences import gPreferences, UserKey


class StatefulAction(ABC):
    """拥有状态的动作"""

    def __init__(self, action: QAction = None):
        self.action = action
        self.onLoad()

    @abstractmethod
    def onLoad(self):
        """刷新状态"""
        pass

    @abstractmethod
    def onChanged(self):
        """状态变化"""
        pass

    @abstractmethod
    def value(self):
        """获取当前状态"""
        pass


class PinnedAction(StatefulAction):
    """固定任务栏动作"""

    def __init__(self, action: QAction, bar: QToolBar):
        self.bar = bar
        super(PinnedAction, self).__init__(action)

    def onLoad(self):
        self.bar.show() if self.value() else self.bar.hide()

    def onChanged(self):
        visible = self.bar.isVisible()
        gPreferences.set(UserKey.Reader.Pinned, not visible)
        self.onLoad()

    def value(self):
        return gPreferences.get(UserKey.Reader.Pinned)


class ScrollableAction(StatefulAction):
    """自动阅读动作"""

    def value(self):
        return gPreferences.get(UserKey.Reader.Scrollable)

    def onLoad(self):
        self.action.setChecked(self.value())

    def onChanged(self):
        gPreferences.set(UserKey.Reader.Scrollable, self.action.isChecked())
        self.onLoad()


class UnchangeableAction(StatefulAction):
    """无需做出响应的动作"""

    def value(self):
        pass

    def onLoad(self):
        pass

    def onChanged(self):
        pass


class SpeedAction(UnchangeableAction):
    """速度调整动作"""

    def value(self):
        return gPreferences.get(UserKey.Reader.Speed)

    @staticmethod
    def check(speed: int):
        """限定速度范围"""
        return min(100, max(1, speed))


class SpeedUpAction(SpeedAction):
    """速度提高动作"""

    def onChanged(self):
        step = gPreferences.get(UserKey.Reader.Step)
        gPreferences.set(UserKey.Reader.Speed, self.check(self.value() + step))


class SpeedDwAction(SpeedAction):
    """速度降低动作"""

    def onChanged(self):
        step = gPreferences.get(UserKey.Reader.Step)
        gPreferences.set(UserKey.Reader.Speed, self.check(self.value() - step))
