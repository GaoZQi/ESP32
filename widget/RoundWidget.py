from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPainterPath, QPen
from PyQt5.QtCore import Qt, QRectF


class RoundWidget(QWidget):
    """
    A QWidget with customizable rounded corners, background color and light gray border,
    without affecting child widget properties.

    Usage:
        widget = RoundWidget(radius=15, color=QColor(100, 150, 200))
    """

    def __init__(self, radius=10, color=QColor(255, 255, 255), flag=1, parent=None):
        super().__init__(parent)
        self._radius = radius
        self._bg_color = color
        self.flag = flag  # 1: 全圆角，2: 顶部圆角底部直角
        self._border_color = QColor("#e0e0e0")
        self._border_width = 1

    def setRadius(self, radius: int):
        """设置圆角半径（像素）"""
        self._radius = radius
        self.update()

    def setBackgroundColor(self, color: QColor):
        """设置背景颜色"""
        self._bg_color = color
        self.update()

    def setBorder(self, color: QColor, width: int = 1):
        """设置边框属性"""
        self._border_color = color
        self._border_width = width
        self.update()

    def paintEvent(self, event):
        """重绘带边框的圆角背景"""
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        # 创建0.5像素偏移的矩形用于像素对齐
        rect = QRectF(
            self._border_width / 2,
            self._border_width / 2,
            self.width() - self._border_width,
            self.height() - self._border_width,
        )

        path = QPainterPath()

        if self.flag == 1:
            # 全圆角模式
            path.addRoundedRect(rect, self._radius, self._radius)
        else:
            # 顶部圆角底部直角模式
            path.moveTo(rect.left(), rect.top() + self._radius)
            # 左上圆角
            path.arcTo(
                rect.left(), rect.top(), self._radius * 2, self._radius * 2, 180, -90
            )
            # 顶部右边
            path.lineTo(rect.right() - self._radius, rect.top())
            # 右上圆角
            path.arcTo(
                rect.right() - self._radius * 2,
                rect.top(),
                self._radius * 2,
                self._radius * 2,
                90,
                -90,
            )
            # 底部直角
            path.lineTo(rect.right(), rect.bottom())
            path.lineTo(rect.left(), rect.bottom())
            path.closeSubpath()

        # 先绘制背景
        painter.fillPath(path, self._bg_color)

        # 再绘制边框
        pen = QPen(self._border_color, self._border_width)
        pen.setCosmetic(True)  # 保持物理像素宽度
        painter.setPen(pen)
        painter.drawPath(path)

        super().paintEvent(event)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QVBoxLayout, QLabel

    app = QApplication(sys.argv)

    # 创建演示窗口
    widget = RoundWidget(radius=20, color=QColor(255, 255, 255), flag=2)
    widget.resize(300, 200)

    # 添加测试内容
    layout = QVBoxLayout(widget)
    label = QLabel("内容区域\n(带边框的圆角容器)")
    label.setAlignment(Qt.AlignCenter)
    layout.addWidget(label)

    widget.show()
    sys.exit(app.exec_())
