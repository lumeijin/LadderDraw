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

from .app import MainWindow


def main():
    # 对于按钮文字显示不全的解决方法，必须放在main中的第一行
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()