from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout
from PyQt5.QtCore import Qt

from qfluentwidgets import SegmentedWidget
from pages import *


class DataHandleTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("DataHandleTab")

        self.mode = SegmentedWidget(self)
        self.stack = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)

        self.vBoxLayout.setContentsMargins(20, 10, 20, 20)
        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.addWidget(self.mode, 0, Qt.AlignHCenter)
        self.vBoxLayout.addWidget(self.stack)
        self.setLayout(self.vBoxLayout)

        items = [
            {
                "title": "BilndWaterMark",
                "func_name": "",
                "script": "",
                "widget": CLITab,
            },
            {"title": "Peano", "func_name": "", "script": "", "widget": CLIInputTab},
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
            {"title": "Gilbert", "func_name": "", "script": "", "widget": CLITab},
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


if __name__ == "__main__":
    from mod.QSSLoader import QSSLoader
    from PyQt5.QtGui import QFont
    from PyQt5.QtWidgets import QApplication, QMainWindow

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
