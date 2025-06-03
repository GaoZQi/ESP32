# coding:utf-8

import sys


from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QColor, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication

from qfluentwidgets import (
    FluentWindow,
    FluentIcon,
    setThemeColor,
    SystemThemeListener,
    isDarkTheme,
    setTheme,
    Theme,
)
from qframelesswindow.utils import getSystemAccentColor

from DataHandle import DataHandleTab
from DataMasking import DataMaskingTab
from widget.secure_editor_tab import SecureEditorTab

from mod.QSSLoader import QSSLoader
from mod.Fluent3Icon import Fluent3Icon


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.themeListener = SystemThemeListener(self)
        self.setWindowTitle("Encryption & Security Platform 32")
        self.setWindowIcon(QIcon("../res/icons/favicon.png"))
        self.setMinimumSize(900, 600)
        self.navigationInterface.setExpandWidth(200)
        # 添加子界面
        self.data_tab = DataHandleTab()
        self.masking_tab = DataMaskingTab()
        self.editor_tab = SecureEditorTab()
        self.addSubInterface(
            self.data_tab, Fluent3Icon.fromName("PrintfaxPrinterFile"), "文档水印加解密"
        )
        self.addSubInterface(
            self.masking_tab, Fluent3Icon.fromName("Fingerprint"), "敏感数据识别及脱敏"
        )
        self.addSubInterface(
            self.editor_tab, Fluent3Icon.fromName("ProtectedDocument"), "文档透明加密"
        )
        self.themeListener.start()

    def closeEvent(self, e):
        # 停止监听器线程
        self.themeListener.terminate()
        self.themeListener.deleteLater()
        super().closeEvent(e)

    def _onThemeChangedFinished(self):
        super()._onThemeChangedFinished()

        # 云母特效启用时需要增加重试机制
        if self.isMicaEffectEnabled():
            QTimer.singleShot(
                100,
                lambda: self.windowEffect.setMicaEffect(self.winId(), isDarkTheme()),
            )


if __name__ == "__main__":
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    # 只能获取 Windows 和 macOS 的主题色
    if sys.platform in ["win32", "darwin"]:
        setThemeColor(getSystemAccentColor(), save=False)
        setTheme(Theme.AUTO)

    app = QApplication(sys.argv)
    # app.setStyleSheet(QSSLoader.load_qss_files("../style"))
    # font = QFont("Microsoft YaHei UI", 8)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
