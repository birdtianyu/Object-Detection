import sys
import glob  # 用来找到所有满足要求的文件

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from ShowImagesWindow import Ui_ShowImagesWin

class MyShowImagesWindow(QMainWindow, Ui_ShowImagesWin):
    def __init__(self, parent=None):
        super(MyShowImagesWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton_1.clicked.connect(self.directoryOpen)
        self.Imgs = []

    def directoryOpen(self):
        """打开文件夹"""
        try:
            directory = QFileDialog.getExistingDirectory(self, "打开", "D:/Python/Text")  # 打开文件夹位置
            print(directory)
        except Exception as e:
            print("错误: ", e)
        # 添加所有图片地址到列表中
        target1 = directory + '/*.jpg'
        print(target1)
        self.Imgs.extend(glob.glob(str(target1)))
        target2 = directory + '/*.png'
        print(target2)
        self.Imgs.extend(glob.glob(str(target2)))
        # print("所有图片地址: \n", self.Imgs)

        for item in self.Imgs:
            print(item)
            label = QLabel()
            label.setPixmap(QPixmap(item))


def main():
    app = QApplication(sys.argv)
    myWin = MyShowImagesWindow()
    myWin.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()



