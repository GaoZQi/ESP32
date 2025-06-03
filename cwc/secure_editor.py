import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QFileDialog, QMessageBox,
    QAction, QPushButton, QVBoxLayout, QWidget
)
import secure_core as core

class SecureEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("文档安全加密编辑器")
        self.setGeometry(300, 200, 800, 600)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

        self.edit_button = QPushButton("编辑解锁")
        self.edit_button.setEnabled(False)
        self.edit_button.clicked.connect(self.unlock_edit)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.edit_button)

        self.setCentralWidget(central_widget)

        self.current_file = None
        self.init_menu()

    def init_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("文件")

        open_action = QAction("打开文件", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("保存并加密", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "打开文件")
        if not path:
            return
        self.current_file = path
        try:
            _ = core.load_file(path)
            self.text_edit.setPlainText("[受控文件已加载，点击“编辑解锁”以查看明文]")
            self.text_edit.setReadOnly(True)
            self.edit_button.setEnabled(True)
            core.write_log("打开文件", path, "成功")
        except ValueError as ve:
            msg = str(ve)
            if "篡改" in msg:
                QMessageBox.critical(self, "警告", f"{msg}")
                core.write_log("打开文件", path, f"失败（{msg}）")
            elif "不是受控文件" in msg:
                reply = QMessageBox.question(
                    self, "提示", "无法识别为受控文件，是否作为新建文件使用？",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    self.text_edit.setPlainText("")
                    self.text_edit.setReadOnly(False)
                    self.edit_button.setEnabled(False)
                    core.write_log("打开非受控文件", path, "作为新建打开")
                else:
                    core.write_log("打开文件", path, "取消")
            else:
                QMessageBox.warning(self, "错误", msg)
                core.write_log("打开文件", path, f"失败（{msg}）")
        except Exception as e:
            QMessageBox.warning(self, "错误", f"打开文件失败：{e}")
            core.write_log("打开文件", path, f"失败（异常：{e}）")

    def unlock_edit(self):
        try:
            content = core.load_file(self.current_file)
            self.text_edit.setPlainText(content)
            self.text_edit.setReadOnly(False)
            self.edit_button.setEnabled(False)
            QMessageBox.information(self, "成功", "文件已解锁，可编辑")
            core.write_log("解锁编辑", self.current_file, "成功")
        except ValueError as ve:
            QMessageBox.critical(self, "解锁失败", str(ve))
            core.write_log("解锁编辑", self.current_file, f"失败（{ve}）")
        except Exception as e:
            QMessageBox.warning(self, "解密失败", f"解密失败：{e}")
            core.write_log("解锁编辑", self.current_file, f"失败（异常：{e}）")

    def save_file(self):
        if not self.current_file:
            path, _ = QFileDialog.getSaveFileName(self, "保存文件")
            if not path:
                return
            self.current_file = path

        try:
            content = self.text_edit.toPlainText()
            core.save_file(self.current_file, content)
            self.text_edit.setReadOnly(True)
            self.edit_button.setEnabled(True)
            QMessageBox.information(self, "保存成功", "文件已加密保存")
            core.write_log("保存并加密", self.current_file, "成功")
        except Exception as e:
            QMessageBox.critical(self, "保存失败", f"错误：{e}")
            core.write_log("保存并加密", self.current_file, f"失败（异常：{e}）")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = SecureEditor()
    editor.show()
    sys.exit(app.exec_())
