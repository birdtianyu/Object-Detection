import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog

from firstWin import Ui_MainWindow
from ChildForm1 import Ui_Form


class MainForm(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainForm, self).__init__()
        self.setupUi(self)
        self.child = ChildrenForm()
        self.fileOpenAction.triggered.connect(self.openMsg)
        self.fileCloseAction.triggered.connect(self.close)
        self.AddWinAction.triggered.connect(self.childShow)

    def openMsg(self):
        #file, ok = QFileDialog.getOpenFileName(self, "打开", "D:/Python", "All Files(*);;Text Files(*.txt)")
        file = QFileDialog.getExistingDirectory(self, "打开", "D:/Python")  # 打开文件夹位置
        # .getOpenFileNames(self, "打开", "D:/Python", "All Files(*);;Text Files(*.txt)")
        self.statusbar.showMessage(file)

    def childShow(self):
        self.MaingridLayout.addWidget(self.child)
        self.child.show()
        # car_sliding_windows.Excute()


class ChildrenForm(QWidget, Ui_Form):
    def __init__(self):
        super(ChildrenForm, self).__init__()
        self.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainForm()
    win.show()
    sys.exit(app.exec_())