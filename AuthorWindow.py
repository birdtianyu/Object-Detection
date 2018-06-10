# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AuthorWindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AuthorWindow(object):
    def setupUi(self, AuthorWindow):
        AuthorWindow.setObjectName("AuthorWindow")
        AuthorWindow.resize(407, 200)
        AuthorWindow.setMaximumSize(QtCore.QSize(1057, 826))
        self.centralwidget = QtWidgets.QWidget(AuthorWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setIndent(5)
        self.label.setOpenExternalLinks(False)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("../../../myicon.png"))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        AuthorWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(AuthorWindow)
        QtCore.QMetaObject.connectSlotsByName(AuthorWindow)

    def retranslateUi(self, AuthorWindow):
        _translate = QtCore.QCoreApplication.translate
        AuthorWindow.setWindowTitle(_translate("AuthorWindow", "开发者信息"))
        self.label.setText(_translate("AuthorWindow", "Detection Software\n"
"Version 1.07\n"
"Last modified 2018.5.17\n"
"CopyRight(C) 2018\n"
"Hongkun Xu\n"
"GitHub:https://github.com/birdtianyu\n"
"Email:birdtianyu@gmail.com "))

