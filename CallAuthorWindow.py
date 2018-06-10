import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from AuthorWindow import Ui_AuthorWindow

class MyAuthorWindow(QMainWindow, Ui_AuthorWindow):
    def __init__(self):
        super(MyAuthorWindow, self).__init__()
        self.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyAuthorWindow()
    myWin.show()
    sys.exit(app.exec_())




