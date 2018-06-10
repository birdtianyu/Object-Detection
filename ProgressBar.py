# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ProgressBar.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ProgressBarWin(object):
    def setupUi(self, ProgressBarWin):
        ProgressBarWin.setObjectName("ProgressBarWin")
        ProgressBarWin.resize(540, 100)
        self.centralwidget = QtWidgets.QWidget(ProgressBarWin)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout.addWidget(self.progressBar)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 4)
        ProgressBarWin.setCentralWidget(self.centralwidget)

        self.retranslateUi(ProgressBarWin)
        QtCore.QMetaObject.connectSlotsByName(ProgressBarWin)

    def retranslateUi(self, ProgressBarWin):
        _translate = QtCore.QCoreApplication.translate
        ProgressBarWin.setWindowTitle(_translate("ProgressBarWin", "下载进度"))
        self.label.setText(_translate("ProgressBarWin", "TextLabel"))
        self.pushButton.setText(_translate("ProgressBarWin", "取消"))

