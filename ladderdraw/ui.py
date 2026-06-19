# -*- coding: utf-8 -*-
# File  : ui.py
# Author: Meijin Lu
#
# 主窗口界面定义。已从 .ui 手工迁移并继续手工维护，
# 不再由 pyuic 自动生成 —— 可直接编辑本文件。


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 650)
        MainWindow.setMinimumSize(QtCore.QSize(700, 500))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_main = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_main.setObjectName("horizontalLayout_main")

        # ========== 左侧面板 ==========
        self.leftPanel = QtWidgets.QWidget(self.centralwidget)
        self.leftPanel.setMinimumSize(QtCore.QSize(240, 0))
        self.leftPanel.setMaximumSize(QtCore.QSize(280, 16777215))
        self.leftPanel.setObjectName("leftPanel")
        self.verticalLayout_left = QtWidgets.QVBoxLayout(self.leftPanel)
        self.verticalLayout_left.setObjectName("verticalLayout_left")

        # ---- 计算参数分组 ----
        self.groupBox_params = QtWidgets.QGroupBox(self.leftPanel)
        self.groupBox_params.setObjectName("groupBox_params")
        self.verticalLayout_params = QtWidgets.QVBoxLayout(self.groupBox_params)
        self.verticalLayout_params.setObjectName("verticalLayout_params")

        self.label = QtWidgets.QLabel(self.groupBox_params)
        self.label.setObjectName("label")
        self.verticalLayout_params.addWidget(self.label)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_8 = QtWidgets.QLabel(self.groupBox_params)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout.addWidget(self.label_8)
        self.txt0 = QtWidgets.QLineEdit(self.groupBox_params)
        self.txt0.setObjectName("txt0")
        self.horizontalLayout.addWidget(self.txt0)
        self.verticalLayout_params.addLayout(self.horizontalLayout)

        self.label_2 = QtWidgets.QLabel(self.groupBox_params)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_params.addWidget(self.label_2)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox_params)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.txt1 = QtWidgets.QLineEdit(self.groupBox_params)
        self.txt1.setObjectName("txt1")
        self.horizontalLayout_2.addWidget(self.txt1)
        self.verticalLayout_params.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox_params)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.txt2 = QtWidgets.QLineEdit(self.groupBox_params)
        self.txt2.setObjectName("txt2")
        self.horizontalLayout_3.addWidget(self.txt2)
        self.verticalLayout_params.addLayout(self.horizontalLayout_3)

        self.label_5 = QtWidgets.QLabel(self.groupBox_params)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_params.addWidget(self.label_5)

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_6 = QtWidgets.QLabel(self.groupBox_params)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6)
        self.txt3 = QtWidgets.QLineEdit(self.groupBox_params)
        self.txt3.setObjectName("txt3")
        self.horizontalLayout_4.addWidget(self.txt3)
        self.verticalLayout_params.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_7 = QtWidgets.QLabel(self.groupBox_params)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_5.addWidget(self.label_7)
        self.txt4 = QtWidgets.QLineEdit(self.groupBox_params)
        self.txt4.setObjectName("txt4")
        self.horizontalLayout_5.addWidget(self.txt4)
        self.verticalLayout_params.addLayout(self.horizontalLayout_5)

        self.label_9 = QtWidgets.QLabel(self.groupBox_params)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_params.addWidget(self.label_9)

        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_10 = QtWidgets.QLabel(self.groupBox_params)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_6.addWidget(self.label_10)
        self.txt5 = QtWidgets.QLineEdit(self.groupBox_params)
        self.txt5.setObjectName("txt5")
        self.horizontalLayout_6.addWidget(self.txt5)
        self.verticalLayout_params.addLayout(self.horizontalLayout_6)

        self.verticalLayout_left.addWidget(self.groupBox_params)

        # ---- 按钮 ----
        self.pushButton_start = QtWidgets.QPushButton(self.leftPanel)
        self.pushButton_start.setObjectName("pushButton_start")
        self.verticalLayout_left.addWidget(self.pushButton_start)

        self.pushButton_clear = QtWidgets.QPushButton(self.leftPanel)
        self.pushButton_clear.setObjectName("pushButton_clear")
        self.verticalLayout_left.addWidget(self.pushButton_clear)

        # ---- 弹簧 ----
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_left.addItem(spacerItem)

        self.horizontalLayout_main.addWidget(self.leftPanel)

        # ========== 右侧 Matplotlib 控件 ==========
        self.matplotlibwidget = MatplotlibWidget(self.centralwidget)
        self.matplotlibwidget.setObjectName("matplotlibwidget")
        self.horizontalLayout_main.addWidget(self.matplotlibwidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "LadderDraw"))
        # 计算参数
        self.groupBox_params.setTitle(_translate("MainWindow", "计算参数"))
        self.label.setText(_translate("MainWindow", "相平衡线 y = αx / (1+(α-1)x)"))
        self.label_8.setText(_translate("MainWindow", "α"))
        self.txt0.setText(_translate("MainWindow", "2.16"))
        self.label_2.setText(_translate("MainWindow", "精馏线 y = ax + b"))
        self.label_3.setText(_translate("MainWindow", "a"))
        self.txt1.setText(_translate("MainWindow", "0.745"))
        self.label_4.setText(_translate("MainWindow", "b"))
        self.txt2.setText(_translate("MainWindow", "0.24"))
        self.label_5.setText(_translate("MainWindow", "q线 y = ax + b"))
        self.label_6.setText(_translate("MainWindow", "a"))
        self.txt3.setText(_translate("MainWindow", "-1"))
        self.label_7.setText(_translate("MainWindow", "b"))
        self.txt4.setText(_translate("MainWindow", "0.865"))
        self.label_9.setText(_translate("MainWindow", "塔釜浓度"))
        self.label_10.setText(_translate("MainWindow", "w"))
        self.txt5.setText(_translate("MainWindow", "0.046"))
        # 按钮
        self.pushButton_start.setText(_translate("MainWindow", "绘制"))
        self.pushButton_clear.setText(_translate("MainWindow", "清空"))


from .canvas import MatplotlibWidget