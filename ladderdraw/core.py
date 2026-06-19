# -*- coding: utf-8 -*-
# File  : core.py
# Author: Meijin Lu
# Date  : 2021/4/6
"""McCabe-Thiele 理论塔板计算 —— 纯数学层。

本模块只依赖 sympy，不依赖 PyQt / matplotlib，因此可以脱离 GUI
单独导入、单元测试，或用于命令行批量计算。

公共 API:
    compute_stages(alpha, rl_a, rl_b, ql_a, ql_b, w) -> StageResult
"""
from dataclasses import dataclass
from typing import List, Optional, Tuple

import sympy

# 贯穿全模块的横坐标符号
t = sympy.Symbol("t")

# 浮点 (x, y) 点
XY = Tuple[float, float]


class Point:
    """二维点 / 交点。

    保留 ``get_x`` / ``get_y`` / ``get_coordinate`` 旧接口以兼容现有调用。
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.coordinate = (x, y)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_coordinate(self):
        return self.coordinate


class PhaseQuilibriumLine:
    """相平衡线 y = αx / (1 + (α-1)x)。"""

    def __init__(self, alpha):
        self.alpha = alpha

    def func(self):
        a = self.alpha
        return a * t / (1 + (a - 1) * t)


class StraightLine:
    """直线 y = a*x + b（精馏线 / q 线 / 对角线 / 提馏线）。"""

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def func(self):
        return self.a * t + self.b


class NoSolutionError(ValueError):
    """给定方程在区间 [0, 1] 内无实数解。"""


def solve_in_unit(expr, symbol=t):
    """求 ``expr = 0`` 在 [0, 1] 内的解；无解抛 :class:`NoSolutionError`。

    封装了原本散落在各处的 ``list(solveset(...))[0]``，避免空解集导致
    的 IndexError。
    """
    solutions = list(sympy.solveset(expr, symbol, sympy.Interval(0, 1)))
    if not solutions:
        raise NoSolutionError(f"方程在 [0, 1] 内无解: {expr} = 0")
    return solutions[0]


@dataclass
class StageResult:
    """``compute_stages`` 的返回结果。"""

    total_stages: float                   # 理论塔板数（含小数部分）
    full_stages: int                      # 完整阶梯数
    steps: List[Tuple[XY, XY, XY]]        # 每级阶梯的 (起点, 中点, 终点)
    # 供 GUI 采样绘制的曲线表达式（sympy）
    pel: object                           # 相平衡线
    rl: object                            # 精馏线
    sl: object                            # 提馏线
    ql: object                            # q 线
    # 关键点
    d_point: XY                           # 馏出液组成点 (xD, xD)
    q_point: XY                           # 精馏线与 q 线交点
    w_point: XY                           # 塔釜浓度点 (w, w)


def _validate_inputs(alpha, rl_a, rl_b, ql_a, ql_b, w):
    """对参数做物理合理性预检，失败时抛 :class:`NoSolutionError`（带中文提示）。

    目的是把退化参数挡在重型符号计算之前，并给出人话提示，
    而不是暴露 sympy 内部的方程信息。
    """
    if alpha <= 1:
        raise NoSolutionError(
            f"相对挥发度 α = {alpha} 应大于 1（α ≤ 1 时无法用此法分离）。"
        )
    if not (0 < w < 1):
        raise NoSolutionError(f"塔釜浓度 w = {w} 应在 (0, 1) 之间。")


def compute_stages(alpha, rl_a, rl_b, ql_a, ql_b, w):
    """计算 McCabe-Thiele 理论塔板数（纯函数，无 Qt 依赖）。

    :param alpha: 相对挥发度 α
    :param rl_a, rl_b: 精馏线 y = a*x + b 的系数
    :param ql_a, ql_b: q 线 y = a*x + b 的系数
    :param w: 塔釜（残液）摩尔分数 xW
    :return: :class:`StageResult`
    :raises NoSolutionError: 当参数不合理（α ≤ 1、w 越界、操作线无交点等）时。
    """
    _validate_inputs(alpha, rl_a, rl_b, ql_a, ql_b, w)

    # ---- 曲线表达式 ----
    pel = alpha * t / (1 + (alpha - 1) * t)   # 相平衡线
    rl = rl_a * t + rl_b                      # 精馏线
    ql = ql_a * t + ql_b                      # q 线
    dl = t                                    # 对角线 y = x

    # ---- 关键交点 ----
    try:
        xd = solve_in_unit(dl - rl)           # 馏出液组成（对角线 ∩ 精馏线）
    except NoSolutionError:
        raise NoSolutionError(
            "精馏线与对角线在 [0, 1] 内无交点，请检查精馏线参数 a、b。"
        ) from None
    d_point = (xd, xd)
    try:
        qx = solve_in_unit(rl - ql)           # 精馏线 ∩ q 线
    except NoSolutionError:
        raise NoSolutionError(
            "精馏线与 q 线在 [0, 1] 内无交点，请检查 q 线参数 a、b。"
        ) from None
    qy = ql.evalf(subs={t: qx})
    q_point = (qx, qy)
    w_point = (w, w)

    # 提馏线：过 (w, w) 与 q_point
    sl = w + (t - w) * (qy - w) / (qx - w)

    # ---- 逐级图解（阶梯法）----
    # 第一级：从 d_point 出发，水平线先到相平衡线，竖线先落回精馏线
    steps: List[Tuple[XY, XY, XY]] = []
    start = d_point
    x_eq = solve_in_unit(pel - start[1])
    mid = (x_eq, start[1])
    end = (x_eq, rl.evalf(subs={t: x_eq}))
    steps.append((start, mid, end))
    full_stages = 1

    max_stages = 500  # 安全上限：退化参数下防止阶梯永不越过 w 而死循环
    total_stages: Optional[float] = None
    while True:
        start = end
        x_prev = float(start[0])
        x_eq = solve_in_unit(pel - start[1])
        mid = (x_eq, start[1])
        # 越过 q 线交点后切换到提馏线
        if x_eq > qx:
            end = (x_eq, rl.evalf(subs={t: x_eq}))
        else:
            end = (x_eq, sl.evalf(subs={t: x_eq}))
        steps.append((start, mid, end))

        # 越过塔釜浓度 w 时，按比例计算小数部分并结束
        if x_eq < w:
            span = x_prev - float(x_eq)
            fraction = (x_prev - w) / span if abs(span) > 1e-10 else 0.0
            total_stages = full_stages + fraction
            break
        full_stages += 1
        if full_stages > max_stages:
            # 阶梯未收敛（常见于 α ≤ 1 等退化参数），避免无限循环
            raise NoSolutionError(
                f"阶梯已超过 {max_stages} 级仍未越过塔釜浓度 w，请检查参数"
                f"（相对挥发度 α 通常应大于 1）。"
            )

    return StageResult(
        total_stages=total_stages,
        full_stages=full_stages,
        steps=steps,
        pel=pel, rl=rl, sl=sl, ql=ql,
        d_point=d_point, q_point=q_point, w_point=w_point,
    )
