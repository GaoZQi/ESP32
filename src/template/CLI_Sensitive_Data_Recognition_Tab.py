from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFileDialog
from qfluentwidgets import (
    TitleLabel, StrongBodyLabel, LineEdit, PushButton,
    FluentIcon, TextEdit, PrimaryPushButton
)


class CLI_Sensitive_Data_Recognition_Tab(QWidget):
    def __init__(self, tab_name="数据脱敏", algorithm_name="敏感数据脱敏", script=None):
        super().__init__()

        self.script_func = script  # 脱敏执行函数（如 run_from_path）

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # 标题
        layout.addWidget(TitleLabel(tab_name))

        # 文件选择布局
        file_layout = QHBoxLayout()
        self.file_input = LineEdit()
        self.file_input.setPlaceholderText("请选择要脱敏的文件")
        self.file_input.setReadOnly(True)

        browse_button = PushButton(FluentIcon.FOLDER, "选择文件")
        browse_button.clicked.connect(self.browse_file)

        self.detect_button = PrimaryPushButton("开始检测")
        self.detect_button.setEnabled(False)
        self.detect_button.clicked.connect(self.start_detection)

        file_layout.addWidget(self.file_input)
        file_layout.addWidget(browse_button)
        file_layout.addWidget(self.detect_button)

        layout.addLayout(file_layout)

        # 结果显示区域
        self.result_display = TextEdit()
        self.result_display.setReadOnly(True)
        layout.addWidget(self.result_display)

        self.setLayout(layout)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "支持文件 (*.txt *.csv *.xlsx *.xls *.json)")
        if file_path:
            self.file_path = file_path
            self.file_input.setText(file_path)
            self.result_display.clear()
            self.detect_button.setEnabled(True)

    def start_detection(self):
        self.result_display.clear()

        if not self.script_func:
            self.result_display.append("⚠️ 未设置处理函数！")
            return

        if not self.file_path:
            self.result_display.append("⚠️ 文件路径为空！")
            return

        try:
            self.result_display.append("开始脱敏处理...")
            result = self.script_func(self.file_path)
            self.result_display.append(str(result))
        except Exception as e:
            self.result_display.append(f"发生错误：{str(e)}")
