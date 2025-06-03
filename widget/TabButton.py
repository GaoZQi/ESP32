from PyQt5.QtWidgets import QPushButton, QButtonGroup
from PyQt5.QtGui import QFont, QColor, QPainter, QPainterPath, QPen
from PyQt5.QtCore import Qt, QRectF


class TabButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)

        # 背景颜色配置
        self.normal_bg = QColor(0, 0, 0, 0)  # 无背景
        self.hover_bg = QColor("#e0e0e0")  # 悬停时背景
        self.pressed_bg = QColor("#bdbdbd")  # 按下时背景
        self.checked_bg = QColor(253, 253, 253, 190)  # 选中时背景
        self.setContentsMargins(3, 3, 3, 3)  # 去除按钮内边距
        # 边框颜色配置（仅选中时显示）
        self.checked_border = QColor("#e0e0e0")

        # 文本颜色配置
        self.text_color = QColor("#424242")
        self.checked_text_color = QColor("#000000")

        # 圆角半径
        self.radius = 10

        # 字体及尺寸
        self.setMinimumSize(50, 25)
        self.setCheckable(True)
        self.setStyleSheet("border: none; background: transparent; margin: none;")
        self.setAttribute(Qt.WA_Hover)
        self.setFixedHeight(30)
        self.setFont(QFont("微软雅黑", 11))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        painter.setRenderHint(QPainter.Antialiasing, True)  # 保持开启
        painter.setRenderHint(QPainter.SmoothPixmapTransform, False)  # 关闭图片平滑
        # 使用整数像素对齐（关键修改1）
        rect = QRectF(0.5, 0.5, self.width() - 1, self.height() - 1)

        path = QPainterPath()
        path.addRoundedRect(rect, self.radius, self.radius)

        # 状态判断
        is_checked = self.isChecked()
        is_hover = self.underMouse()
        is_pressed = self.isDown()

        # 选择背景颜色
        if is_checked:
            bg_color = self.checked_bg
        elif is_pressed:
            bg_color = self.pressed_bg
        elif is_hover:
            bg_color = self.hover_bg
        else:
            bg_color = self.normal_bg

        # 填充背景
        painter.fillPath(path, bg_color)

        # 若选中，则绘制浅灰色边框
        if is_checked:
            pen = QPen(self.checked_border)
            pen.setWidth(2)
            pen.setCosmetic(True)  # 固定线宽不受缩放影响
            painter.setPen(pen)
            painter.drawPath(path)
        else:
            painter.setPen(Qt.NoPen)

        # 绘制文字（关键修改3）
        text_color = self.checked_text_color if is_checked else self.text_color
        painter.setPen(text_color)

        # 使用精确的文本位置计算
        text_rect = QRectF(0, 0, self.width(), self.height())
        font_metrics = painter.fontMetrics()
        text_width = font_metrics.horizontalAdvance(self.text())
        text_height = font_metrics.height()
        text_top = (self.height() - text_height) / 2 + font_metrics.ascent()

        painter.drawText(
            int((self.width() - text_width) / 2), int(text_top), self.text()
        )


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import (
        QApplication,
        QMainWindow,
        QVBoxLayout,
        QWidget,
        QStackedWidget,
        QHBoxLayout,
        QListWidget,
        QListWidgetItem,
        QTextEdit,
        QLineEdit,
        QPushButton,
    )
    from PyQt5.QtGui import QColor, QFont
    from PyQt5.QtCore import Qt

    app = QApplication(sys.argv)
    main_window = QMainWindow()
    main_window.setWindowTitle("TabButton Example")
    main_window.setGeometry(100, 100, 800, 600)
    button = TabButton("Tab 1")
    button.setChecked(True)
    button2 = TabButton("Tab 2")
    button3 = TabButton("Tab 3")
    center = QWidget()
    main = QHBoxLayout()
    main.addWidget(button)
    main.addWidget(button2)
    main.addWidget(button3)
    center.setLayout(main)

    main_window.setCentralWidget(center)

    main_window.show()
    sys.exit(app.exec_())
