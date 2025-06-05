from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout
from PyQt5.QtCore import Qt

from qfluentwidgets import SegmentedWidget

from template import *

from algorithms.DataEncode import BlindWaterMarkEnc, BlindWaterMarkDec, PeanoEnc, PeanoDec, SimpleScaleDownEnc, SimpleScaleDownDec, Novel_to_ImageEnc, Novel_to_ImageDec, GilbertEnc, GilbertDec, CloackedPixelEnc, CloackedPixelDec

def init_func(func):
    return func.get_encoder().encode()
class DataHandleTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("DataHandleTab")

        self.mode = SegmentedWidget(self)
        self.stack = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)

        self.vBoxLayout.setContentsMargins(20, 10, 20, 20)
        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.addWidget(self.mode, 0, Qt.AlignHCenter)
        self.vBoxLayout.addWidget(self.stack)
        self.setLayout(self.vBoxLayout)

        items = [
            {
                "title": "BilndWaterMark",
                "func_name": "",
                "enc_script": BlindWaterMarkEnc.get_encoder(),
                "dec_script": BlindWaterMarkDec.get_decoder(),
                "widget": CLI2Tab,
            },
            {
                "title": "Peano",
                "func_name": "",
                "enc_script": PeanoEnc.get_encoder(),
                "dec_script": PeanoDec.get_decoder(),
                "widget": CLITEXTTab
            },
            {
                "title": "SampleScaleDown",
                "func_name": "",
                "enc_script": SimpleScaleDownEnc.get_encoder(),
                "dec_script": SimpleScaleDownDec.get_decoder(),
                "widget": CLI3Tab,
            },
            {
                "title": "Novel_To_Image",
                "func_name": "",
                "enc_script": Novel_to_ImageEnc.get_encoder(),
                "dec_script": Novel_to_ImageDec.get_decoder(),
                "widget": CLITEXTTab,
            },
            {
                "title": "Gilbert",
                "func_name": "",
                "enc_script": GilbertEnc.get_encoder(),
                "dec_script": GilbertDec.get_decoder(),
                "widget": CLI1Tab
            },
            {
                "title": "Cloacked-pixel",
                "func_name": "",
                "enc_script": CloackedPixelEnc.get_encoder(),
                "dec_script": CloackedPixelDec.get_decoder(),
                "widget": CLITEXT2Tab,
            },
        ]

        # 添加页面与标签项
        for item in items:
            if item["widget"] is CLI2Tab or item["widget"] is CLI3Tab or item["widget"] is CLITEXTTab or item["widget"] is CLI1Tab or item["widget"] is CLITEXT2Tab:
                page = item["widget"](item["title"], item["func_name"], item["enc_script"], item["dec_script"])
            else:
                page = item["widget"](item["title"], item["func_name"], item["script"])
            page.setObjectName(item["title"])  # 设置唯一标识
            self.stack.addWidget(page)
            self.mode.addItem(
                routeKey=item["title"],
                text=item["title"],
                onClick=lambda _, p=page: self.stack.setCurrentWidget(p),
            )

        # 初始化状态
        self.stack.setCurrentIndex(0)
        self.mode.setCurrentItem(self.stack.currentWidget().objectName())
