# -*- coding: utf-8 -*-

"""
@File    : TimingView.py
@Time    : 2024年5月22日14:20:38
@Author  : fseven<zhu867564473@live.cn>
@Desc    : 定时窗口
"""
from PySide6.QtCore import Qt, QTime
from PySide6.QtWidgets import QDialog, QGridLayout, QLabel, QCheckBox, QPushButton, QSpinBox,QTimeEdit

from conf.Lang import LanguageKeys
from conf.Views import Views
from helper.I18n import I18n
from helper.NetHelper import NetHelper
from helper.Preferences import UserKey, gPreferences
from helper.Signals import gSignals
from ui.view.ViewDelegate import ViewDelegate


class _View(ViewDelegate):
    """定时窗口UI"""

    def __init__(self, win, code, key):
        super(_View, self).__init__(win, code, key)

        self.ui_lab_start = QLabel(I18n.text(LanguageKeys.timing_start))
        self.ui_lab_start.setToolTip(I18n.text(LanguageKeys.tips_timing_start))

        self.ui_timeEdit_start = QTimeEdit()
        self.ui_timeEdit_start.setDisplayFormat('hh:mm:ss')
        self.ui_timeEdit_start.setTime(QTime.currentTime().addSecs(60))

        self.ui_lab_stop = QLabel(I18n.text(LanguageKeys.timing_stop))
        self.ui_lab_stop.setToolTip(I18n.text(LanguageKeys.tips_timing_stop))

        self.ui_timeEdit_stop = QTimeEdit()
        self.ui_timeEdit_stop.setDisplayFormat('hh:mm:ss')
        self.ui_timeEdit_stop.setTime(self.ui_timeEdit_start.time().addSecs(60 * 60 * 2))

        self.ui_lab_status = QLabel(I18n.text(LanguageKeys.timing_start))        

        self.ui_checkBox_everyDay = QCheckBox(I18n.text(LanguageKeys.timing_every_day))
        self.ui_checkBox_everyDay.setChecked(True)        
        self.ui_checkBox_everyDay.setToolTip(I18n.text(LanguageKeys.tips_timing_every_day))

        self.ui_btn_open = QPushButton(I18n.text(LanguageKeys.timing_btn_open))
        self.ui_btn_close = QPushButton(I18n.text(LanguageKeys.timing_btn_close))



        self.ui_layout = QGridLayout()
        self.ui_layout.setAlignment(Qt.AlignTop)
        self.ui_layout.addWidget(self.ui_lab_start, 0, 0, 1, 1)
        self.ui_layout.addWidget(self.ui_timeEdit_start, 0, 1, 1, 2)
        self.ui_layout.addWidget(self.ui_lab_stop, 1, 0, 1, 1)
        self.ui_layout.addWidget(self.ui_timeEdit_stop, 1, 1, 1, 2)
        self.ui_layout.addWidget(self.ui_lab_status,2,0,1,1)
        self.ui_layout.addWidget(self.ui_checkBox_everyDay, 2, 1, 1, 2)
        self.ui_layout.addWidget(self.ui_btn_close, 3, 0, 1, 1)
        self.ui_layout.addWidget(self.ui_btn_open, 3, 1, 1, 1)
        self.ui_layout.setColumnStretch(4, 1)
        self.view.setLayout(self.ui_layout)


class TimingView(QDialog):
    """选项视图"""

    def __init__(self):
        super(TimingView, self).__init__()

        self.view = _View(self, Views.Timing, UserKey.Profile.WinRect)
        self.setWindowTitle(I18n.text(LanguageKeys.toolbar_timing))
        self.setFixedHeight(130)
        self.setModal(True)
        self.setupPreferences()
        self.setupSignals()

    def setupSignals(self):
        """关联信号"""
        # noinspection PyUnresolvedReferences
        self.view.ui_btn_open.clicked.connect(self.onClosePage)
        # noinspection PyUnresolvedReferences
        self.view.ui_btn_close.clicked.connect(self.onClosePage)

    def setupPreferences(self):
        """初始化用户存储数据"""
        self.view.ui_checkBox_everyDay.setChecked(gPreferences.get(UserKey.Timing.EveryDay))     

    def savePreferences(self):
        """保存用户存储数据"""
        startTime = self.view.ui_timeEdit_start.time()
        stopTime = self.view.ui_timeEdit_stop.time()
        everDayChecked = self.view.ui_checkBox_everyDay.isChecked()        

        gPreferences.set(UserKey.Timing.EveryDay,everDayChecked)
        gPreferences.set(UserKey.Timing.StartTime,startTime.msecsSinceStartOfDay())
        gPreferences.set(UserKey.Timing.StopTime,stopTime.msecsSinceStartOfDay())

    def onClosePage(self):        
        self.savePreferences()            
        self.close()        

    def closeEvent(self, event):
        self.view.closeEvent(event)
        super(TimingView, self).closeEvent(event)

    def resizeEvent(self, event):
        self.view.resizeEvent(event)
        super(TimingView, self).resizeEvent(event)
