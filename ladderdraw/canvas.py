# -*- coding: utf-8 -*-
# File  : canvas.py
# Author: Meijin Lu
# Date  : 2021/4/6
"""Matplotlib + PyQt5 绘图控件层（仅负责显示，不含计算逻辑）。

计算（Point / 曲线 / 理论塔板数）见 :mod:`ladderdraw.core`。

matplotlib 常用对象:
    Figure ---> 面板 / 画板
    Axes   ---> 子图 / 画布 / 画纸
    Axis   ---> 坐标轴对象（刻度线、刻度文本、网格、标题等）

缩写:
    mpl            ---> matplotlib
    FigureCanvas   ---> FigureCanvasQTAgg
"""
import sys

import matplotlib
import matplotlib.font_manager
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QSizePolicy, QWidget)


# 按平台顺序尝试的中文字体；找到第一个系统可用的即采用
_CJK_FONT_CANDIDATES = [
    "SimHei", "Microsoft YaHei",                 # Windows
    "PingFang SC", "Heiti SC", "STHeiti",        # macOS
    "Noto Sans CJK SC", "Source Han Sans SC",    # Linux (常见)
    "WenQuanYi Zen Hei", "WenQuanYi Micro Hei",  # Linux (文泉驿)
    "Arial Unicode MS",                          # 跨平台兜底
]


def _pick_cjk_font():
    """返回系统里第一个可用的中文字体名；都没有则返回 None。"""
    available = {f.name for f in matplotlib.font_manager.fontManager.ttflist}
    for name in _CJK_FONT_CANDIDATES:
        if name in available:
            return name
    return None


def setup_chinese_font():
    """配置 matplotlib 中文显示，跨平台自动回退（不再硬编码 SimHei）。"""
    cjk = _pick_cjk_font()
    if cjk:
        matplotlib.rcParams['font.sans-serif'] = (
            [cjk] + matplotlib.rcParams['font.sans-serif']
        )
    matplotlib.rcParams['axes.unicode_minus'] = False


class MyMplCanvas(FigureCanvas):
    """画布基类"""

    def __init__(self, parent=None, width=8, height=7, dpi=110, **kwargs):
        setup_chinese_font()
        self.fig = Figure(figsize=(width, height), dpi=dpi, constrained_layout=True,
                          facecolor='#f9f9f9')
        self.axes = self.fig.add_subplot(111)
        self.axes.set_facecolor('#fefefe')

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class MatplotlibWidget(QWidget):
    """将绘图类和工具栏封装到窗体中"""

    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)
        self.initUi()

    def initUi(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.mpl = MyMplCanvas(self, width=8, height=7, dpi=110)
        self.mpl_ntb = NavigationToolbar(self.mpl, self)

        self.layout.addWidget(self.mpl)
        self.layout.addWidget(self.mpl_ntb)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MatplotlibWidget()
    ui.show()
    sys.exit(app.exec_())
