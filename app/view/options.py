# -*- coding: utf-8 -*-

"""
@File    : options.py
@Time    : 2022/10/1 11:52
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 用户自定义选项视图
"""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QLineEdit, QPushButton, QSpinBox

from conf.views import Views
from helper.gui import GUI
from helper.i18n import I18n
from helper.preferences import Preferences, UserKey
from helper.signals import Signals
from view.webview import ReaderActions


class _View(GUI.View):
    def __init__(self):
        super(_View, self).__init__()

        self.ui_lab_speed = QLabel('滚速')
        self.ui_lab_speed.setToolTip('直接修改阅读速度 (1-100)')
        self.ui_spin_speed = QSpinBox()
        self.ui_spin_speed.setMinimum(1)
        self.ui_spin_speed.setMaximum(100)
        self.ui_lab_step = QLabel('步幅')
        self.ui_lab_step.setToolTip('调整加速、减速步幅 (1-10)')
        self.ui_spin_step = QSpinBox()
        self.ui_spin_step.setMinimum(1)
        self.ui_spin_step.setMaximum(10)
        self.ui_lab_call = QLabel('读完通知')
        self.ui_edit_call = QLineEdit()
        self.ui_edit_call.setPlaceholderText('读完通知，接受GET请求')
        self.ui_btn_call = QPushButton('测试')
        self.ui_edit_call.setFixedHeight(32)

        self.ui_layout = QGridLayout()
        self.ui_layout.setAlignment(Qt.AlignTop)
        self.ui_layout.addWidget(self.ui_lab_speed, 0, 0, 1, 1)
        self.ui_layout.addWidget(self.ui_spin_speed, 0, 1, 1, 1)
        self.ui_layout.addWidget(self.ui_lab_step, 1, 0, 1, 1)
        self.ui_layout.addWidget(self.ui_spin_step, 1, 1, 1, 1)
        self.ui_layout.addWidget(self.ui_lab_call, 2, 0, 1, 1)
        self.ui_layout.addWidget(self.ui_edit_call, 2, 1, 1, 2)
        self.ui_layout.addWidget(self.ui_btn_call, 2, 3, 1, 1)
        self.ui_layout.setColumnStretch(2, 1)

        self.setLayout(self.ui_layout)


class Options(QDialog, _View):
    def __init__(self):
        super(Options, self).__init__()

        self.setWindowTitle(I18n.text("toolbar:profile"))
        self.setFixedHeight(120)
        self.setModal(True)
        self.set_window_code(Views.Profile)
        self.set_rect_key(UserKey.Profile.WinRect)
        self.setup_preferences()
        self.setup_signals()

    # noinspection PyUnresolvedReferences
    def setup_signals(self):
        self.ui_btn_call.clicked.connect(self.on_btn_call)
        self.ui_spin_speed.valueChanged.connect(self.on_speed_changed)
        self.ui_spin_step.valueChanged.connect(self.on_step_changed)

    def setup_preferences(self):
        self.ui_spin_speed.setValue(Preferences().get(UserKey.Reader.Speed))
        self.ui_spin_step.setValue(Preferences().get(UserKey.Reader.Step))
        url = Preferences().get(UserKey.Profile.NoticeUrl)
        if len(url) > 0:
            self.ui_edit_call.setText(url)

    @staticmethod
    def on_speed_changed(value: int):
        Preferences().set(UserKey.Reader.Speed, value)
        Signals().reader_setting_changed.emit(ReaderActions.SpeedDown)
        Signals().reader_refresh_speed.emit()

    @staticmethod
    def on_step_changed(value: int):
        Preferences().set(UserKey.Reader.Step, value)
        Signals().reader_setting_changed.emit(ReaderActions.SpeedDown)
        Signals().reader_refresh_speed.emit()

    def on_btn_call(self):
        api = self.ui_edit_call.text()
        print(api)

    def closeEvent(self, event: QCloseEvent):
        super(Options, self).closeEvent(event)
