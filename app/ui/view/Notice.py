# -*- coding: utf-8 -*-

"""
@File    : Notice.py
@Time    : 2022/9/27 21:56
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 通知子窗口
"""
from enum import Enum

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QTextBrowser, QVBoxLayout

from helper.GUI import GUI


class _View(GUI.View):
    def __init__(self):
        super(_View, self).__init__()

        self.ui_msg_box = QTextBrowser()
        self.ui_msg_box.setContextMenuPolicy(Qt.NoContextMenu)
        self.ui_msg_box.setReadOnly(True)
        self.ui_msg_box.setFont(GUI.font())
        self.ui_msg_box.setAcceptRichText(True)
        self.ui_msg_box.setOpenExternalLinks(True)
        self.ui_msg_box.setLineWrapMode(QTextBrowser.NoWrap)
        self.ui_msg_box.setTextInteractionFlags(Qt.LinksAccessibleByMouse)

        self.ui_layout = QVBoxLayout()
        self.ui_layout.addWidget(self.ui_msg_box)

        self.setLayout(self.ui_layout)


class FillType(Enum):
    PlainText = 0
    Markdown = 1
    Html = 2


class Notice(QDialog, _View):

    def __init__(self,
                 code: int,
                 rect_key: str,
                 sub_title: str,
                 content: str,
                 fill_type: FillType = FillType.Markdown,
                 modal: bool = False
                 ):
        super(Notice, self).__init__()

        self.setModal(modal)
        self.setWindowCode(code)
        self.setWinRectKey(rect_key)
        self.setupUi(sub_title, content, fill_type)

    def setupUi(self, sub_title: str, content: str, fill_type: FillType):
        self.setWindowTitle(sub_title)
        self.setMinimumSize(480, 320)

        if fill_type == FillType.PlainText:
            self.ui_msg_box.setPlainText(content)
        elif fill_type == FillType.Markdown:
            self.ui_msg_box.setMarkdown(content)
        elif fill_type == FillType.Html:
            self.ui_msg_box.setHtml(content)

        self.show()
