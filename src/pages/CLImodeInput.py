import sys
import os

from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
)
from PyQt5.QtCore import QProcess

sys.path.append("..")
from widget.RoundWidget import RoundWidget


class CLIInputTab(RoundWidget):
    def __init__(self, tab_name="Example", algorithm_name="Example", script=""):
        super().__init__()
        self.setWindowTitle("数据挖掘与攻击检测展示系统 - 攻击检测")
        self.setBackgroundColor(QColor(250, 250, 250, 200))
        self.setRadius(10)
        self.setBorder(QColor(238, 238, 238), 2)
        self.setContentsMargins(5, 5, 5, 5)

        self.script = script
        self.process = None  # 保存 QProcess 实例

        layout = QVBoxLayout()

        title_label = QLabel(tab_name)
        title_label.setObjectName("H1")
        layout.addWidget(title_label)

        tip_label = QLabel("核心算法：" + algorithm_name)
        tip_label.setObjectName("H2")
        layout.addWidget(tip_label)

        # 显示结果的文本框
        result_display = QTextEdit()
        result_display.setReadOnly(True)
        layout.addWidget(result_display)

        file_layout = QHBoxLayout()
        # 输入框
        log_path_input = QLineEdit()
        log_path_input.setPlaceholderText("请输入文本")
        file_layout.addWidget(log_path_input)

        # 开始检测按钮（初始禁用）
        start_button = QPushButton("\uf0ad")
        start_button.setFont(QFont("Segoe Fluent Icons", 10))
        start_button.setStyleSheet("padding: 0px;")
        start_button.setFixedSize(30, 30)
        start_button.setObjectName("OKButton")
        start_button.setEnabled(False)
        start_button.clicked.connect(self.on_start_clicked)
        file_layout.addWidget(start_button)

        layout.addLayout(file_layout)

        self.result_display = result_display
        self.log_path_input = log_path_input
        self.start_button = start_button

        log_path_input.textChanged.connect(self.check_start_button)

        self.setLayout(layout)

        self.start_detection(self.script)

    def check_start_button(self):
        if self.log_path_input.text():
            self.start_button.setEnabled(True)
        else:
            self.start_button.setEnabled(False)

    def start_detection(self, script):
        self.result_display.clear()

        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.setProcessChannelMode(QProcess.MergedChannels)  # 合并输出

        python_executable = sys.executable
        if not python_executable:
            self.result_display.append("Python解释器未找到")
            return

        abs_script = os.path.abspath(script)
        self.result_display.append(f"启动脚本: {abs_script}")

        self.process.start(python_executable, [abs_script])

        if not self.process.waitForStarted():
            self.result_display.append("脚本启动失败")

    def on_start_clicked(self):
        input_text = self.log_path_input.text()
        if self.process and self.process.state() == QProcess.Running:
            self.process.write((input_text + "\n").encode("utf-8"))  # 写入并回车
        else:
            self.result_display.append("进程未启动或已退出")

    def handle_stdout(self):
        data = self.process.readAllStandardOutput().data()
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            text = data.decode("gbk", errors="replace")
        self.result_display.append(text)

    def handle_stderr(self):
        error_data = self.process.readAllStandardError().data()
        try:
            text = error_data.decode("utf-8")
        except UnicodeDecodeError:
            text = error_data.decode("gbk", errors="replace")
        self.result_display.append(f"错误信息：\n{text}")


if __name__ == "__main__":
    from mod.QSSLoader import QSSLoader

    app = QApplication(sys.argv)
    app.setFont(QFont("Microsoft YaHei UI", 12))
    app.setStyleSheet(QSSLoader.load_qss_files("../../style"))
    main_window = QMainWindow()
    main_window.setWindowTitle("Data Mining and Attack Detection System")
    main_window.setGeometry(100, 100, 1650, 1000)

    data_tab = CLIInputTab(script="your_script.py")

    main_window.setCentralWidget(data_tab)

    main_window.show()
    sys.exit(app.exec_())
