import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from ProgressBar import Ui_ProgressBarWin

class MyProgressBar(QMainWindow, Ui_ProgressBarWin):
    def __init__(self, parent=None):
        super(MyProgressBar, self).__init__(parent)
        self.setupUi(self)
        self.label.setText("开始下载")
        self.pushButton.clicked.connect(self.DoCancel)    # 取消按钮点击事件
        self.state = True

    def DoCancel(self):
        """关闭当前窗口"""
        self.state = False

    def getstate(self):
        return self.state

    def setPercent(self, Number):
        self.progressBar.setValue(Number)

    def setLabelText(self, text):
        self.label.setText(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyProgressBar()
    myWin.show()
    sys.exit(app.exec_())





