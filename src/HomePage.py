import sys
import os

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QListWidget,
    QListWidgetItem,
    QStackedWidget,
)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy

from qfluentwidgets import (
    ElevatedCardWidget,
    ImageLabel,
    CaptionLabel,
    FluentIcon,
    TitleLabel,
    BodyLabel,
    StrongBodyLabel,
    FlowLayout,
)

from template import *


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("HomePageTab")
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(20, 20, 20, 10)
        mainLayout.setAlignment(Qt.AlignTop)

        title = TitleLabel("加密安全工作台 32")
        subtitle1 = StrongBodyLabel("简介")
        description = BodyLabel(
            "本工作台旨在提供一个集成的加密和安全平台，支持多种加密算法和数据处理功能。"
            "用户可以通过简单的界面进行数据加密、解密、数据掩码处理等操作，"
            "并且支持多种文件格式的处理。"
            "工作台还提供了文档透明加密编辑器，"
            "使用户能够在加密状态下编辑文档，确保数据的安全性和隐私保护。"
        )
        description.setWordWrap(True)
        description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        subtitle2 = StrongBodyLabel("主要功能")

        # 获取当前运行路径，无论是.py还是.exe都能适配
        if getattr(sys, "frozen", False):
            BASE_DIR = os.path.dirname(sys.executable)
        else:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        RED_PATH = os.path.join(BASE_DIR, "res", "pic", "file.png")
        BLU_PATH = os.path.join(BASE_DIR, "res", "pic", "card.png")
        GRE_PATH = os.path.join(BASE_DIR, "res", "pic", "chat.png")

        emojiCard1 = EmojiCard(RED_PATH, "文档水印加解密")
        emojiCard2 = EmojiCard(BLU_PATH, "敏感数据识别及脱敏")
        emojiCard3 = EmojiCard(GRE_PATH, "文档透明加密")

        mainLayout.addWidget(title)
        mainLayout.addWidget(subtitle1)
        mainLayout.addWidget(description)
        mainLayout.addWidget(subtitle2)

        self.flowLayout = FlowLayout()
        self.flowLayout.setSpacing(6)
        self.flowLayout.setAlignment(Qt.AlignVCenter)
        self.flowLayout.addWidget(emojiCard1)
        self.flowLayout.addWidget(emojiCard2)
        self.flowLayout.addWidget(emojiCard3)
        mainLayout.addLayout(self.flowLayout)


class EmojiCard(ElevatedCardWidget):

    def __init__(self, iconPath: str, name: str, parent=None):
        super().__init__(parent)
        self.iconWidget = ImageLabel(iconPath, self)
        self.label = CaptionLabel(name, self)

        self.iconWidget.scaledToHeight(68)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setAlignment(Qt.AlignCenter)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.iconWidget, 0, Qt.AlignCenter)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.label, 0, Qt.AlignHCenter | Qt.AlignBottom)

        self.setFixedSize(168, 176)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet("QWidget { background-color: #f0f0f0; }")

    mainWindow = HomePage()
    mainWindow.setWindowTitle("Data Masking Tab Example")
    mainWindow.setGeometry(100, 100, 800, 600)

    mainWindow.show()

    sys.exit(app.exec_())
