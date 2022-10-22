# -*- coding: utf-8 -*-

"""
@File    : OptionsView.py
@Time    : 2022/10/1 11:52
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 选项视图
"""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QGridLayout, QLabel, QLineEdit, QPushButton, QSpinBox

from conf.Lang import LanguageKeys
from conf.Views import Views
from helper.I18n import I18n
from helper.NetHelper import NetHelper
from helper.Preferences import UserKey, gPreferences
from helper.Signals import gSignals
from ui.view.ViewDelegate import ViewDelegate


class _View(ViewDelegate):
    """选项视图UI"""

    def __init__(self, win, code, key):
        super(_View, self).__init__(win, code, key)

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
        self.view.setLayout(self.ui_layout)


class OptionsView(QDialog):
    """选项视图"""

    def __init__(self):
        super(OptionsView, self).__init__()

        self.view = _View(self, Views.Profile, UserKey.Profile.WinRect)
        self.setWindowTitle(I18n.text(LanguageKeys.toolbar_profile))
        self.setFixedHeight(110)
        self.setModal(True)
        self.setupPreferences()
        self.setupSignals()

    def setupSignals(self):
        """关联信号"""
        # noinspection PyUnresolvedReferences
        self.view.ui_btn_call.clicked.connect(self.onCallBtnClicked)
        # noinspection PyUnresolvedReferences
        self.view.ui_spin_speed.valueChanged.connect(self.onSpeedChanged)
        # noinspection PyUnresolvedReferences
        self.view.ui_spin_step.valueChanged.connect(self.onStepChanged)
        gSignals.finished_api_done.connect(self.onFetchApiResult)

    def setupPreferences(self):
        """初始化用户存储数据"""
        self.view.ui_spin_speed.setValue(gPreferences.get(UserKey.Reader.Speed))
        self.view.ui_spin_step.setValue(gPreferences.get(UserKey.Reader.Step))
        url = gPreferences.get(UserKey.Profile.NoticeUrl)
        if len(url) > 0:
            self.view.ui_edit_call.setText(url)

    def onFetchApiResult(self, result):
        """设置 GET API 返回结果"""
        if result:
            gPreferences.set(UserKey.Profile.NoticeUrl, self.view.ui_edit_call.text())
            self.view.ui_lab_tip.setText('<p style="color:green;">OK</p>')
        else:
            self.view.ui_lab_tip.setText('<p style="color:red;">BAD</p>')
        self.view.ui_btn_call.setEnabled(True)
        self.view.ui_edit_call.setEnabled(True)

    def onCallBtnClicked(self):
        """设置 Get API"""
        self.view.ui_lab_tip.clear()
        api = self.view.ui_edit_call.text()
        if len(api) > 0:
            self.view.ui_btn_call.setEnabled(False)
            self.view.ui_edit_call.setEnabled(False)
            NetHelper.httpGet(api)
        else:
            self.view.ui_lab_tip.setText('<p style="color:red;">BAD</p>')

    @staticmethod
    def onSpeedChanged(value: int):
        """速度变化事件"""
        gPreferences.set(UserKey.Reader.Speed, value)
        gSignals.reader_refresh_speed.emit()

    @staticmethod
    def onStepChanged(value: int):
        """步幅变化事件"""
        gPreferences.set(UserKey.Reader.Step, value)
        gSignals.reader_refresh_speed.emit()

    def closeEvent(self, event):
        self.view.closeEvent(event)
        super(OptionsView, self).closeEvent(event)

    def resizeEvent(self, event):
        self.view.resizeEvent(event)
        super(OptionsView, self).resizeEvent(event)
