# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TFRecordBar.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TFRecordProcess(object):
    def setupUi(self, TFRecordProcess):
        TFRecordProcess.setObjectName("TFRecordProcess")
        TFRecordProcess.resize(500, 100)
        self.centralwidget = QtWidgets.QWidget(TFRecordProcess)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout.addWidget(self.progressBar)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        TFRecordProcess.setCentralWidget(self.centralwidget)

        self.retranslateUi(TFRecordProcess)
        QtCore.QMetaObject.connectSlotsByName(TFRecordProcess)

    def retranslateUi(self, TFRecordProcess):
        _translate = QtCore.QCoreApplication.translate
        TFRecordProcess.setWindowTitle(_translate("TFRecordProcess", "制作数据集进度"))
        self.label.setText(_translate("TFRecordProcess", "开始制作数据集"))
        self.pushButton.setText(_translate("TFRecordProcess", "取消"))

