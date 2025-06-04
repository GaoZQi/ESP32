import sys
import os

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)
from PyQt5.QtCore import QProcess

from qfluentwidgets import (
    TitleLabel,
    StrongBodyLabel,
    LineEdit,
    PushButton,
    FluentIcon,
    PrimaryDropDownPushButton,
    TextEdit,
    RoundMenu,
    Action,
)


class CLITab(QWidget):
    def __init__(
        self,
        tab_name="Example",
        algorithm_name="Example",
        encode_func=None,
        decode_func=None,
    ):
        super().__init__()

        # 存储传入的函数
        self.encode_func = encode_func
        self.decode_func = decode_func

        layout = QVBoxLayout()

        title_label = TitleLabel(tab_name)
        layout.addWidget(title_label)

        tip_label = StrongBodyLabel("核心算法：" + algorithm_name)
        layout.addWidget(tip_label)

        file_layout = QHBoxLayout()
        # 输入框：日志文件路径
        log_path_input = LineEdit()
        log_path_input.setPlaceholderText("请输入待检测文件路径")
        log_path_input.setReadOnly(True)
        file_layout.addWidget(log_path_input)

        # 浏览按钮
        browse_button = PushButton(FluentIcon.FOLDER, "选择文件")
        browse_button.clicked.connect(lambda: self.browse_file(log_path_input))
        file_layout.addWidget(browse_button)
        layout.addLayout(file_layout)

        # 开始检测按钮（初始禁用）
        start_button = PrimaryDropDownPushButton("选择操作")
        start_button.setEnabled(False)

        # 创建菜单
        menu = RoundMenu(parent=start_button)
        menu.addAction(
            Action(
                "加密",
                triggered=lambda: self.perform_action("encode", log_path_input.text()),
            )
        )
        menu.addAction(
            Action(
                "解密",
                triggered=lambda: self.perform_action("decode", log_path_input.text()),
            )
        )

        # 添加菜单
        start_button.setMenu(menu)
        file_layout.addWidget(start_button)

        # 显示结果的文本框
        result_display = TextEdit()
        result_display.setReadOnly(True)
        layout.addWidget(result_display)

        self.result_display = result_display
        self.log_path_input = log_path_input
        self.start_button = start_button

        # 输入框文本变化时检查启用状态
        log_path_input.textChanged.connect(self.check_start_button)

        self.setLayout(layout)

    def check_start_button(self):
        """检查是否启用开始检测按钮"""
        if self.log_path_input.text():
            self.start_button.setEnabled(True)
        else:
            self.start_button.setEnabled(False)

    def browse_file(self, log_path_input):
        """打开文件对话框选择日志文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择要上传的文件", "", "文件 (*)"
        )
        if file_path:
            log_path_input.setText(file_path)
            self.result_display.clear()  # 清空日志

    def perform_action(self, action_type, file_path):
        if not file_path:
            return

        self.result_display.clear()

        try:
            if action_type == "encode" and self.encode_func:
                self.result_display.append("开始加密...")
                result = self.encode_func(file_path)
                self.result_display.append("加密完成!")
                self.result_display.append(f"加密结果: {result}")
            elif action_type == "decode" and self.decode_func:
                self.result_display.append("开始解密...")
                result = self.decode_func(file_path)
                self.result_display.append("解密完成!")
                self.result_display.append(f"解密结果: {result}")
            else:
                self.result_display.append("错误：未指定有效的处理函数")
        except Exception as e:
            self.result_display.append(f"操作过程中发生错误：{str(e)}")
