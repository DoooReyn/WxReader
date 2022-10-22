# -*- coding: utf-8 -*-

"""
@File    : SponsorView.py
@Time    : 2022/10/10 20:13
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 赞助页面
"""
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QGridLayout, QLabel, QWidget

from conf.Lang import LanguageKeys
from conf.ResMap import ResMap
from conf.Views import Views
from helper.I18n import I18n
from helper.Preferences import UserKey
from ui.view.ViewDelegate import ViewDelegate


class _View(ViewDelegate):
    """赞助视图 UI"""

    def __init__(self, win, code, key):
        super(_View, self).__init__(win, code, key)

        self.ui_lab_tip = QLabel(I18n.text(LanguageKeys.notice_sponsor))
        self.ui_pixmap_wx = QLabel('')
        self.ui_pixmap_alipay = QLabel('')

        self.ui_layout = QGridLayout()
        self.ui_layout.addWidget(self.ui_lab_tip, 0, 0, 1, 2)
        self.ui_layout.addWidget(self.ui_pixmap_wx, 1, 0, 1, 1)
        self.ui_layout.addWidget(self.ui_pixmap_alipay, 1, 1, 1, 1)
        self.view.setLayout(self.ui_layout)


class SponsorView(QDialog):
    """赞助视图"""

    def __init__(self, parent: QWidget = None):
        super(SponsorView, self).__init__(parent)

        self.view = _View(self, Views.Sponsor, UserKey.Sponsor.WinRect)
        self.setModal(True)
        self.setFixedSize(640, 480)
        self.setQrcode(self.view.ui_pixmap_wx, 308, ResMap.img_wx_qrcode)
        self.setQrcode(self.view.ui_pixmap_alipay, 270, ResMap.img_alipay_qrcode)
        self.show()

    @staticmethod
    def setQrcode(canvas: QLabel, height: int, where: str):
        """设置二维码图片"""
        canvas.setScaledContents(True)
        canvas.resize(height, 420)
        canvas.setPixmap(QPixmap(where))
        canvas.show()

    def closeEvent(self, event):
        self.view.closeEvent(event)
        super(SponsorView, self).closeEvent(event)

    def resizeEvent(self, event):
        self.view.resizeEvent(event)
        super(SponsorView, self).resizeEvent(event)
