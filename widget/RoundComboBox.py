from PyQt5.QtWidgets import QComboBox, QStyledItemDelegate
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QFont
from PyQt5.QtWidgets import QStyle


class ComboBoxItemDelegate(QStyledItemDelegate):
    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        size.setHeight(35)  # 增加高度留出阴影空间
        return size

    def paint(self, painter, option, index):
        painter.setRenderHint(QPainter.Antialiasing)

        # 原始项尺寸
        original_rect = option.rect

        # 绘制背景
        bg_color = (
            QColor("#f0f0f0")
            if option.state & QStyle.State_Selected
            else QColor("#fdfdfd")
        )
        painter.setBrush(bg_color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(original_rect, 5, 5)

        # 绘制文本
        text_rect = original_rect.adjusted(12, 0, -7, 0)
        painter.setPen(QColor("#1a1a1a"))
        painter.drawText(
            text_rect, Qt.AlignLeft | Qt.AlignVCenter, index.data(Qt.DisplayRole)
        )


class RoundComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_styles()
        self.setItemDelegate(ComboBoxItemDelegate(self))

        # 初始化字体
        self.icon_font = QFont("Segoe Fluent Icons")
        self.icon_font.setPixelSize(12)  # 控制图标大小

    def setup_styles(self):
        self.setFixedHeight(35)
        self.setStyleSheet(
            """
            QComboBox {
                padding-left: 15px;
                color: #1a1a1a;
                background-color: #fdfdfd;
            }
            QComboBox::drop-down { 
                width: 40px;
                border: none; 
            }
            /* 下拉列表样式 */
            QComboBox QAbstractItemView {
                background-color: transparent;
                border: 2px solid #f1f1f1;
                border-radius: 10px;
                outline: none;
            }
            /* 滚动条样式 */
            QScrollBar:vertical {
                background: transparent;
                width: 5px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #cccccc;
                border-radius: 5px;
                min-height: 15px;
            }
            QScrollBar::add-line:vertical, 
            QScrollBar::sub-line:vertical {
                height: 0px;
                background: none;
            }
            QScrollBar::add-page:vertical, 
            QScrollBar::sub-page:vertical {
                background: none;
            }
        """
        )

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制背景
        bg_rect = self.rect().adjusted(1, 1, -1, -1)
        painter.setBrush(QBrush(QColor("#fdfdfd")))
        painter.setPen(QPen(QColor("#f1f1f1"), 2))
        painter.drawRoundedRect(bg_rect, 10, 10)

        # 绘制当前选中项文本
        text_rect = QRect(15, 0, self.width() - 35, self.height())
        painter.setPen(QColor("#1a1a1a"))
        painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, self.currentText())

        # 绘制字体图标箭头
        painter.save()
        painter.setFont(self.icon_font)
        painter.setPen(QColor("#1a1a1a"))

        # 计算图标位置
        icon_rect = QRect(self.width() - 30, 0, 24, self.height())
        painter.drawText(icon_rect, Qt.AlignCenter, "\uf08e")  # 使用Unicode字符
        painter.restore()


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    combo = RoundComboBox()
    combo.addItems([f"Option {i}" for i in range(1, 20)])
    combo.show()
    sys.exit(app.exec_())
