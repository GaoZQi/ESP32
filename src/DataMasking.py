import sys
import os

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QListWidget,
    QListWidgetItem,
    QStackedWidget,
)
from PyQt5.QtCore import Qt

from qfluentwidgets import SegmentedWidget

from template import *


class DataMaskingTab(QWidget):

    def __init__(self):
        super().__init__()
        self.setObjectName("DataMaskingTab")

        self.mode = SegmentedWidget(self)
        self.stack = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)

        self.vBoxLayout.setContentsMargins(20, 20, 20, 20)
        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.addWidget(self.mode, 0, Qt.AlignHCenter)
        self.vBoxLayout.addWidget(self.stack)

        self.setLayout(self.vBoxLayout)
        # 导航项文本列表
        items = [
            {
                "title": "BilndWaterMark",
                "func_name": "",
                "script": "",
                "widget": CLITab,
            },
            {
                "title": "Peano",
                "func_name": "",
                "script": "",
                "widget": CLIInputTab,
            },
            {
                "title": "SampleScaleDown",
                "func_name": "",
                "script": "",
                "widget": CLITab,
            },
            {
                "title": "Novel_To_Image",
                "func_name": "",
                "script": "",
                "widget": CLIInputTab,
            },
            {
                "title": "Gilbert",
                "func_name": "",
                "script": "",
                "widget": CLITab,
            },
            {
                "title": "Cloacked-pixel",
                "func_name": "",
                "script": "",
                "widget": CLITab,
            },
        ]
        # 添加页面与标签项
        for item in items:
            page = item["widget"](item["title"], item["func_name"], item["script"])
            page.setObjectName(item["title"])  # 设置唯一标识
            self.stack.addWidget(page)
            self.mode.addItem(
                routeKey=item["title"],
                text=item["title"],
                onClick=lambda _, p=page: self.stack.setCurrentWidget(p),
            )

        # 初始化状态
        self.stack.setCurrentIndex(0)
        self.mode.setCurrentItem(self.stack.currentWidget().objectName())
