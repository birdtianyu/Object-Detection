from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import cv2
from MyWindow import Ui_MainWindow

# 利用PyQt 的QLabel显示视频：
# 借助QTimer，不断产生事件，显示图片
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.timer_camera = QTimer(self)
        self.cap = cv2.VideoCapture(0)
        self.timer_camera.timeout.connect(self.show_pic)
        self.timer_camera.start(10)
    
    def show_pic(self):
        success, frame = self.cap.read()
        if success:
            show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(showImage))

            show2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            showImage2 = QImage(show2.data, show2.shape[1], show2.shape[0], QImage.Format_Grayscale8)
            self.label_2.setPixmap(QPixmap.fromImage(showImage2))
            self.label_3.setPixmap(QPixmap.fromImage(showImage))
            self.label_4.setPixmap(QPixmap.fromImage(showImage))
            self.timer_camera.start(10)
            self.statusbar.showMessage("成功打开摄像头")

if __name__=='__main__':
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
