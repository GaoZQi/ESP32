from PyQt5.QtWidgets import QPushButton, QApplication, QWidget, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QPainterPath
from PyQt5.QtCore import Qt, QRectF, QSize


class IconButton(QPushButton):
    def __init__(
        self,
        icon_char: str,
        font_family: str = "Segoe Fluent Icons",
        tooltip: str = "",
        parent=None,
    ):
        super().__init__(parent)
        self.setToolTip(tooltip)
        self.setCursor(Qt.PointingHandCursor)

        # 颜色配置
        self.background_color = QColor("#f9f9f9")
        self.border_color = QColor("#d1d1d1")
        self.hover_color = QColor("#e0e0e0")
        self.pressed_color = QColor("#c0c0c0")
        self.icon_color = QColor("#333333")
        self.border_width = 1.5
        self.radius = 5

        # 图标配置
        self.icon_char = icon_char
        self.font_family = font_family
        self.icon_size = QSize(14, 14)  # 略微放大图标

        # 控件设置
        self.setFlat(True)
        self.setStyleSheet("border: none; background: transparent;")
        self.setAttribute(Qt.WA_Hover)
        self.setFixedSize(self.sizeHint())

    def sizeHint(self) -> QSize:
        """建议按钮尺寸调整为28x28"""
        return QSize(28, 28)

    def paintEvent(self, event):
        """优化后的绘制方法"""
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        # 计算绘制区域
        border_adjust = self.border_width / 2
        main_rect = QRectF(
            border_adjust,
            border_adjust,
            self.width() - self.border_width,
            self.height() - self.border_width,
        )
        path = QPainterPath()
        path.addRoundedRect(main_rect, self.radius, self.radius)

        # 状态颜色判断
        if self.isDown():
            bg_color = self.pressed_color
            icon_color = self.pressed_color.darker(120)
        elif self.underMouse():
            bg_color = self.hover_color
            icon_color = self.icon_color.darker(110)
        else:
            bg_color = self.background_color
            icon_color = self.icon_color

        # 绘制背景
        painter.save()
        painter.setPen(Qt.NoPen)
        painter.setBrush(bg_color)
        painter.drawPath(path)
        painter.restore()

        # 绘制边框
        if self.border_width > 0:
            painter.setPen(QPen(self.border_color, self.border_width))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(path)

        # 绘制图标
        font = QFont(self.font_family)
        font.setPixelSize(self.icon_size.height())
        painter.setFont(font)
        painter.setPen(icon_color)
        painter.drawText(self.rect(), Qt.AlignCenter, self.icon_char)


if __name__ == "__main__":
    import sys
    import os

    # 创建演示窗口
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("图标字体按钮演示")
    window.setGeometry(300, 300, 400, 300)
    layout = QVBoxLayout(window)

    # 使用FontAwesome的双箭头图标（）
    demo_icon = "\ue70f"

    # 创建按钮实例
    button = IconButton(demo_icon)
    layout.addWidget(button)
    layout.setAlignment(Qt.AlignCenter)

    # 显示窗口
    window.show()
    sys.exit(app.exec_())
