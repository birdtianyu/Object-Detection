import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QMessageBox
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtCore import QRegExp

from TFRecordWindow import Ui_TFRecord_Window
import TFRecordControl

class MyTFRecordWindow(QMainWindow, Ui_TFRecord_Window):
    def __init__(self, parent=None):
        super(MyTFRecordWindow, self).__init__(parent)
        self.setupUi(self)
        # 关联文件夹快捷方式
        self.toolButton_1.clicked.connect(self.directoryOpen1)
        self.toolButton_2.clicked.connect(self.directoryOpen2)

        # 设置预留文字
        self.lineEdit_1.setPlaceholderText("每个分类文件夹的总地址路径")
        self.lineEdit_2.setPlaceholderText("路径")
        self.lineEdit_3.setPlaceholderText("即每类图片的文件夹名称, 请以;分隔")
        self.lineEdit_4.setPlaceholderText("限制图像数量为1到120的整数")
        self.lineEdit_5.setPlaceholderText("由英文和数字组成")
        self.lineEdit_6.setPlaceholderText("限制图像裁剪尺寸输入为1到600的整数")

        # 预设内部变量
        self.comeFrom = r"D:/Python/Train_Data/TensorFlow_Data/Sample"
        self.comeTo = r"D:/Python/Train_Data/TensorFlow_Data/Inputdata"
        self.imgClassName = {'Gun', 'Knife', 'Lighter'}        # 文件夹名称集合
        self.perNum = 100
        self.TFRecordName = "Detection"
        self.size = 64
        # self.form

        # 限制图像裁剪尺寸输入为1到120的整数
        pIntValidator = QIntValidator(self)
        pIntValidator.setRange(1, 120)  # 设置输入整数的范围
        self.lineEdit_4.setValidator(pIntValidator)

        # 限制TFRecord数据集名称文本输入为英文字母和数字
        reg = QRegExp("[a-zA-Z0-9]+$")
        pValidator = QRegExpValidator(self)
        pValidator.setRegExp(reg)
        self.lineEdit_5.setValidator(pValidator)

        # 限制图像裁剪尺寸输入为1到600的整数
        pIntValidator = QIntValidator(self)
        pIntValidator.setRange(1, 600)     # 设置输入整数的范围
        self.lineEdit_6.setValidator(pIntValidator)

        # 当输入改变更新变量值
        self.lineEdit_1.textChanged.connect(self.SetComeFrom)
        self.lineEdit_2.textChanged.connect(self.SetComeTo)
        self.lineEdit_3.textChanged.connect(self.SetImgClassName)
        self.lineEdit_4.textChanged.connect(self.SetPerNum)
        self.lineEdit_5.textChanged.connect(self.SetTFRecordName)
        self.lineEdit_6.textChanged.connect(self.SetSize)

        # 当点击OK时会发射信号，开始执行
        self.buttonBox.accepted.connect(self.GetStart)

    def directoryOpen1(self):
        """快捷方式填写文件夹路径"""
        self.file1 = QFileDialog.getExistingDirectory(self, "打开", r"D:/")
        self.lineEdit_1.setText(self.file1)

    def directoryOpen2(self):
        """快捷方式填写文件夹路径"""
        self.file2 = QFileDialog.getExistingDirectory(self, "打开", r"D:/")
        self.lineEdit_2.setText(self.file2)

    def SetComeFrom(self, text):
        if text == "":
            self.comeFrom = r"D:/Python/Train_Data/TensorFlow_Data/Sample"
        else:
            self.comeFrom = text

    def SetComeTo(self, text):
        if text == "":
            self.comeTo = r"D:/Python/Train_Data/TensorFlow_Data/Inputdata"
        else:
            self.comeTo = text

    def SetImgClassName(self, text):
        if text == "":
            self.imgClassName = {'Gun', 'Knife', 'Lighter'}
        else:
            temp = text
            temp = temp.split(';')
            self.imgClassName = set(temp)

    def SetPerNum(self, text):
        if text == "":
            self.perNum = 100
        else:
            self.perNum = int(text)

    def SetTFRecordName(self, text):
        if text == "":
            self.TFRecordName = "Detection"
        else:
            self.TFRecordName = text

    def SetSize(self, text):
        if text == "":
            self.size = 64
        else:
            self.size = int(text)

    def GetStart(self):
        """主要执行函数"""
        # 首先开始异常处理
        print("comeFrom, ", self.comeFrom)
        print("comeTo, ", self.comeTo)
        print("imgClassName, ", self.imgClassName)
        print("perNum, ", self.perNum)
        print("TFRecordName,", self.TFRecordName)
        print("size,", self.size)
        if self.TFRecordName == "Detection":
            # 使用information信息框
            reply = QMessageBox.information(self, "警告", "请填写相关信息", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            print(reply)  # 必须打印出来才会显示出来窗口
        else:
            TFRecordControl.handle(self.comeFrom, self.imgClassName, self.size, self.perNum, self.TFRecordName, self.comeTo)
            self.close()

def main():
    app = QApplication(sys.argv)
    myWin = MyTFRecordWindow()
    myWin.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()





