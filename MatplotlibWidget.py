# -*- coding: utf-8 -*-
# File  : MatplotlibWidget.py
# Author: Meijin Lu
# Date  : 2021/4/6
import sys
import matplotlib.pyplot as plt
import sympy
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QSizePolicy, QMessageBox, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
t = sympy.Symbol("t")
"""
matplotlib常用对象:
Figure--->面板,画板
Axes--->子图,画布,画纸
Axis--->坐标轴对象
Axis容器包括坐标轴上的刻度线、刻度文本、坐标网格以及坐标轴标题等内容。
在本文件中,MatplotlibWidget表示绘图窗体,装载有 Figure对象

缩写:
mpl--->matplotlib
plt--->matplotlib.pyplot
FigureCanvas--->FigureCanvasQTAgg
"""


class Point():
    """点,交点等"""

    def __init__(self, *args):
        self.coordinate = (args[0], args[1])

    def get_coordinate(self):
        return self.coordinate

    def get_x(self):
        return self.coordinate[0]

    def get_y(self):
        return self.coordinate[1]


class PhaseQuilibriumLine():
    """平衡线类"""

    def __init__(self, alpha):
        self.alpha = alpha

    def func(self):
        a = self.alpha
        return a * t / (1 + (a - 1) * t)


class StraightLine():
    """直线类,如精馏线,对角线,提馏线"""

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def func(self):
        a = self.a
        b = self.b
        return a * t + b


class MyMplCanvas(FigureCanvas):
    """画布基类"""
    def __init__(self, parent=None, width=10, height=8, dpi=100, **kwargs):
        # 设置中文显示
        plt.rcParams['font.family'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        # 新建一个绘图对象
        self.fig = Figure(figsize=(width, height), dpi=dpi, constrained_layout=True)
        # 一个画图区域
        self.axes = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        # 定义FigureCanvas的尺寸策略
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class MatplotlibWidget(QWidget):
    """将绘图类和工具栏封装到窗体中"""

    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)
        self.initUi()

    def initUi(self):
        self.layout = QVBoxLayout(self)
        self.mpl = MyMplCanvas(self, width=10, height=8, dpi=100)
        self.mpl_ntb = NavigationToolbar(self.mpl, self)

        self.layout.addWidget(self.mpl)
        self.layout.addWidget(self.mpl_ntb)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MatplotlibWidget()
    ui.mpl.start_plot()
    ui.show()
    sys.exit(app.exec_())
