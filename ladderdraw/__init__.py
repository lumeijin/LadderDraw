# ladderdraw - McCabe-Thiele 精馏阶梯图绘制工具
"""LadderDraw: McCabe-Thiele 精馏理论塔板阶梯图绘制工具。

GUI 入口: ``python -m ladderdraw``
纯计算 API（无需 Qt）: ``from ladderdraw import compute_stages``
"""
from .core import (
    NoSolutionError,
    PhaseQuilibriumLine,
    Point,
    StageResult,
    StraightLine,
    compute_stages,
    solve_in_unit,
    t,
)

__all__ = [
    "Point",
    "PhaseQuilibriumLine",
    "StraightLine",
    "compute_stages",
    "StageResult",
    "NoSolutionError",
    "solve_in_unit",
    "t",
]
