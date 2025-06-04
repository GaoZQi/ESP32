import os, sys
from typing import Optional
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFileDialog,
)
from PyQt5.QtCore import Qt
from qfluentwidgets import (
    TitleLabel,
    TextEdit,
    FluentIcon,
    Action,
    CommandBar,
    Flyout,
    InfoBarIcon,
    FlyoutAnimationType,
    MessageBox,
    BodyLabel,
)

import algorithms.SecureEditor.secure_core as core


class SensitiveData(QWidget):

    def __init__(self):
        super().__init__()
        self.setObjectName("SensitiveDataPage")

        self.TitleLabel = TitleLabel("文档透明加密编辑器")
        self.text_edit = TextEdit(self)
        self.text_edit.setReadOnly(True)

        self.file_label = BodyLabel()

        self.commandBar = CommandBar()
        self.commandBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        # 初始化命令栏按钮并保存引用
        self.action_new = Action(
            FluentIcon.ADD, "新建文件", triggered=self.new_file
        )  # 新增
        self.action_open = Action(
            FluentIcon.FOLDER, "打开文件", triggered=self.open_file
        )
        self.action_unlock = Action(
            FluentIcon.VIEW, "解锁文件", triggered=self.unlock_edit
        )
        self.action_save = Action(FluentIcon.SAVE, "保存文件", triggered=self.save_file)
        self.action_export = Action(
            FluentIcon.SAVE_AS, "导出文件", triggered=self.export_file
        )

        self.commandBar.addAction(self.action_new)  # 新增按钮添加顺序
        self.commandBar.addAction(self.action_open)
        self.commandBar.addSeparator()
        self.commandBar.addAction(self.action_unlock)
        self.commandBar.addSeparator()
        self.commandBar.addAction(self.action_save)
        self.commandBar.addAction(self.action_export)
        self.commandBar.addSeparator()

        # 初始按钮状态
        self.action_unlock.setEnabled(False)
        self.action_save.setEnabled(False)
        self.action_export.setEnabled(False)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(10, 10, 10, 10)
        lay.setAlignment(Qt.AlignTop)
        lay.addWidget(self.TitleLabel)
        lay.addWidget(self.file_label)
        lay.addWidget(self.commandBar)
        lay.addWidget(self.text_edit, 1)

        self.current_file: Optional[str] = None
