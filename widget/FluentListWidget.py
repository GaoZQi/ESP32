import sys
from PyQt5.QtWidgets import (
    QApplication,
    QListWidget,
    QListWidgetItem,
    QStyledItemDelegate,
    QStyle,
    QWidget,
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QPainter


class CustomDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        painter.save()

        # 设置背景和选中状态
        is_selected = option.state & QStyle.State_Selected
        is_hover = option.state & QStyle.State_MouseOver

        # 绘制背景
        if is_selected or is_hover:
            bg_color = (
                QColor(255, 255, 255, 190)
                if is_selected
                else QColor(240, 240, 240, 190)
            )
            painter.setBrush(bg_color)
            painter.setPen(Qt.NoPen)

            # 创建圆角矩形背景
            bg_rect = option.rect.adjusted(2, 2, -2, -2)
            painter.drawRoundedRect(bg_rect, 10, 10)

        # 绘制文本（四周保留15px边距）
        text = index.data(Qt.DisplayRole)
        text_rect = option.rect.adjusted(10, 10, -10, -10)
        painter.setPen(Qt.black)
        painter.drawText(text_rect, Qt.AlignCenter, text)

        painter.restore()

    def sizeHint(self, option, index):
        return QSize(0, 40)  # 固定高度为60px


class FluentListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setItemDelegate(CustomDelegate(self))
        self.setSpacing(0)
        self.init_style()
        self.setMinimumWidth(175)
        self.setMaximumWidth(200)

    def init_style(self):
        self.setStyleSheet(
            """
            QListWidget {
                background: transparent;
                border: none;
                outline: 0;
                margin: 0px;
                font-size: 12px;
                font-weight: 600;
            }
            QListWidget::item {
                border: none;
                margin: 2px 5px;
                padding: 2px 5px;
            }
        """
        )
        self.viewport().setStyleSheet("background: transparent;")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 创建半透明窗口用于演示效果
    window = QWidget()
    window.setAttribute(Qt.WA_TranslucentBackground)
    window.setStyleSheet("background: rgba(255,255,255, 150);")
    window.resize(300, 300)

    # 创建并设置列表控件
    list_widget = FluentListWidget(window)
    list_widget.resize(250, 250)
    list_widget.move(25, 25)

    # 添加示例项
    for i in range(5):
        item = QListWidgetItem(f"List Item {i+1}")
        item.setSizeHint(QSize(0, 40))  # 确保项高度与代理一致
        list_widget.addItem(item)

    window.show()
    sys.exit(app.exec_())
