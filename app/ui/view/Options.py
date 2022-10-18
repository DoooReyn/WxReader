# -*- coding: utf-8 -*-

"""
@File    : Options.py
@Time    : 2022/10/1 11:52
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 用户自定义选项视图
"""
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QDialog, QGridLayout, QLabel, QLineEdit, QPushButton, QSpinBox

from conf.Lang import LanguageKeys
from conf.Views import Views
from helper.GUI import GUI
from helper.I18n import I18n
from helper.NetHelper import NetHelper
from helper.Preferences import Preferences, UserKey
from helper.Signals import Signals
from ui.model.ReaderHelper import ReaderActions


class _View(GUI.View):
    def __init__(self):
        super(_View, self).__init__()

        self.ui_lab_speed = QLabel(I18n.text(LanguageKeys.options_speed))
        self.ui_lab_speed.setToolTip(I18n.text(LanguageKeys.options_tooltip_speed))
        self.ui_spin_speed = QSpinBox()
        self.ui_spin_speed.setMinimum(1)
        self.ui_spin_speed.setMaximum(100)
        self.ui_lab_step = QLabel(I18n.text(LanguageKeys.options_step))
        self.ui_lab_step.setToolTip(I18n.text(LanguageKeys.options_tooltip_step))
        self.ui_spin_step = QSpinBox()
        self.ui_spin_step.setMinimum(1)
        self.ui_spin_step.setMaximum(10)
        self.ui_lab_call = QLabel(I18n.text(LanguageKeys.options_finished_notice))
        self.ui_edit_call = QLineEdit()
        self.ui_edit_call.setPlaceholderText(I18n.text(LanguageKeys.options_finished_placeholder))
        self.ui_btn_call = QPushButton(I18n.text(LanguageKeys.options_api_test))
        self.ui_edit_call.setFixedHeight(32)
        self.ui_lab_tip = QLabel('')

        self.ui_layout = QGridLayout()
        self.ui_layout.setAlignment(Qt.AlignTop)
        self.ui_layout.addWidget(self.ui_lab_speed, 0, 0, 1, 1)
        self.ui_layout.addWidget(self.ui_spin_speed, 0, 1, 1, 1)
        self.ui_layout.addWidget(self.ui_lab_step, 0, 2, 1, 1)
        self.ui_layout.addWidget(self.ui_spin_step, 0, 3, 1, 1)
        self.ui_layout.addWidget(self.ui_lab_call, 1, 0, 1, 1)
        self.ui_layout.addWidget(self.ui_edit_call, 1, 1, 1, 4)
        self.ui_layout.addWidget(self.ui_btn_call, 1, 5, 1, 1)
        self.ui_layout.addWidget(self.ui_lab_tip, 2, 1, 1, 6)
        self.ui_layout.setColumnStretch(4, 1)

        self.setLayout(self.ui_layout)


class Options(_View, QDialog):
    def __init__(self):
        super(Options, self).__init__()

        self.setWindowTitle(I18n.text(LanguageKeys.toolbar_profile))
        self.setFixedHeight(110)
        self.setModal(True)
        self.setWindowCode(Views.Profile)
        self.setWinRectKey(UserKey.Profile.WinRect)
        self.setupPreferences()
        self.setupSignals()

    # noinspection PyUnresolvedReferences
    def setupSignals(self):
        self.ui_btn_call.clicked.connect(self.onCallBtnClicked)
        self.ui_spin_speed.valueChanged.connect(self.onSpeedChanged)
        self.ui_spin_step.valueChanged.connect(self.onStepChanged)
        Signals().finished_api_done.connect(self.onFetchApiResult)

    def setupPreferences(self):
        self.ui_spin_speed.setValue(Preferences().get(UserKey.Reader.Speed))
        self.ui_spin_step.setValue(Preferences().get(UserKey.Reader.Step))
        url = Preferences().get(UserKey.Profile.NoticeUrl)
        if len(url) > 0:
            self.ui_edit_call.setText(url)

    @staticmethod
    def onSpeedChanged(value: int):
        Preferences().set(UserKey.Reader.Speed, value)
        Signals().reader_setting_changed.emit(ReaderActions.SpeedDown)
        Signals().reader_refresh_speed.emit()

    @staticmethod
    def onStepChanged(value: int):
        Preferences().set(UserKey.Reader.Step, value)
        Signals().reader_setting_changed.emit(ReaderActions.SpeedDown)
        Signals().reader_refresh_speed.emit()

    def onFetchApiResult(self, result):
        if result:
            Preferences().set(UserKey.Profile.NoticeUrl, self.ui_edit_call.text())
            self.ui_lab_tip.setText('<p style="color:green;">OK</p>')
        else:
            self.ui_lab_tip.setText('<p style="color:red;">BAD</p>')
        self.ui_btn_call.setEnabled(True)
        self.ui_edit_call.setEnabled(True)

    def onCallBtnClicked(self):
        self.ui_lab_tip.clear()
        api = self.ui_edit_call.text()
        if len(api) > 0:
            self.ui_btn_call.setEnabled(False)
            self.ui_edit_call.setEnabled(False)
            NetHelper.httpGet(api)
        else:
            self.ui_lab_tip.setText('<p style="color:red;">BAD</p>')

    def closeEvent(self, event: QCloseEvent):
        super(Options, self).closeEvent(event)
