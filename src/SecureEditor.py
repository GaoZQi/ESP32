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


class SecureEditorTab(QWidget):
    """轻量版 – 可直接嵌入原前端。"""

    def __init__(self):
        super().__init__()
        self.setObjectName("SecureEditorTab")

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

    # ----- 新增 新建文件逻辑 -----
    def new_file(self):
        # 弹出“保存为”对话框，默认后缀txt
        path, _ = QFileDialog.getSaveFileName(
            self, "新建文件", "", "文本文件 (*.txt);;"
        )
        if not path:
            return
        # 确保文件有txt后缀
        if not path.endswith(".txt"):
            path += ".txt"

        # 创建空白文件
        try:
            with open(path, "w", encoding="utf-8") as f:
                pass  # 创建空文件
            self.file_label.setText(f"当前文件：{os.path.basename(path)}")
        except Exception as e:
            self._err("新建文件失败", f"无法创建文件：{e}")
            return

        self.current_file = path
        self.text_edit.clear()  # 清空文本编辑器
        self.text_edit.setReadOnly(False)  # 进入编辑状态

        # 按钮状态调整
        self.action_unlock.setEnabled(False)  # 新文件无需解锁
        self.action_save.setEnabled(True)  # 可保存
        self.action_export.setEnabled(False)  # 导出不可用（没加密文件）

        core.write_log("新建文件", path, "成功")

    # 下面是已有方法，保持不变
    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "打开文件", "", "受控文件 (*.sec);;"
        )
        if not path:
            return

        self.current_file = path
        self.action_export.setEnabled(False)  # 禁用导出按钮（直到解锁）
        try:
            core.load_file(path)  # 验证合法性
            self.text_edit.setPlainText("受控文件已加载，点击“编辑解锁”以查看明文")
            self.text_edit.setReadOnly(True)
            self.action_unlock.setEnabled(True)
            self.action_save.setEnabled(False)  # 打开时不可保存
            self.file_label.setText(f"当前文件：{os.path.basename(path)}")
            core.write_log("打开文件", path, "成功")
        except ValueError as ve:
            self._handle_open_error(path, ve)
        except Exception as e:
            self._err("打开文件", f"异常：{e}")

    def unlock_edit(self):
        if not self.current_file:
            return
        try:
            txt = core.load_file(self.current_file)
            self.text_edit.setPlainText(txt)
            self.text_edit.setReadOnly(False)
            self.action_unlock.setEnabled(False)
            self.action_save.setEnabled(True)
            self.action_export.setEnabled(True)  # 解锁后允许导出

            Flyout.create(
                icon=InfoBarIcon.SUCCESS,
                title="解锁成功",
                content="文件已解锁，可编辑。",
                target=self.commandBar,
                parent=self,
                isClosable=True,
                aniType=FlyoutAnimationType.DROP_DOWN,
            )
            core.write_log("解锁编辑", self.current_file, "成功")
        except Exception as e:
            self._err("解锁失败", str(e))

    def save_file(self):
        if not self.current_file:
            return

        # 自动添加 .sec 后缀（如果没有）
        if not self.current_file.endswith(".sec"):
            new_path = self.current_file + ".sec"
        else:
            new_path = self.current_file

        try:
            core.save_file(new_path, self.text_edit.toPlainText())

            # 删除原始文件（如果是另一个）
            if new_path != self.current_file and os.path.exists(self.current_file):
                os.remove(self.current_file)

            self.current_file = new_path
            self.text_edit.setReadOnly(True)
            self.action_unlock.setEnabled(False)
            self.action_save.setEnabled(False)
            self.action_export.setEnabled(False)
            self.file_label.setText("")
            self.text_edit.clear()

            Flyout.create(
                icon=InfoBarIcon.SUCCESS,
                title="保存成功",
                content=f"文件已保存为：{os.path.basename(new_path)}",
                target=self.commandBar,
                parent=self,
                isClosable=True,
                aniType=FlyoutAnimationType.DROP_DOWN,
            )
            core.write_log("保存并加密", new_path, "成功")

        except Exception as e:
            self._err("保存失败", str(e))

    def export_file(self):
        if not self.current_file or self.text_edit.isReadOnly():
            return

        # 去掉 .sec 后缀
        if self.current_file.endswith(".sec"):
            export_path = self.current_file[:-4]
        else:
            export_path = self.current_file + ".export.txt"

        try:
            with open(export_path, "w", encoding="utf-8") as f:
                f.write(self.text_edit.toPlainText())

            Flyout.create(
                icon=InfoBarIcon.SUCCESS,
                title="导出成功",
                content=f"明文已导出为：{os.path.basename(export_path)}",
                target=self.commandBar,
                parent=self,
                isClosable=True,
                aniType=FlyoutAnimationType.DROP_DOWN,
            )
            core.write_log("导出明文", export_path, "成功")
        except Exception as e:
            self._err("导出失败", str(e))

    def _handle_open_error(self, path: str, ve: ValueError):
        msg = str(ve)
        if "篡改" in msg:
            box = MessageBox("警告", msg, self)
            box.yesButton.setText("是")
            box.cancelButton.setText("否")
            box.exec()
        elif "不是受控文件" in msg:
            box = MessageBox("提示", "识别失败，作为新建文件打开？", self)
            box.yesButton.setText("是")
            box.cancelButton.setText("否")
            if box.exec():
                self.text_edit.clear()
                self.text_edit.setReadOnly(False)
                self.action_unlock.setEnabled(False)
                self.action_save.setEnabled(True)
                return
        else:
            box = MessageBox("错误", msg, self)
            box.yesButton.setText("是")
            box.cancelButton.setText("否")
            box.exec()
        core.write_log("打开文件", path, f"失败（{msg}）")

    def _err(self, title: str, content: str):
        # Flyout.create(
        #     icon=InfoBarIcon.ERROR,
        #     title=title,
        #     content=content,
        #     target=self.commandBar,
        #     parent=self,
        #     isClosable=True,
        #     aniType=FlyoutAnimationType.DROP_DOWN,
        # )
        pass
