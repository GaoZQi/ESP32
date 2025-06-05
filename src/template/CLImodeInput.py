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
    def __init__(self, tab_name="Example", algorithm_name="Example", process_func=None):
        super().__init__()

        # 存储传入的处理函数
        self.process_func = process_func

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

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

    def check_start_button(self):
        if self.log_path_input.text():
            self.start_button.setEnabled(True)
        else:
            self.start_button.setEnabled(False)

    def on_start_clicked(self):
        input_text = self.log_path_input.text()
        if not input_text:
            return

        self.result_display.clear()
        self.result_display.append(f"输入内容: {input_text}")
        self.result_display.append("正在处理...")

        try:
            if self.process_func:
                result = self.process_func(input_text)
                self.result_display.append("处理完成!")
                self.result_display.append(f"处理结果:\n{result}")
            else:
                self.result_display.append("错误：未指定处理函数")
        except Exception as e:
            self.result_display.append(f"处理过程中发生错误：{str(e)}")
