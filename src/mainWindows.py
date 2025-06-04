# coding:utf-8

import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QMainWindow, QApplication

from qfluentwidgets import (
    FluentWindow,
    FluentIcon,
    setThemeColor,
    SystemThemeListener,
    isDarkTheme,
    setTheme,
    Theme,
    qconfig,
)

from qframelesswindow.utils import getSystemAccentColor

# from DataHandle import DataHandleTab

# from DataMasking import DataMaskingTab
from SecureEditor import SecureEditorTab

from mod.Fluent3Icon import Fluent3Icon


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Encryption & Security Platform 32")
        import os

        # 获取当前运行路径，无论是.py还是.exe都能适配
        if getattr(sys, "frozen", False):
            BASE_DIR = os.path.dirname(sys.executable)
        else:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        ICON_PATH = os.path.join(BASE_DIR, "res", "icons", "favicon.png")

        self.setWindowIcon(QIcon(ICON_PATH))
        self.setMinimumSize(900, 600)
        self.navigationInterface.setExpandWidth(200)

        # 添加子界面
        # self.data_tab = DataHandleTab()
        # self.masking_tab = DataMaskingTab()
        self.editor_tab = SecureEditorTab()

        # self.addSubInterface(
        #     self.data_tab, Fluent3Icon.fromName("PrintfaxPrinterFile"), "文档水印加解密"
        # )
        # self.addSubInterface(
        #     self.masking_tab, Fluent3Icon.fromName("Fingerprint"), "敏感数据识别及脱敏"
        # )
        self.addSubInterface(
            self.editor_tab, Fluent3Icon.fromName("ProtectedDocument"), "文档透明加密"
        )

        # 启动系统主题监听器
        self.themeListener = SystemThemeListener(self)
        self.themeListener.start()

        # 初次保存当前系统主题色
        self._lastSystemColor = getSystemAccentColor()

        # 启动定时检测系统主题色变化（增强兼容性）
        self._themeColorTimer = QTimer(self)
        self._themeColorTimer.timeout.connect(self.checkSystemAccentColor)
        self._themeColorTimer.start(5000)

        # 注册主题色变化的槽函数
        qconfig.themeColorChanged.connect(self.onThemeColorChanged)

    def closeEvent(self, e):
        self.themeListener.terminate()
        self.themeListener.deleteLater()
        super().closeEvent(e)

    def _onThemeChangedFinished(self):
        super()._onThemeChangedFinished()
        if self.isMicaEffectEnabled():
            QTimer.singleShot(
                100,
                lambda: self.windowEffect.setMicaEffect(self.winId(), isDarkTheme()),
            )

    def checkSystemAccentColor(self):
        """定时检测系统主题色变化"""
        currentColor = getSystemAccentColor()
        setTheme(Theme.AUTO)
        if currentColor != self._lastSystemColor:
            print(f"[系统主题色变化] -> {currentColor.name()}")
            setThemeColor(currentColor, save=False)
            self._lastSystemColor = currentColor

    def onThemeColorChanged(self, color: QColor):
        """监听主题色变化后执行的操作"""
        print(f"[监听] 当前主题色已更新为：{color.name()}")
        # 可以在这里刷新所有依赖主题色的组件，比如按钮样式、背景等
        # 示例：self.data_tab.updateStyle(color.name()) （你可以定义这个方法）
        pass


if __name__ == "__main__":
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # 设置初始主题色和主题风格
    if sys.platform in ["win32", "darwin"]:
        setThemeColor(getSystemAccentColor(), save=False)
        setTheme(Theme.AUTO)

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
