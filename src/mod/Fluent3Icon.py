import os
from qfluentwidgets import FluentFontIconBase, Theme


class Fluent3Icon(FluentFontIconBase):
    """Custom icon font icon"""

    def path(self, theme=Theme.AUTO):
        # 获取当前脚本所在目录
        base_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_dir, "font", "Segoe Fluent Icons.ttf")

    def iconNameMapPath(self):
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "font",
            "fontNameMap.json",
        )
