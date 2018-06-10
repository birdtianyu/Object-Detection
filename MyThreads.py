
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import numpy as np

class WorkThread(QThread):
    trigger = pyqtSignal(np.ndarray)

    def __init__(self, file, bar):
        super(WorkThread, self).__init__()
        self.file = str(file)
        self.MyprogressBar = bar
        self.result = 0

    def run(self):
        print("run thread")
        Result, RectArea = Ando(Path=str(self.file), Is_Train=1, bar=self.MyprogressBar)  # 检测物体
        print(Result, RectArea)
        self.MyprogressBar.setValue(70)  # 进度条
        img = cv2.imread(str(self.file))
        img = cv2.rectangle(img, (RectArea[0], RectArea[1]), (RectArea[2], RectArea[3]), (0, 255, 0), 3)  # 画出矩形区域
        cv2.putText(img, Result, (RectArea[0] + 10, RectArea[3] - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        self.trigger.emit(img)  # 循环完毕后发出信号