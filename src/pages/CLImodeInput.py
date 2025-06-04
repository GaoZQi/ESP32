import sys
import os

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QWidget,
)
from PyQt5.QtCore import QProcess

from qfluentwidgets import (
    TitleLabel,
    StrongBodyLabel,
    LineEdit,
    FluentIcon,
    PrimaryToolButton,
    TextEdit,
    FluentIcon,
)


class CLIInputTab(QWidget):
    def __init__(self, tab_name="Example", algorithm_name="Example", script=""):
        super().__init__()

        self.script = script
        self.process = None  # 保存 QProcess 实例

        layout = QVBoxLayout()

        title_label = TitleLabel(tab_name)
        layout.addWidget(title_label)

        tip_label = StrongBodyLabel("核心算法：" + algorithm_name)
        layout.addWidget(tip_label)

        # 显示结果的文本框
        result_display = TextEdit()
        result_display.setReadOnly(True)
        layout.addWidget(result_display)

        file_layout = QHBoxLayout()
        # 输入框
        log_path_input = LineEdit()
        log_path_input.setPlaceholderText("请输入文本")
        file_layout.addWidget(log_path_input)

        # 开始检测按钮（初始禁用）
        start_button = PrimaryToolButton(FluentIcon.PLAY)
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
