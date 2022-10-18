# -*- coding: utf-8 -*-

"""
@File    : Notice.py
@Time    : 2022/9/27 21:56
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 通知子窗口
"""
from enum import Enum

from PySide6.QtCore import Qt
from PySide6.QtGui import QTextBlockFormat, QTextOption
from PySide6.QtWidgets import QDialog, QTextBrowser, QVBoxLayout

from helper.GUI import GUI


class FillType(Enum):
    PlainText = 0
    Markdown = 1
    Html = 2


class _View(GUI.View):
    def __init__(self):
        super(_View, self).__init__()

        self.ui_msg_box = QTextBrowser()
        self.ui_msg_box.setContextMenuPolicy(Qt.NoContextMenu)
        self.ui_msg_box.setReadOnly(True)
        self.ui_msg_box.setFont(GUI.font())
        self.ui_msg_box.setAcceptRichText(True)
        self.ui_msg_box.setOpenExternalLinks(True)
        self.ui_msg_box.setWordWrapMode(QTextOption.WordWrap)
        self.ui_msg_box.setLineWrapMode(QTextBrowser.FixedColumnWidth)
        self.ui_msg_box.setLineWrapColumnOrWidth(self.ui_msg_box.width())
        self.ui_msg_box.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        self.ui_msg_box.setStyleSheet("QTextBrowser {font-size: 16px;}")

        self.ui_layout = QVBoxLayout()
        self.ui_layout.addWidget(self.ui_msg_box)

        self.setLayout(self.ui_layout)


class Notice(_View, QDialog):

    def __init__(self,
                 code: int,
                 rect_key: str,
                 sub_title: str,
                 content: str,
                 fill_type: FillType = FillType.Markdown
                 ):
        super(Notice, self).__init__()

        self.setModal(True)
        self.setWindowCode(code)
        self.setWinRectKey(rect_key)
        self.setupUi(sub_title, content, fill_type)

    def setupUi(self, sub_title: str, content: str, fill_type: FillType):
        self.setWindowTitle(sub_title)
        self.setMinimumSize(480, 320)

        if fill_type == FillType.PlainText:
            self.ui_msg_box.setPlainText(content)
            self.applyBasicStyle()
        elif fill_type == FillType.Markdown:
            self.ui_msg_box.setMarkdown(content)
            self.applyBasicStyle()
        elif fill_type == FillType.Html:
            self.ui_msg_box.setHtml(content)

        self.show()

    def applyBasicStyle(self):
        font = self.ui_msg_box.font()
        font.setPointSize(16)
        self.ui_msg_box.setFont(font)
        self.ui_msg_box.document().setDocumentMargin(10)
        self.ui_msg_box.setFixedHeight(int(self.ui_msg_box.document().size().height()))
        self.setFixedHeight(self.ui_msg_box.height() + 20)

    def center(self):
        font = self.ui_msg_box.font()
        font.setBold(True)
        font.setPointSize(16)
        self.ui_msg_box.setFont(font)
        self.ui_msg_box.setAlignment(Qt.AlignCenter)
        self.ui_msg_box.document().setDocumentMargin(10)
        self.ui_msg_box.setFixedHeight(int(self.ui_msg_box.document().size().height()))
        self.setFixedSize(320, self.ui_msg_box.height() + 20)

    def applyLineSpacing(self):
        fmt = self.ui_msg_box.textCursor().blockFormat()
        fmt.setLineHeight(16, QTextBlockFormat.LineDistanceHeight)
        self.ui_msg_box.textCursor().setBlockFormat(fmt)
