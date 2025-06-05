# coding:utf-8

import sys
import os

from PyQt5.QtCore import Qt, QTimer, QSize, QEventLoop
from PyQt5.QtGui import QIcon, QColor, QFont
from PyQt5.QtWidgets import QApplication

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


from qfluentwidgets import SplashScreen
from qframelesswindow import FramelessWindow, StandardTitleBar

from qframelesswindow.utils import getSystemAccentColor

from DataHandle import DataHandleTab
from DataMasking import DataMaskingTab
from SecureEditor import SecureEditorTab
from HomePage import HomePage

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
        self.home_tab = HomePage()
        self.data_tab = DataHandleTab()
        self.masking_tab = DataMaskingTab()
        self.editor_tab = SecureEditorTab()

        self.addSubInterface(self.home_tab, FluentIcon.HOME, "首页")
        self.addSubInterface(
            self.data_tab, Fluent3Icon.fromName("PrintfaxPrinterFile"), "文档水印加解密"
        )
        self.addSubInterface(
            self.masking_tab, Fluent3Icon.fromName("Fingerprint"), "敏感数据识别及脱敏"
        )
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


class StartView(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.resize(700, 600)
        self.setWindowTitle("Encryption & Security Platform 32")
        # 获取当前运行路径，无论是.py还是.exe都能适配
        if getattr(sys, "frozen", False):
            BASE_DIR = os.path.dirname(sys.executable)
        else:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        ICON_PATH = os.path.join(BASE_DIR, "res", "pic", "title.png")

        self.setWindowIcon(QIcon(ICON_PATH))

        # 1. 创建启动页面
        self.setFixedSize(600, 327)
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(512, 112))
        self.splashScreen.show()

        # 启动定时器，等待一段时间后关闭启动界面并打开主窗口
        QTimer.singleShot(3, self.showMainWindow)

    def showMainWindow(self):
        """关闭启动界面并显示主窗口"""
        self.mainWindow = MainWindow()
        self.mainWindow.show()
        self.close()


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
    app.setStyleSheet(
        """
        QWidget {
            font-family: "Microsoft YaHei UI";
        }
        QLabel {
            margin: 5px 0px;
        }
        """
    )
    font = QFont("Microsoft YaHei UI")
    font.setHintingPreference(QFont.PreferNoHinting)
    app.setFont(font)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    # 在入口文件顶部添加
    if getattr(sys, "frozen", False):
        APP_BASE_DIR = os.path.dirname(sys.executable)
    else:
        APP_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # 设置全局环境变量（可选方案）
    os.environ["APP_BASE_DIR"] = APP_BASE_DIR
    # 创建并显示启动界面
    start = StartView()
    start.show()

    sys.exit(app.exec_())
