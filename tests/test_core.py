# -*- coding: utf-8 -*-
# File  : test_core.py
"""ladderdraw.core 的回归测试（仅依赖 sympy，不需要 PyQt/matplotlib）。

运行方式:
    python -m unittest discover -s tests        # 内置 unittest
    # 或
    python -m pytest tests                       # 若装了 pytest
"""
import unittest

from ladderdraw.core import NoSolutionError, compute_stages


# 与 GUI 预填默认值一致；README 的基准理论塔板数 14.3 即由此组参数得到
DEFAULTS = dict(alpha=2.16, rl_a=0.745, rl_b=0.24,
                ql_a=-1, ql_b=0.865, w=0.046)


class TestComputeStages(unittest.TestCase):
    # ---------- 正常计算 ----------

    def test_default_total_stages(self):
        """默认参数 → 理论塔板数 ≈ 14.286（README 基准 14.3）。"""
        r = compute_stages(**DEFAULTS)
        self.assertAlmostEqual(r.total_stages, 14.286, places=2)

    def test_default_stage_counts(self):
        r = compute_stages(**DEFAULTS)
        self.assertEqual(r.full_stages, 14)
        self.assertEqual(len(r.steps), 15)   # 1 个起步阶梯 + 14 个循环阶梯

    def test_key_points(self):
        r = compute_stages(**DEFAULTS)
        self.assertAlmostEqual(float(r.d_point[0]), 0.941, places=2)  # xD
        self.assertAlmostEqual(float(r.q_point[0]), 0.358, places=2)  # qx

    def test_steps_geometry(self):
        """每级阶梯：起点-中点等 y（横线），中点-终点等 x（竖线）。"""
        r = compute_stages(**DEFAULTS)
        for start, mid, end in r.steps:
            self.assertEqual(float(start[1]), float(mid[1]))
            self.assertEqual(float(mid[0]), float(end[0]))

    # ---------- 参数校验 / 友好报错 ----------

    def test_alpha_le_one_rejected(self):
        """α ≤ 1 物理上不可分离，应立即报错而非死循环。"""
        with self.assertRaises(NoSolutionError):
            compute_stages(alpha=0.5, rl_a=0.745, rl_b=0.24,
                           ql_a=-1, ql_b=0.865, w=0.046)

    def test_w_out_of_range_rejected(self):
        with self.assertRaises(NoSolutionError):
            compute_stages(alpha=2.16, rl_a=0.745, rl_b=0.24,
                           ql_a=-1, ql_b=0.865, w=1.5)

    def test_parallel_rectifying_line_rejected(self):
        """精馏线与对角线平行（无交点）应被捕获。"""
        with self.assertRaises(NoSolutionError):
            compute_stages(alpha=2.16, rl_a=1, rl_b=0.5,
                           ql_a=-1, ql_b=0.865, w=0.046)

    def test_friendly_message_content(self):
        """校验失败的消息应是中文人话，而非 sympy 内部方程。"""
        try:
            compute_stages(alpha=0.5, rl_a=0.745, rl_b=0.24,
                           ql_a=-1, ql_b=0.865, w=0.046)
        except NoSolutionError as exc:
            self.assertIn("相对挥发度", str(exc))
        else:
            self.fail("应抛出 NoSolutionError")


if __name__ == '__main__':
    unittest.main()
