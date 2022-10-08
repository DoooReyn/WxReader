# -*- coding: utf-8 -*-

"""
@File    : WindowController.py
@Time    : 2022/10/7 15:08
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : PyCharm
"""
from ui.controller.Controller import Controller
from ui.view.WindowView import WindowView


class WindowController(Controller):
    def __init__(self):
        super(WindowController, self).__init__()

        self._view = WindowView()

        self.start()

    def start(self):
        self._view.show()
