# LadderDraw

一个化工小工具，用于绘制化工原理中常见的精馏塔塔板阶梯图（McCabe-Thiele 图）。

## 截图

![软件截图](pic/软件截图.png)

## Get Started

### 安装依赖

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 运行

```bash
python -m ladderdraw
```

### 操作说明

1. 在左侧面板输入 **相平衡线 α**、**精馏线 a/b**、**q 线 a/b** 和 **塔釜浓度 w**
2. 点击 **绘制** 按钮生成阶梯图
3. 图表区支持 matplotlib 工具栏交互（平移、缩放、保存）

## 理论塔板数计算原理

McCabe-Thiele 法中，理论塔板数通过逐级图解法计算：

1. 从塔顶馏出液组成点 (xD, xD) 出发，在平衡线和操作线（精馏线/提馏线）之间交替画水平线和竖直线，形成阶梯
2. 每完成一个 **水平→竖直** 的完整阶梯，计为 **1 块理论塔板**
3. 当最后一段水平线的 x 坐标即将越过塔釜浓度 w 时，按比例计算小数部分：

```
小数部分 = (x_起点 - w) / (x_起点 - x_平衡线交点)
```

其中：
- x_起点 — 最后一个完整阶梯起步时的 x 坐标
- x_平衡线交点 — 该步水平线本应到达的相平衡线 x 坐标
- w — 塔釜浓度

**理论塔板数 = 完整阶梯数 + 小数部分**

例如默认参数下：14 个完整阶梯 + 0.3 部分阶梯 = **14.3 块理论塔板**。

## 项目思路

PyQt5 与 matplotlib 结合，构建桌面应用：

**对象模型：**

![对象模型](pic/对象模型.png)

### 依赖

- PyQt5
- matplotlib
- sympy
- numpy

### 开发工具

- Python 3
- Qt Designer（UI 设计）

## License

MIT
