import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from TFRecordBar import Ui_TFRecordProcess

class MyTFRecordProcessBar(QMainWindow, Ui_TFRecordProcess):
    def __init__(self, parent=None):
        super(MyTFRecordProcessBar, self).__init__(parent)
        self.setupUi(self)
        self.label.setText("开始")
        self.pushButton.clicked.connect(self.DoCancel)  # 取消按钮点击事件
        self.state = True
        self.progressBar.setValue(0)

    def DoCancel(self):
        """关闭当前窗口"""
        self.state = False
        self.close()

    def getstate(self):
        return self.state

    def setPercent(self, Number):
        self.progressBar.setValue(Number)

    def setLabelText(self, text):
        self.label.setText(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyTFRecordProcessBar()
    myWin.show()
    sys.exit(app.exec_())



