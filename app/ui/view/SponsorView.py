# -*- coding: utf-8 -*-

"""
@File    : SponsorView.py
@Time    : 2022/10/10 20:13
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 赞助页面
"""
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QWidget

from conf.Lang import LanguageKeys
from conf.ResMap import ResMap
from conf.Views import Views
from helper.GUI import GUI
from helper.I18n import I18n
from helper.Preferences import UserKey


class _View(GUI.View):
    def __init__(self, parent: QWidget = None):
        super(_View, self).__init__(parent)

        self.ui_lab_tip = QLabel(I18n.text(LanguageKeys.notice_sponsor))
        self.ui_pixmap_wx = QLabel('')
        self.ui_pixmap_alipay = QLabel('')

        self.ui_layout = QGridLayout()
        self.ui_layout.addWidget(self.ui_lab_tip, 0, 0, 1, 2)
        self.ui_layout.addWidget(self.ui_pixmap_wx, 1, 0, 1, 1)
        self.ui_layout.addWidget(self.ui_pixmap_alipay, 1, 1, 1, 1)
        self.setLayout(self.ui_layout)


class SponsorView(QDialog, _View):
    def __init__(self, parent: QWidget = None):
        super(SponsorView, self).__init__(parent)

        self.setModal(True)
        self.setWindowCode(Views.Sponsor)
        self.setWinRectKey(UserKey.Sponsor.WinRect)
        self.setQrcode(self.ui_pixmap_wx, 308, ResMap.img_wx_qrcode)
        self.setQrcode(self.ui_pixmap_alipay, 270, ResMap.img_alipay_qrcode)
        self.setFixedSize(640, 480)
        self.show()

    @staticmethod
    def setQrcode(canvas: QLabel, height: int, where: str):
        canvas.setScaledContents(True)
        canvas.resize(height, 420)
        canvas.setPixmap(QPixmap(where))
        canvas.show()
