# -*- coding: utf-8 -*-
# File  : app.py
# Author: Meijin Lu
# Date  : 2021/4/6
"""主窗口控制器：读取参数 -> 调用 core.compute_stages -> 绘制结果。"""
import sys
from pathlib import Path

import numpy as np
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from .core import NoSolutionError, compute_stages, t
from .ui import Ui_MainWindow


def _resource_dir():
    """定位 resources/ 目录；兼容源码运行与 PyInstaller 冻结环境。"""
    if getattr(sys, 'frozen', False):
        # PyInstaller onefile：资源被解包到临时目录 _MEIPASS/resources
        base = Path(sys._MEIPASS)
    else:
        base = Path(__file__).resolve().parent.parent
    return base / "resources"


_RESOURCE_DIR = _resource_dir()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # 设置窗口图标
        icon_path = _RESOURCE_DIR / "icons" / "huagong.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        self.txt0.setFocus()
        self._result = None  # 最近一次 compute_stages 的结果（StageResult）

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
        """读取参数 -> 计算 -> 绘制。"""
        txt = self.get_txt()
        if txt is None:
            return
        alpha, rl_a, rl_b, ql_a, ql_b, w = txt
        try:
            self._result = compute_stages(alpha, rl_a, rl_b, ql_a, ql_b, w)
        except NoSolutionError as exc:
            QMessageBox.warning(self, '警告', f'参数不合理，无法求解：\n{exc}')
            return
        self.ladder_draw()

    @pyqtSlot()
    def on_pushButton_clear_clicked(self):
        """清空图表与输入框。"""
        self.matplotlibwidget.mpl.axes.cla()
        self.matplotlibwidget.mpl.draw()
        for edit in (self.txt0, self.txt1, self.txt2,
                     self.txt3, self.txt4, self.txt5):
            edit.clear()
        self.txt0.setFocus()

    def get_txt(self):
        """读取并校验 6 个输入框，返回 float 元组；非法则弹警告并返回 None。"""
        value_list = (self.txt0.text(), self.txt1.text(), self.txt2.text(),
                      self.txt3.text(), self.txt4.text(), self.txt5.text())
        parsed = []
        for item in value_list:
            if self.is_number(item):
                parsed.append(float(item))
            else:
                QMessageBox.warning(self, '警告', '请检查输入')
                return None
        return tuple(parsed)

    @staticmethod
    def is_number(s):
        """为空返回 False；否则判断是否为数字（含 Unicode 数字字符）。"""
        if s is None:
            return False
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
            return False

    # ---------- 绘制 ----------

    def ladder_draw(self):
        """依据 self._result 绘制阶梯图。"""
        r = self._result
        mpl = self.matplotlibwidget.mpl
        axes = mpl.axes
        axes.cla()

        # 固定图表参数
        main_lw = 1.2
        step_lw = 1.8
        step_color = "r"

        axes.set_title("塔板阶梯图", fontsize=12, fontweight="bold")
        axes.set_xlabel("X", fontsize=10)
        axes.set_ylabel("Y", fontsize=10)
        axes.tick_params(axis='both', labelsize=9)
        axes.set_xlim(0, 1)
        axes.set_ylim(0, 1)
        axes.grid(True, linestyle=":", alpha=0.4)

        range_x = np.linspace(0, 1, 100)

        # 对角线 (Diagonal)
        axes.plot([0, 1], [0, 1], color="black", linewidth=main_lw,
                  label="Diagonal")

        # 相平衡线 / 精馏线 / 提馏线 / q 线
        curves = [
            (r.pel, "black", "--", "Equilibrium Line"),
            (r.rl, "green", "-", "Rectifying Line"),
            (r.sl, "blue", "-", "Stripping Line"),
            (r.ql, "orange", "-.", "q-Line"),
        ]
        for expr, color, style, label in curves:
            ys = np.array([float(expr.evalf(subs={t: i})) for i in range_x])
            axes.plot(range_x, ys, color=color, linewidth=main_lw,
                      linestyle=style, label=label)

        axes.legend(fontsize=8, loc="center right")

        # 阶梯（横向到相平衡线，纵向到操作线）
        for start, mid, end in r.steps:
            axes.plot([float(start[0]), float(mid[0])],
                      [float(start[1]), float(mid[1])],
                      color=step_color, linewidth=step_lw)
            axes.plot([float(mid[0]), float(end[0])],
                      [float(mid[1]), float(end[1])],
                      color=step_color, linewidth=step_lw)

        # 理论塔板数（保留 1 位小数）
        axes.text(0.5, 0.04, f"理论塔板数 = {r.total_stages:.1f}",
                  transform=axes.transAxes, fontsize=11, fontweight="bold",
                  ha="center", va="bottom",
                  bbox=dict(facecolor="lightyellow", edgecolor="#cc8800",
                            boxstyle="round,pad=0.4", alpha=0.92))

        mpl.draw()
