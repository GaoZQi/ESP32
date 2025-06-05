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
        layout.setContentsMargins(0, 0, 0, 0)

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

class CLI1Tab(QWidget):
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
        log_path_input.setPlaceholderText("请输入原始图片路径")
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

    def perform_action(self, action_type, origion_file):
        if not origion_file:
            return

        self.result_display.clear()

        try:
            if action_type == "encode" and self.encode_func:
                self.result_display.append("开始加密...")
                result = self.encode_func.encode(origion_file)
                self.result_display.append("加密完成!")
                self.result_display.append(f"加密结果: {result}")
            elif action_type == "decode" and self.decode_func:
                self.result_display.append("开始解密...")
                result = self.decode_func.decode(origion_file)
                self.result_display.append("解密完成!")
                self.result_display.append(f"解密结果: {result}")
            else:
                self.result_display.append("错误：未指定有效的处理函数")
        except Exception as e:
            self.result_display.append(f"操作过程中发生错误：{str(e)}")

class CLI2Tab(QWidget):
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
        log_path_input.setPlaceholderText("请输入原始图片路径")
        log_path_input.setReadOnly(True)
        file_layout.addWidget(log_path_input)

        # 浏览按钮
        browse_button = PushButton(FluentIcon.FOLDER, "选择文件")
        browse_button.clicked.connect(lambda: self.browse_file(log_path_input))
        file_layout.addWidget(browse_button)
        layout.addLayout(file_layout)

        file_layout2 = QHBoxLayout()
        file_input2 = LineEdit()
        file_input2.setPlaceholderText("请输入隐藏图片路径")
        file_input2.setReadOnly(True)
        browse_button2 = PushButton(FluentIcon.FOLDER, "选择文件")
        browse_button2.clicked.connect(lambda: self.browse_file(file_input2))
        file_layout2.addWidget(file_input2)
        file_layout2.addWidget(browse_button2)
        layout.addLayout(file_layout2)

        # 开始检测按钮（初始禁用）
        start_button = PrimaryDropDownPushButton("选择操作")
        start_button.setEnabled(False)

        # 创建菜单
        menu = RoundMenu(parent=start_button)
        menu.addAction(
            Action(
                "加密",
                triggered=lambda: self.perform_action("encode", log_path_input.text(), file_input2.text()),
            )
        )
        menu.addAction(
            Action(
                "解密",
                triggered=lambda: self.perform_action("decode", log_path_input.text(), file_input2.text()),
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

    def perform_action(self, action_type, origion_file, hide_file):
        if not origion_file or not hide_file:
            return

        self.result_display.clear()

        try:
            if action_type == "encode" and self.encode_func:
                self.result_display.append("开始加密...")
                self.encode_func.encode(origion_file, hide_file)
                result = "加密成功"
                self.result_display.append("加密完成!")
                self.result_display.append(f"加密结果: {result}")
            elif action_type == "decode" and self.decode_func:
                self.result_display.append("开始解密...")
                self.decode_func.decode(origion_file, hide_file)
                self.result_display.append("解密完成!")
                result = "解密成功"
                self.result_display.append(f"解密结果: {result}")
            else:
                self.result_display.append("错误：未指定有效的处理函数")
        except Exception as e:
            self.result_display.append(f"操作过程中发生错误：{str(e)}")
            
class CLI3Tab(QWidget):
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
        log_path_input.setPlaceholderText("请输入原始图片路径")
        log_path_input.setReadOnly(True)
        file_layout.addWidget(log_path_input)

        # 浏览按钮
        browse_button = PushButton(FluentIcon.FOLDER, "选择文件")
        browse_button.clicked.connect(lambda: self.browse_file(log_path_input))
        file_layout.addWidget(browse_button)
        layout.addLayout(file_layout)

        file_layout2 = QHBoxLayout()
        file_input2 = LineEdit()
        file_input2.setPlaceholderText("请输入隐藏图片路径")
        file_input2.setReadOnly(True)
        browse_button2 = PushButton(FluentIcon.FOLDER, "选择文件")
        browse_button2.clicked.connect(lambda: self.browse_file(file_input2))
        file_layout2.addWidget(file_input2)
        file_layout2.addWidget(browse_button2)
        layout.addLayout(file_layout2)
        
        file_layout3 = QHBoxLayout()
        file_input3 = LineEdit()
        file_input3.setPlaceholderText("请输入解密图片路径")
        file_input3.setReadOnly(True)
        browse_button3 = PushButton(FluentIcon.FOLDER, "选择文件")
        browse_button3.clicked.connect(lambda: self.browse_file(file_input3))
        file_layout3.addWidget(file_input3)
        file_layout3.addWidget(browse_button3)
        layout.addLayout(file_layout3)
        
        self.text_input = LineEdit()
        self.text_input.setPlaceholderText("请输入维度权重信息")
        layout.addWidget(self.text_input)

        # 开始检测按钮（初始禁用）
        start_button = PrimaryDropDownPushButton("选择操作")
        start_button.setEnabled(False)

        # 创建菜单
        menu = RoundMenu(parent=start_button)
        menu.addAction(
            Action(
                "加密",
                triggered=lambda: self.perform_action("encode", log_path_input.text(), file_input2.text()),
            )
        )
        menu.addAction(
            Action(
                "解密",
                triggered=lambda: self.perform_action(action_type="decode", origion_file=file_input3.text(), text_input=self.text_input.text())
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
        self.file_input2 = file_input2
        self.file_input3 = file_input3
        self.start_button = start_button

        # 输入框文本变化时检查启用状态
        log_path_input.textChanged.connect(self.check_start_button)
        file_input2.textChanged.connect(self.check_start_button)
        file_input3.textChanged.connect(self.check_start_button)
        self.text_input.textChanged.connect(self.check_start_button)
        self.setLayout(layout)

    def check_start_button(self):
        """检查是否启用开始检测按钮"""
        if (self.log_path_input.text() and self.file_input2.text()) or (self.file_input3.text() and self.text_input.text()):
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

    def perform_action(self, action_type, origion_file, hide_file = '', text_input = ''):

        self.result_display.clear()

        try:
            if action_type == "encode" and self.encode_func:
                self.result_display.append("开始加密...")
                result = self.encode_func.encode(origion_file, hide_file)
                self.result_display.append("加密完成!")
                self.result_display.append(f"加密结果: {result}")
            elif action_type == "decode" and self.decode_func:
                self.result_display.append("开始解密...")
                print(text_input)
                result = self.decode_func.decode(origion_file, text_input)
                self.result_display.append("解密完成!")
                self.result_display.append(f"解密结果: {result}")
            else:
                self.result_display.append("错误：未指定有效的处理函数")
        except Exception as e:
            self.result_display.append(f"操作过程中发生错误：{str(e)}")
            
class CLITEXTTab(QWidget):
    def __init__(self, tab_name="Example", algorithm_name="Example", encode_func=None, decode_func=None):
        super().__init__()

        self.encode_func = encode_func
        self.decode_func = decode_func

        layout = QVBoxLayout()

        layout.addWidget(TitleLabel(tab_name))
        layout.addWidget(StrongBodyLabel("核心算法：" + algorithm_name))

        self.text_input = LineEdit()
        self.text_input.setPlaceholderText("请输入隐藏信息")
        layout.addWidget(self.text_input)

        file_layout2 = QHBoxLayout()
        self.file_input = LineEdit()
        self.file_input.setPlaceholderText("请输入隐藏图片路径")
        self.file_input.setReadOnly(True)
        browse_button2 = PushButton(FluentIcon.FOLDER, "选择文件")
        browse_button2.clicked.connect(lambda: self.browse_file(self.file_input))
        file_layout2.addWidget(self.file_input)
        file_layout2.addWidget(browse_button2)
        layout.addLayout(file_layout2)

        self.start_button = PrimaryDropDownPushButton("选择操作")
        self.start_button.setEnabled(False)
        layout.addWidget(self.start_button)

        self.text_input.textChanged.connect(self.check_start_button)
        self.file_input.textChanged.connect(self.check_start_button)

        menu = RoundMenu(parent=self.start_button)
        menu.addAction(Action("加密", triggered=lambda: self.perform_action("encode", self.text_input.text())))
        menu.addAction(Action("解密", triggered=lambda: self.perform_action("decode", file=self.file_input.text())))
        self.start_button.setMenu(menu)

        self.result_display = TextEdit()
        self.result_display.setReadOnly(True)
        layout.addWidget(self.result_display)

        self.setLayout(layout)

    def check_start_button(self):
        if self.text_input.text() or self.file_input.text():
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

    def perform_action(self, action_type, text = '', file = None):
        self.result_display.clear()
        try:
            if action_type == "encode" and self.encode_func:
                self.result_display.append("开始加密...")
                res = self.encode_func.encode(text)
                self.result_display.append("加密完成!")
                self.result_display.append(f"加密结果保存至: {res}")
            elif action_type == "decode" and self.decode_func:
                self.result_display.append("开始解密...")
                res = self.decode_func.decode(file)
                self.result_display.append("解密完成!")
                self.result_display.append(f"解密结果保存至: {res}")
            else:
                self.result_display.append("错误：未指定有效的处理函数")
        except Exception as e:
            self.result_display.append(f"操作过程中发生错误：{str(e)}")

class CLITEXT2Tab(QWidget):
    def __init__(self, tab_name="Example", algorithm_name="Example", encode_func=None, decode_func=None):
        super().__init__()

        self.encode_func = encode_func
        self.decode_func = decode_func

        layout = QVBoxLayout()

        layout.addWidget(TitleLabel(tab_name))
        layout.addWidget(StrongBodyLabel("核心算法：" + algorithm_name))

        self.text_input = LineEdit()
        self.text_input.setPlaceholderText("请输入隐藏信息")
        layout.addWidget(self.text_input)
        
        self.text_input1 = LineEdit()
        self.text_input1.setPlaceholderText("请输入密码")
        layout.addWidget(self.text_input1)

        file_layout2 = QHBoxLayout()
        self.file_input = LineEdit()
        self.file_input.setPlaceholderText("请输入隐藏图片路径")
        self.file_input.setReadOnly(True)
        browse_button2 = PushButton(FluentIcon.FOLDER, "选择文件")
        browse_button2.clicked.connect(lambda: self.browse_file(self.file_input))
        file_layout2.addWidget(self.file_input)
        file_layout2.addWidget(browse_button2)
        layout.addLayout(file_layout2)

        self.start_button = PrimaryDropDownPushButton("选择操作")
        self.start_button.setEnabled(False)
        layout.addWidget(self.start_button)

        self.text_input.textChanged.connect(self.check_start_button)
        self.file_input.textChanged.connect(self.check_start_button)

        menu = RoundMenu(parent=self.start_button)
        menu.addAction(Action("加密", triggered=lambda: self.perform_action("encode", secret=self.text_input.text(), password=self.text_input1.text(), file=self.file_input.text())))
        menu.addAction(Action("解密", triggered=lambda: self.perform_action("decode", password=self.text_input1.text(), file=self.file_input.text())))
        self.start_button.setMenu(menu)

        self.result_display = TextEdit()
        self.result_display.setReadOnly(True)
        layout.addWidget(self.result_display)

        self.setLayout(layout)

    def check_start_button(self):
        if self.text_input.text() or self.file_input.text():
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

    def perform_action(self, action_type, secret = '', password = '',file = None):
        self.result_display.clear()
        try:
            if action_type == "encode" and self.encode_func:
                self.result_display.append("开始加密...")
                res = self.encode_func.encode(secret, password, file)
                self.result_display.append("加密完成!")
                self.result_display.append(f"加密结果保存至: {res}")
            elif action_type == "decode" and self.decode_func:
                self.result_display.append("开始解密...")
                res = self.decode_func.decode(password, file)
                self.result_display.append("解密完成!")
                self.result_display.append(f"解密结果为: {res}")
            else:
                self.result_display.append("错误：未指定有效的处理函数")
        except Exception as e:
            self.result_display.append(f"操作过程中发生错误：{str(e)}")
