# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DownLoadBaiduImg.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DownLoadBaiduImgWindow(object):
    def setupUi(self, DownLoadBaiduImgWindow):
        DownLoadBaiduImgWindow.setObjectName("DownLoadBaiduImgWindow")
        DownLoadBaiduImgWindow.resize(600, 300)
        self.centralwidget = QtWidgets.QWidget(DownLoadBaiduImgWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label_1 = QtWidgets.QLabel(self.groupBox)
        self.label_1.setObjectName("label_1")
        self.gridLayout.addWidget(self.label_1, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.lineEdit_3, 2, 1, 1, 1)
        self.toolButton = QtWidgets.QToolButton(self.groupBox)
        self.toolButton.setObjectName("toolButton")
        self.gridLayout.addWidget(self.toolButton, 2, 2, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 2)
        self.lineEdit_1 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_1.setText("")
        self.lineEdit_1.setObjectName("lineEdit_1")
        self.gridLayout.addWidget(self.lineEdit_1, 0, 1, 1, 2)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout.addWidget(self.lineEdit_4, 3, 1, 1, 2)
        self.verticalLayout.addWidget(self.groupBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        DownLoadBaiduImgWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(DownLoadBaiduImgWindow)
        self.buttonBox.rejected.connect(DownLoadBaiduImgWindow.close)
        QtCore.QMetaObject.connectSlotsByName(DownLoadBaiduImgWindow)

    def retranslateUi(self, DownLoadBaiduImgWindow):
        _translate = QtCore.QCoreApplication.translate
        DownLoadBaiduImgWindow.setWindowTitle(_translate("DownLoadBaiduImgWindow", "下载百度图片集"))
        self.groupBox.setTitle(_translate("DownLoadBaiduImgWindow", "选项"))
        self.label_1.setText(_translate("DownLoadBaiduImgWindow", "关键字:"))
        self.label_3.setText(_translate("DownLoadBaiduImgWindow", "存放地址:"))
        self.label_4.setText(_translate("DownLoadBaiduImgWindow", "标 签:"))
        self.label_2.setText(_translate("DownLoadBaiduImgWindow", "数据数量:"))
        self.toolButton.setText(_translate("DownLoadBaiduImgWindow", "..."))

