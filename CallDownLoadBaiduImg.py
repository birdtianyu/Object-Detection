import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QMessageBox
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtCore import QRegExp

from DownLoadBaiduImg import Ui_DownLoadBaiduImgWindow
from DownLoadBaiduControl import DownLoadControl
from CallProgressBar import MyProgressBar

FILE = "D:/"   # 文件保存地址

class MyDownLoadWindow(QMainWindow, Ui_DownLoadBaiduImgWindow):
    def __init__(self, parent=None):
        super(MyDownLoadWindow, self).__init__(parent)
        self.setupUi(self)
        # 关联文件夹快捷方式
        self.toolButton.clicked.connect(self.directoryOpen)
        # 限制文本输入为1到600的整数
        pIntValidator = QIntValidator(self)
        pIntValidator.setRange(1, 600)   # 设置输入整数的范围
        self.lineEdit_2.setValidator(pIntValidator)
        # 限制文本输入为英文字母和数字
        reg = QRegExp("[a-zA-Z0-9]+$")
        pValidator = QRegExpValidator(self)
        pValidator.setRegExp(reg)
        self.lineEdit_4.setValidator(pValidator)

        # 设置预留文字
        self.lineEdit_1.setPlaceholderText("中文或英文")
        self.lineEdit_2.setPlaceholderText("1到600的整数")
        self.lineEdit_3.setPlaceholderText("文件夹路径")
        self.lineEdit_4.setPlaceholderText("图片英文前缀名称")

        # 预设内部变量
        self.Title = "默认值"
        self.Number = 1
        self.Directory = r"D:\Python"
        self.Label = "Index_"

        # 当输入改变更新变量值
        self.lineEdit_1.textChanged.connect(self.SetTitleText)
        self.lineEdit_2.textChanged.connect(self.SetNumberText)
        self.lineEdit_3.textChanged.connect(self.SetDirectoryText)
        self.lineEdit_4.textChanged.connect(self.SetLabelText)

        # 当点击OK时会发射信号，获取输入文本s
        self.buttonBox.accepted.connect(self.GetInfor)

    def directoryOpen(self):
        """快捷方式填写文件夹路径"""
        self.file = QFileDialog.getExistingDirectory(self, "打开", "D:/Python/Text")  # 打开文件夹位置
        self.lineEdit_3.setText(self.file)

    def SetTitleText(self, text):
        if text == "":
            self.Title = "默认值"
        else:
            self.Title = text

    def SetNumberText(self, text):
        if text == "":
            self.Number = 1
        else:
            self.Number = int(text)

    def SetDirectoryText(self, text):
        if text == "":
            self.Directory = r"D:\Python"
        else:
            self.Directory = text

    def SetLabelText(self, text):
        if text == "":
            self.Label = "Index_"
        else:
            self.Label = text

    def GetInfor(self):
        """主要处理函数"""
        self.Label = self.Label + '_'
        # print("关键字:", self.Title, " 数量: ", self.Number, " 保存目录: ", self.Directory, " 图像标签: ", self.Label)
        if self.Title == "默认值":
            # 使用information信息框
            reply = QMessageBox.information(self, "警告", "请填写相关信息", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            print(reply)
        else:
            NewTask = DownLoadControl(self.Title, self.Number, self.Directory, self.Label)
            try:
                # ProgressBarObject = MyProgressBar()
                # ProgressBarObject.show()
                # QApplication.processEvents()  # 实时显示
                NewTask.Main()  # 开始执行下载任务
            except Exception as e:
                print("运行错误:", e)
            # 打开下载完成的文件夹
            # qApp = QApplication.instance()
            # qApp.quit()
            # FILE = self.file   # 设置训练集地址

            # 将存储地址写入文件
            with open('./config/Information.txt', 'w') as f:
                f.write(self.file)
            os.startfile(self.file)
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyDownLoadWindow()
    myWin.show()
    sys.exit(app.exec_())






