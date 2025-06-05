from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFileDialog
from qfluentwidgets import (
    TitleLabel, StrongBodyLabel, LineEdit, PushButton,
    FluentIcon, TextEdit, PrimaryPushButton
)


class CLI_Data_Desensitization_Tab(QWidget):
    def __init__(self, tab_name="Data_Desensitization", func_name="", script=None):
        super().__init__()

        self.script = script

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # 标题
        layout.addWidget(TitleLabel(tab_name))
        

        # 文件选择 + 一键脱敏按钮（同一行）
        file_layout = QHBoxLayout()
        self.file_input = LineEdit()
        self.file_input.setPlaceholderText("请选择要检测的文件路径")
        self.file_input.setReadOnly(True)

        browse_button = PushButton(FluentIcon.FOLDER, "选择文件")
        browse_button.clicked.connect(self.browse_file)

        self.start_button = PrimaryPushButton("一键脱敏")
        self.start_button.setEnabled(False)
        self.start_button.clicked.connect(self.perform_action)

        file_layout.addWidget(self.file_input)
        file_layout.addWidget(browse_button)
        file_layout.addWidget(self.start_button)
        layout.addLayout(file_layout)

        # 结果输出框
        self.result_display = TextEdit()
        self.result_display.setReadOnly(True)
        layout.addWidget(self.result_display)

        self.setLayout(layout)

        # 状态联动
        self.file_input.textChanged.connect(self.check_ready)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择要脱敏的文件",
            "",
            "支持的文件 (*.txt *.csv *.json *.xlsx *.xls)"
        )
        if file_path:
            self.file_input.setText(file_path)
            self.result_display.clear()

    def check_ready(self):
        self.start_button.setEnabled(bool(self.file_input.text().strip()))

    def perform_action(self):
        self.result_display.clear()
        file_path = self.file_input.text().strip()

        if not file_path:
            self.result_display.append("未选择文件")
            return

        try:
            self.result_display.append("开始脱敏处理...\n")
            result_path = self.script(file_path)

            if not result_path:
                self.result_display.append("⚠️ 脱敏失败，可能未检测到敏感数据。")
                return

            self.result_display.append(f"脱敏完成，结果已保存至：\n{result_path}")

        except Exception as e:
            self.result_display.append(f"发生错误：{str(e)}")
