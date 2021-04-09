# -*- coding: utf-8 -*-
# File  : LadderDraw.py
# Author: Meijin Lu
# Date  : 2021/4/6
from PyQt5.QtCore import pyqtSlot, QCoreApplication, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication
from sympy import Interval, solveset
from UiLadderDraw import Ui_MainWindow
from MatplotlibWidget import *
import numpy as np


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.txt0.setFocus()
        # 后续一定要更新下面的值
        self.d_point = Point(0.99, 0.99)
        self.w_point = Point(0.01, 0.01)
        self.q_point = Point(0.5, 0.5)
        # 初始化对角线(diagonal line),相平衡线,精馏线,提馏线,q线的方程
        self.dl = StraightLine(1, 0).func()
        self.pel = None
        self.rl = None
        self.sl = None
        self.ql = None

    @pyqtSlot()
    def on_pushButton_start_clicked(self):
        """
        整个操作中最重要的函数
        :return:
        """
        # 获取输入框中的信息,收到的值不为空则表明没有出错
        txt = self.get_txt()
        if txt is not None:
            # 相平衡线对象,一个指针,这里确定它的alpha值
            pel = PhaseQuilibriumLine(txt[0])
            self.pel = pel.func()
            # 精馏线对象,指针,确定a和b
            rl = StraightLine(txt[1],
                              txt[2])
            self.rl = rl.func()
            # q线对象,指针,确定a和b
            ql = StraightLine(txt[3],
                              txt[4])
            self.ql = ql.func()
            w = txt[5]
            self.w_point = Point(w, w)
            # 求解提馏线
            self.d_point = self.get_common_point(self.dl, self.rl)
            self.q_point = self.get_common_point(self.rl, self.ql)
            qx = self.q_point.get_x()
            qy = self.q_point.get_y()
            self.sl = w + (t - w) * (qy - w) / (qx - w)
            # 开始绘制
            self.ladder_draw()

    @pyqtSlot()
    def on_pushButton_clear_clicked(self):
        self.matplotlibwidget.mpl.axes.cla()
        self.txt0.clear()
        self.txt1.clear()
        self.txt2.clear()
        self.txt3.clear()
        self.txt4.clear()
        self.txt5.clear()
        self.txt0.setFocus()

    def get_txt(self):
        """
        判断数据,获取数据
        在本版本的pyqt5中
        QLineEdit获取文本的方法
        Text()--->text()
        """
        value_list = (self.txt0.text(),
                      self.txt1.text(),
                      self.txt2.text(),
                      self.txt3.text(),
                      self.txt4.text(),
                      self.txt5.text())
        txt = []
        for item in value_list:
            # 判断不为空,且字符串为数字
            if self.is_number(item):
                txt.append(eval(item))
            else:
                # 插眼:弹出警告框可能有问题
                QMessageBox.warning(self, '警告', '请检查输入')
                return None
        return tuple(txt)

    def is_number(self, s):
        """
        为空则直接返回False
        不为空判断是否为数字
        """
        if s is not None:
            try:
                float(s)
                return True
            except ValueError:
                pass
            try:
                import unicodedata
                unicodedata.numeric(s)
                return True
            except (TypeError, ValueError):
                pass
            return False
        else:
            return False

    def ladder_draw(self):
        """
        只要没有到达w_point,
        从d_point开始,在pel和rl之间画阶梯,
        画到q_point时,改为在pel和sl之间画阶梯。
        :return:
        """
        self.matplotlibwidget.mpl.axes.cla()
        # 画布 mpl
        mpl = self.matplotlibwidget.mpl
        # 画图区域 axes
        axes = mpl.axes
        axes.set_title("塔板阶梯图", fontsize=10)
        axes.set_ylabel("Y轴", fontsize=8)
        axes.set_xlabel("X轴", fontsize=8)
        axes.set_xlim(0, 1)
        axes.set_ylim(0, 1)
        # 画出对角线
        axes.plot([0, 1], [0, 1], color="black")
        # 画出相平衡线,精馏线,提馏线
        range_x = np.linspace(0, 1, 100)
        range_pel_y = np.array([self.pel.evalf(subs={t: i}) for i in range_x])
        axes.plot(range_x, range_pel_y, color="black")
        range_rl_y = np.array([self.rl.evalf(subs={t: i}) for i in range_x])
        axes.plot(range_x, range_rl_y, color="green")
        range_sl_y = np.array([self.sl.evalf(subs={t: i}) for i in range_x])
        axes.plot(range_x, range_sl_y, color="blue")
        mpl.draw()

        # 初始化关键点
        start_point = self.d_point
        x = list(solveset(self.pel - start_point.get_y(), t, Interval(0, 1)))[0]
        y = start_point.get_y()
        middle_point = Point(x, y)
        end_point = Point(x, self.rl.evalf(subs={t: x}))
        self.one_step(start_point, middle_point, end_point)
        while x > self.w_point.get_x():
            start_point = end_point
            x = list(solveset(self.pel - start_point.get_y(), t, Interval(0, 1)))[0]
            y = start_point.get_y()
            middle_point = Point(x, y)
            if x > self.q_point.get_x():
                end_point = Point(x, self.rl.evalf(subs={t: x}))
            else:
                end_point = Point(x, self.sl.evalf(subs={t: x}))
            self.one_step(start_point, middle_point, end_point)

    def one_step(self, start_point, middle_point, end_point):
        # 画布 mpl
        mpl = self.matplotlibwidget.mpl
        # 画图区域 axes
        axes = mpl.axes
        # 横线
        axes.plot([start_point.get_x(), middle_point.get_x()],
                  [start_point.get_y(), middle_point.get_y()],
                  "r")
        # 竖线
        axes.plot([middle_point.get_x(), end_point.get_x()],
                  [middle_point.get_y(), end_point.get_y()],
                  "r")
        mpl.draw()

    def get_common_point(self, exp1, exp2):
        """
        :param : func1,func2两个函数表达式
        :return: Point对象
        """
        x = list(solveset(exp1 - exp2, t, Interval(0, 1)))[0]
        y = exp1.evalf(subs={t: x})
        return Point(x, y)


if __name__ == '__main__':
    import sys

    # 对于按钮文字显示不全的解决方法，必须放在main中的第一行
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
