# -*- coding: utf-8 -*-
# File  : __main__.py
# Author: Meijin Lu
# Date  : 2021/4/6
"""
Package entry point.
Run with: python -m ladderdraw
"""
import sys
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import QApplication

# 用绝对导入：`python -m ladderdraw` 与 PyInstaller 冻结（入口被当作顶层
# __main__ 运行、无包上下文）两种场景下都能正常解析。
from ladderdraw.app import MainWindow


def main():
    # 对于按钮文字显示不全的解决方法，必须放在main中的第一行
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()