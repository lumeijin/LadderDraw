# -*- coding: utf-8 -*-
# File  : app.py
# Author: Meijin Lu
# Date  : 2021/4/6
from pathlib import Path

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtGui import QIcon
from sympy import Interval, solveset
from .ui import Ui_MainWindow
from .canvas import *
import numpy as np


# 项目根目录（package 上一层）
_RESOURCE_DIR = Path(__file__).resolve().parent.parent / "resources"


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # 设置窗口图标
        icon_path = _RESOURCE_DIR / "icons" / "huagong.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        self.txt0.setFocus()
        # 后续一定要更新下面的值
        self.d_point = Point(0.99, 0.99)
        self.w_point = Point(0.01, 0.01)
        self.q_point = Point(0.5, 0.5)
        # 初始化对角线(diagonal line), 相平衡线, 精馏线, 提馏线, q线的方程
        self.dl = StraightLine(1, 0).func()
        self.pel = None
        self.rl = None
        self.sl = None
        self.ql = None

        # 对齐左侧参数标签（α, a, b, w），使输入框上下对齐
        for lbl in [self.label_8, self.label_3, self.label_4,
                     self.label_6, self.label_7, self.label_10]:
            lbl.setMinimumWidth(28)

        # 添加简单的样式美化
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #ccc;
                border-radius: 4px;
                margin-top: 8px;
                padding-top: 14px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 4px;
            }
            QPushButton {
                padding: 6px;
                font-size: 13px;
                border: 1px solid #aaa;
                border-radius: 3px;
                background: #f0f0f0;
            }
            QPushButton:hover {
                background: #e0e0e0;
            }
            QPushButton:pressed {
                background: #d0d0d0;
            }
            QLineEdit {
                padding: 3px;
                border: 1px solid #bbb;
                border-radius: 2px;
            }
        """)

    # ---------- 槽函数 ----------

    @pyqtSlot()
    def on_pushButton_start_clicked(self):
        """
        整个操作中最重要的函数
        :return:
        """
        # 获取输入框中的信息, 收到的值不为空则表明没有出错
        txt = self.get_txt()
        if txt is not None:
            # 相平衡线对象, 一个指针, 这里确定它的alpha值
            pel = PhaseQuilibriumLine(txt[0])
            self.pel = pel.func()
            # 精馏线对象, 指针, 确定a和b
            rl = StraightLine(txt[1], txt[2])
            self.rl = rl.func()
            # q线对象, 指针, 确定a和b
            ql = StraightLine(txt[3], txt[4])
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
        判断数据, 获取数据
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
            # 判断不为空, 且字符串为数字
            if self.is_number(item):
                txt.append(eval(item))
            else:
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

    # ---------- 绘制方法 ----------

    def ladder_draw(self):
        """
        只要没有到达w_point,
        从d_point开始, 在pel和rl之间画阶梯,
        画到q_point时, 改为在pel和sl之间画阶梯。
        :return:
        """
        self.matplotlibwidget.mpl.axes.cla()
        # 画布 mpl
        mpl = self.matplotlibwidget.mpl
        # 画图区域 axes
        axes = mpl.axes

        # 固定图表参数
        xfont = 10
        yfont = 10
        main_lw = 1.2
        step_lw = 1.8
        step_color = "r"

        axes.set_title("塔板阶梯图", fontsize=12, fontweight="bold")
        axes.set_ylabel("Y", fontsize=yfont)
        axes.set_xlabel("X", fontsize=xfont)
        axes.tick_params(axis='both', labelsize=9)
        axes.set_xlim(0, 1)
        axes.set_ylim(0, 1)
        axes.grid(True, linestyle=":", alpha=0.4)

        # 生成 x 轴数据
        range_x = np.linspace(0, 1, 100)

        # 画出对角线 (Diagonal)
        axes.plot([0, 1], [0, 1], color="black", linewidth=main_lw,
                  label="Diagonal")

        # 画出相平衡线 (Equilibrium Line)
        range_pel_y = np.array([self.pel.evalf(subs={t: i}) for i in range_x])
        axes.plot(range_x, range_pel_y, color="black", linewidth=main_lw,
                  linestyle="--", label="Equilibrium Line")

        # 画出精馏线 (Rectifying Line)
        range_rl_y = np.array([self.rl.evalf(subs={t: i}) for i in range_x])
        axes.plot(range_x, range_rl_y, color="green", linewidth=main_lw,
                  label="Rectifying Line")

        # 画出提馏线 (Stripping Line)
        range_sl_y = np.array([self.sl.evalf(subs={t: i}) for i in range_x])
        axes.plot(range_x, range_sl_y, color="blue", linewidth=main_lw,
                  label="Stripping Line")

        # 画出 q 线 (q-Line)
        if self.ql is not None:
            range_ql_y = np.array([self.ql.evalf(subs={t: i}) for i in range_x])
            axes.plot(range_x, range_ql_y, color="orange", linewidth=main_lw,
                      linestyle="-.", label="q-Line")

        # 添加图例（放置在右侧垂直居中位置）
        axes.legend(fontsize=8, loc="center right")
        mpl.draw()

        # 画出阶梯（画法保持原样），并用小数方式计算理论塔板数
        full_stages = 0

        start_point = self.d_point
        x_eq = list(solveset(self.pel - start_point.get_y(), t, Interval(0, 1)))[0]
        y = start_point.get_y()
        middle_point = Point(x_eq, y)
        end_point = Point(x_eq, self.rl.evalf(subs={t: x_eq}))
        self.one_step(start_point, middle_point, end_point, step_color, step_lw)
        full_stages += 1

        while True:
            start_point = end_point
            x_prev = float(start_point.get_x())   # 记下本步起点
            x_eq = list(solveset(self.pel - start_point.get_y(), t, Interval(0, 1)))[0]
            y = start_point.get_y()

            # 仍然画完整的阶梯（视觉不变）
            middle_point = Point(x_eq, y)
            if x_eq > self.q_point.get_x():
                end_point = Point(x_eq, self.rl.evalf(subs={t: x_eq}))
            else:
                end_point = Point(x_eq, self.sl.evalf(subs={t: x_eq}))
            self.one_step(start_point, middle_point, end_point, step_color, step_lw)

            # 判断是否越过了塔釜浓度 w
            if x_eq < self.w_point.get_x():
                xw = float(self.w_point.get_x())
                fraction = (x_prev - xw) / (x_prev - float(x_eq)) if abs(x_prev - float(x_eq)) > 1e-10 else 0.0
                total_stages = full_stages + fraction
                break

            full_stages += 1

        # 在图表底部中央显示理论塔板数（保留 1 位小数）
        axes.text(0.5, 0.04, f"理论塔板数 = {total_stages:.1f}",
                  transform=axes.transAxes, fontsize=11, fontweight="bold",
                  ha="center", va="bottom",
                  bbox=dict(facecolor="lightyellow", edgecolor="#cc8800",
                            boxstyle="round,pad=0.4", alpha=0.92))
        mpl.draw()

    def one_step(self, start_point, middle_point, end_point, color="r", lw=1.8):
        # 画布 mpl
        mpl = self.matplotlibwidget.mpl
        # 画图区域 axes
        axes = mpl.axes
        # 横线
        axes.plot([start_point.get_x(), middle_point.get_x()],
                  [start_point.get_y(), middle_point.get_y()],
                  color=color, linewidth=lw)
        # 竖线
        axes.plot([middle_point.get_x(), end_point.get_x()],
                  [middle_point.get_y(), end_point.get_y()],
                  color=color, linewidth=lw)
        mpl.draw()

    def get_common_point(self, exp1, exp2):
        """
        :param : func1,func2两个函数表达式
        :return: Point对象
        """
        x = list(solveset(exp1 - exp2, t, Interval(0, 1)))[0]
        y = exp1.evalf(subs={t: x})
        return Point(x, y)