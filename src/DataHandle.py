import sys
import os

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QStackedWidget,
)
from PyQt5.QtCore import Qt

from qfluentwidgets import TitleLabel

from pages import *


class DataHandleTab(QWidget):

    def __init__(self):
        super().__init__()
        self.setObjectName("DataHandleTab")

        self.setContentsMargins(10, 10, 10, 10)
        self.list_widget = QListWidget()
        # 右侧堆栈页面
        self.stack = QStackedWidget()

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

        # 添加导航项及对应页面
        for item in items:
            tab = QListWidgetItem(item["title"])
            # item.setTextAlignment(Qt.AlignCenter)
            self.list_widget.addItem(tab)
            # 每个导航项对应一个实例页面
            self.stack.addWidget(
                item["widget"](item["title"], item["func_name"], item["script"])
            )

        # 默认选中第一个
        self.list_widget.setCurrentRow(0)

        # 连接信号：列表行变化切换堆栈页面
        self.list_widget.currentRowChanged.connect(self.stack.setCurrentIndex)

        # 整体布局
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.list_widget)
        main_layout.addWidget(self.stack)

        self.setLayout(main_layout)


if __name__ == "__main__":
    from mod.QSSLoader import QSSLoader
    from PyQt5.QtGui import QFont

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app = QApplication(sys.argv)
    app.setFont(QFont("Microsoft YaHei UI", 12))
    app.setStyleSheet(QSSLoader.load_qss_files("../style"))
    main_window = QMainWindow()
    main_window.setWindowTitle("Data Mining and Attack Detection System")
    main_window.setGeometry(100, 100, 825, 500)

    data_tab = DataHandleTab()
    main_window.setCentralWidget(data_tab)

    main_window.show()
    sys.exit(app.exec_())
