# -*- coding: utf-8 -*-

"""
@File    : Notice.py
@Time    : 2022/9/27 21:56
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 通知子窗口
"""
from enum import Enum, unique

from PySide6.QtCore import Qt
from PySide6.QtGui import QTextBlockFormat, QTextOption
from PySide6.QtWidgets import QDialog, QTextBrowser, QVBoxLayout

from helper.GUI import GUI
from ui.view.ViewDelegate import ViewDelegate


@unique
class ContentFillType(Enum):
    """内容填充类型"""
    PlainText = 0
    Markdown = 1
    Html = 2


class _View(ViewDelegate):
    """通知视图 UI"""

    def __init__(self, win, code, key):
        super(_View, self).__init__(win, code, key)

        self.ui_msg_box = QTextBrowser()
        self.ui_msg_box.setContextMenuPolicy(Qt.NoContextMenu)
        self.ui_msg_box.setReadOnly(True)
        self.ui_msg_box.setFont(GUI.font())
        self.ui_msg_box.setAcceptRichText(True)
        self.ui_msg_box.setOpenExternalLinks(True)
        self.ui_msg_box.setWordWrapMode(QTextOption.WordWrap)
        self.ui_msg_box.setLineWrapMode(QTextBrowser.LineWrapMode.FixedColumnWidth)
        self.ui_msg_box.setLineWrapColumnOrWidth(self.ui_msg_box.width())
        self.ui_msg_box.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        self.ui_msg_box.setStyleSheet("QTextBrowser {font-size: 16px;}")

        self.ui_layout = QVBoxLayout()
        self.ui_layout.addWidget(self.ui_msg_box)
        self.view.setLayout(self.ui_layout)


class NoticeView(QDialog):
    """通知视图"""

    def __init__(self,
                 code: int,
                 rect_key: str,
                 sub_title: str,
                 content: str,
                 fill_type: ContentFillType = ContentFillType.Markdown
                 ):
        super(NoticeView, self).__init__()

        self.view = _View(self, code, rect_key)
        self.view.setWindowCode(code)
        self.view.setWinRectKey(rect_key)
        self.setModal(True)
        self.setupUi(sub_title, content, fill_type)

    def setupUi(self, sub_title: str, content: str, fill_type: ContentFillType):
        """设置UI"""
        self.setWindowTitle(sub_title)
        self.setMinimumSize(480, 340)

        if fill_type == ContentFillType.PlainText:
            self.view.ui_msg_box.setPlainText(content)
            self.applyBasicStyle()
        elif fill_type == ContentFillType.Markdown:
            self.view.ui_msg_box.setMarkdown(content)
            self.applyBasicStyle()
        elif fill_type == ContentFillType.Html:
            self.view.ui_msg_box.setHtml(content)

        self.show()

    def applyBasicStyle(self):
        """应用风格"""
        font = self.view.ui_msg_box.font()
        font.setPointSize(16)
        self.view.ui_msg_box.setFont(font)
        self.view.ui_msg_box.document().setDocumentMargin(10)
        self.view.ui_msg_box.setFixedHeight(int(self.view.ui_msg_box.document().size().height()))
        self.setFixedHeight(self.view.ui_msg_box.height() + 20)

    def setContentCentered(self):
        """设置内容居中"""
        font = self.view.ui_msg_box.font()
        font.setBold(True)
        font.setPointSize(16)
        self.view.ui_msg_box.setFont(font)
        self.view.ui_msg_box.setAlignment(Qt.AlignCenter)
        self.view.ui_msg_box.document().setDocumentMargin(10)
        self.view.ui_msg_box.setFixedHeight(int(self.view.ui_msg_box.document().size().height()))
        self.setFixedSize(320, self.view.ui_msg_box.height() + 20)

    def applyLineSpacing(self):
        """设置行间距"""
        fmt = self.view.ui_msg_box.textCursor().blockFormat()
        fmt.setLineHeight(16, QTextBlockFormat.LineDistanceHeight)
        self.view.ui_msg_box.textCursor().setBlockFormat(fmt)

    def closeEvent(self, event):
        self.view.closeEvent(event)
        super(NoticeView, self).closeEvent(event)

    def resizeEvent(self, event):
        self.view.resizeEvent(event)
        super(NoticeView, self).resizeEvent(event)
