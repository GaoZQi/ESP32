# src/widget/secure_editor_tab.py
import os, sys
from typing import Optional
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QPushButton,
    QFileDialog,
    QMessageBox,
)
import src.algorithms.SecureEditor.secure_core as core


class SecureEditorTab(QWidget):
    """轻量版 – 可直接嵌入原前端。"""

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setObjectName("SecureEditorTab")
        self.current_file: Optional[str] = None

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        self.btn_unlock = QPushButton("编辑解锁", self)
        self.btn_unlock.setEnabled(False)
        self.btn_unlock.clicked.connect(self.unlock_edit)

        self.btn_open = QPushButton("📂", self)
        self.btn_open.setToolTip("打开文件")
        self.btn_open.clicked.connect(self.open_file)

        self.btn_save = QPushButton("💾", self)
        self.btn_save.setToolTip("保存并加密")
        self.btn_save.clicked.connect(self.save_file)

        bar = QHBoxLayout()
        bar.setSpacing(6)
        bar.addWidget(self.btn_open)
        bar.addWidget(self.btn_save)
        bar.addStretch()
        bar.addWidget(self.btn_unlock)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(10, 10, 10, 10)
        lay.setSpacing(8)
        lay.addLayout(bar)
        lay.addWidget(self.text_edit, 1)

    # ----- 业务 -----
    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "打开文件")
        if not path:
            return
        self.current_file = path
        try:
            core.load_file(path)  # 仅验证
            self.text_edit.setPlainText("受控文件已加载，点击“编辑解锁”以查看明文")
            self.text_edit.setReadOnly(True)
            self.btn_unlock.setEnabled(True)
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
            self.btn_unlock.setEnabled(False)
            QMessageBox.information(self, "成功", "文件已解锁，可编辑")
            core.write_log("解锁编辑", self.current_file, "成功")
        except Exception as e:
            self._err("解锁失败", str(e))

    def save_file(self):
        if not self.current_file:
            p, _ = QFileDialog.getSaveFileName(self, "保存文件")
            if not p:
                return
            self.current_file = p
        try:
            core.save_file(self.current_file, self.text_edit.toPlainText())
            self.text_edit.setReadOnly(True)
            self.btn_unlock.setEnabled(True)
            QMessageBox.information(self, "保存成功", "文件已加密保存")
            core.write_log("保存并加密", self.current_file, "成功")
        except Exception as e:
            self._err("保存失败", str(e))

    # ----- 辅助 -----
    def _handle_open_error(self, path: str, ve: ValueError):
        msg = str(ve)
        if "篡改" in msg:
            QMessageBox.critical(self, "警告", msg)
        elif "不是受控文件" in msg:
            if (
                QMessageBox.question(
                    self,
                    "提示",
                    "识别失败，作为新建文件打开？",
                    QMessageBox.Yes | QMessageBox.No,
                )
                == QMessageBox.Yes
            ):
                self.text_edit.clear()
                self.text_edit.setReadOnly(False)
                self.btn_unlock.setEnabled(False)
                return
        else:
            QMessageBox.warning(self, "错误", msg)
        core.write_log("打开文件", path, f"失败（{msg}）")

    def _err(self, title: str, detail: str):
        QMessageBox.critical(self, title, detail)
        if self.current_file:
            core.write_log(title, self.current_file, f"失败（{detail}）")
