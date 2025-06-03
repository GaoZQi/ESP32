import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QDialog,
    QLineEdit,
    QFileDialog,
    QTableWidgetItem,
    QTableWidget,
)
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QFont, QColor

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

# from widget.RoundWidget import RoundWidget
from mod.QSSLoader import QSSLoader

# from widget.IconButton import IconButton
# from alorgorithmDialog import alorgorithmDialog as PopupDialog
# from algorithms import *


class DataMiningTab(QWidget):
    def __init__(self):
        super().__init__()
        # self.setBackgroundColor(QColor(250, 250, 250, 200))
        # self.setRadius(10)
        # self.setBorder(QColor(238, 238, 238), 2)
        self.setContentsMargins(10, 0, 10, 10)  # 设置内边距
        self.algorithms = {"": None}
        self.setObjectName("dataMiningTab")
        self.dataURL = None
        self.choose = list(self.algorithms.keys())[0]
        main_layout = QHBoxLayout()
        alorgorithm_layout = QHBoxLayout()
        alorgorithm_layout.setContentsMargins(0, 0, 0, 0)
        data_layout = QHBoxLayout()
        self.Data_tab = QWidget()
        # Dropdown for algorithm selection
        self.tip = "算法："
        self.algorithm_label = QLabel(self.tip + self.choose)
        self.algorithm_label.setObjectName("H1")
        # algorithm_button = IconButton("\ue932")
        # algorithm_button.clicked.connect(self.show_popup)
        alorgorithm_layout.addWidget(self.algorithm_label)
        alorgorithm_layout.addSpacing(5)
        # alorgorithm_layout.addWidget(algorithm_button)
        alorgorithm_layout.setAlignment(Qt.AlignLeft)
        # main_layout.addLayout(alorgorithm_layout)

        data_tip = QLabel("数据集")
        data_tip.setObjectName("H2")
        # main_layout.addWidget(data_tip)

        data_URL_layout = QHBoxLayout()
        self.dataURLText = QLineEdit()
        self.dataURLText.setPlaceholderText("数据集路径")
        self.dataURLText.setReadOnly(True)
        data_URL_layout.addWidget(self.dataURLText)
        choose_button = QPushButton("选择数据集")
        choose_button.setObjectName("chooseButton")
        choose_button.clicked.connect(self.choose_file)
        data_URL_layout.addWidget(choose_button)
        data_layout.addLayout(data_URL_layout)

        # Table for displaying data
        self.table = QTableWidget()
        self.table.setMinimumWidth(350)

        # Run button
        self.run_button = QPushButton("运行")
        self.run_button.setObjectName("OKButton")
        self.run_button.setEnabled(False)
        self.run_button.clicked.connect(self.run_algorithm)

        # 在类初始化部分修改画布创建代码
        self.canvas_container = QWidget()
        self.canvas_container.setContentsMargins(0, 0, 0, 0)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background: transparent;")

        # 设置Matplotlib图形背景为透明
        self.figure.patch.set_alpha(0)

        # 将画布添加到容器
        canvas_layout = QVBoxLayout(self.canvas_container)
        canvas_layout.setContentsMargins(0, 0, 0, 0)
        canvas_layout.addWidget(self.canvas)

        config_layout = QVBoxLayout()
        config_layout.addLayout(alorgorithm_layout)
        config_layout.addWidget(data_tip)
        config_layout.addLayout(data_layout)
        config_layout.addWidget(self.table)
        config_layout.addWidget(self.run_button)
        config_layout.setAlignment(Qt.AlignTop)
        # Combine layouts
        pic_tip = QLabel("处理结果")
        pic_tip.setObjectName("H1")
        pic_layout = QVBoxLayout()
        pic_layout.addWidget(pic_tip)
        # pic_layout.addWidget(self.canvas, stretch=3)
        pic_layout.addWidget(self.canvas_container, stretch=3)
        main_layout.addLayout(config_layout, 2)  # 左边3份
        main_layout.addSpacing(10)  # 左右间距
        main_layout.addLayout(pic_layout, 2)  # 右边2份
        main_layout.setStretch(0, 1)  # 第一个子布局（左边）权重3
        main_layout.setStretch(1, 2)  # 第二个子布局（右边）权重2
        self.setLayout(main_layout)

    def showEvent(self, event):
        super().showEvent(event)
        QApplication.postEvent(self, QEvent(QEvent.UpdateRequest))  # 触发立即重绘

    def run_algorithm(self):
        selected_algorithm = self.algorithm_label.text().replace(self.tip, "")
        if not selected_algorithm or not self.dataURL:
            return

        # 清除旧图形
        self.figure.clf()
        self.ax = self.figure.add_subplot(111)

        # 添加加载动画
        self.ax.text(
            0.5,
            0.5,
            "正在处理中...",
            ha="center",
            va="center",
            fontsize=14,
            color="gray",
        )
        self.canvas.draw()

        # 异步执行耗时操作
        QApplication.processEvents()  # 立即处理UI事件

        try:
            algorithm_func = self.algorithms[selected_algorithm]
            algorithm_func(self.dataURL, self.ax, self.canvas)

            # 强制界面更新
            self.canvas.draw()
            self.canvas.update()
            self.update()  # 更新整个widget
        except Exception as e:
            self.figure.clf()
            self.ax = self.figure.add_subplot(111)
            self.ax.text(
                0.5, 0.5, f"Error: {str(e)}", ha="center", va="center", color="red"
            )
            self.canvas.draw()

    def show_popup(self):
        dialog = QDialog(
            self, items=self.algorithms, title="数据挖掘算法", choose=self.choose
        )
        if dialog.exec_() == QDialog.Accepted:
            selected = dialog.selected_algorithm
            # 更新标签或下拉框
            print("Selected algorithm:", selected)
            self.algorithm_label.setText(self.tip + selected)

    def choose_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "选择数据集", "", "CSV Files (*.csv);;All Files (*)"
        )
        if file_name:
            self.dataURLText.setText(file_name)
            self.dataURL = file_name
            self.run_button.setEnabled(True)
            self.load_csv_data()  # ← 加载数据
        else:
            self.dataURLText.clear()
            self.dataURL = None
            self.run_button.setEnabled(False)
            self.table.clear()

    def load_csv_data(self):
        if not self.dataURL:
            return
        import csv

        with open(self.dataURL, newline="", encoding="utf-8-sig") as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)

        if not rows:
            self.table.clear()
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            return

        row_count = len(rows)
        col_count = max(len(row) for row in rows)

        self.table.clear()
        self.table.setRowCount(row_count)
        self.table.setColumnCount(col_count)
        # （可选）将第一行作为水平表头
        self.table.setHorizontalHeaderLabels(rows[0])
        data_rows = rows[1:]
        for i, row in enumerate(data_rows):
            for j, cell in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(cell))

        # 如果不需要特殊表头，就全部按数据填入：
        # 隐藏水平表头（列名）
        self.table.horizontalHeader().setVisible(False)
        # 隐藏垂直表头（行号）
        self.table.verticalHeader().setVisible(False)

        for i, row in enumerate(rows):
            for j, cell in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(cell))


if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    app.setFont(QFont("Microsoft YaHei UI", 12))
    app.setStyleSheet(QSSLoader.load_qss_files("style"))
    main_window.setWindowTitle("Data Mining and Attack Detection System")
    main_window.setGeometry(100, 100, 825, 500)

    data_tab = DataMiningTab()
    main_window.setCentralWidget(data_tab)

    main_window.show()
    sys.exit(app.exec_())
