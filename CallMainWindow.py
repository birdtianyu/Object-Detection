import sys  # 不能删
import os   # 打开指定文件夹用
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # 只显示 Error

import cv2  # 打开摄像头和视频
from threading import Thread

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from MainWindow import Ui_MainWindow
from CallDownLoadBaiduImg import *
from CallTFRecordWindow import *
from CallAuthorWindow import *

from CNNmain import *             # 我的CNN网络
from labelImg import MainWindow   # 图片编辑窗口
from MyObjectDetectionTools import Main_Detect_Image  # 图片检测
from MyObjectDetectionTools import Main_Detect_Video  # 视频检测
from WaitGif import LoadingGifWin
from MyThreads import WorkThread

class MyCNN2Thread(Thread):
    def __init__(self, file):
        Thread.__init__(self)   # 要先初始化进程，坑爹
        self.file = str(file)
        self.result = 0

    def run(self):
        self.result = Main_Detect_Image(self.file)

    def getImg(self):
        return self.result

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.Child_BaiduDownLoad = MyDownLoadWindow()
        self.Child_TFRecord = MyTFRecordWindow()
        self.Child_Author = MyAuthorWindow()
        self.Child_ImgEditor = MainWindow(None, os.path.join(os.path.dirname(sys.argv[0]), 'data', 'predefined_classes.txt'),
                                          None)
        self.Child_WaitGif = LoadingGifWin()     # 等待Gif
        self.actionBaiduImage.triggered.connect(self.BaiduShow)         # 打开百度图片下载窗口
        self.actionTFRecord.triggered.connect(self.TFRecord)            # 打开数据集预处理窗口
        self.actionTensorboard.triggered.connect(self.OpenTensorBoard)  # 打开Tensorboard所在文件夹
        self.actionjupyter_Notebook.triggered.connect(self.OpenJupyterNoteBook)   # 打开jupyter notebook所在文件夹
        self.actionOpenData.triggered.connect(self.OpenDataPathf)       # 打开处理后的数据集图片位置
        self.actionOpenDataImgs.triggered.connect(self.OpenDataPathf)
        self.actionOpenImg.triggered.connect(self.OpenDataPath)         # 打开原始数据集图片位置
        self.actionAuthor.triggered.connect(self.AuthorInf)             # 开发者窗口
        self.actionOpenProject.triggered.connect(self.OpenMyProject)    # 打开本项目文件夹

        self.pushButton_openImg.clicked.connect(self.OpenImg)           # 打开图片
        self.actionOpenTarget.triggered.connect(self.OpenImg)
        self.actionClose.triggered.connect(self.closeImg)               # 关闭图片

        # 计时器
        self.timer_camera = QTimer(self)                                # 摄像头相应计时器1
        self.timer_camera2 = QTimer(self)                               # 计时器2

        self.pushButton_openCamera.clicked.connect(self.OpenCameraFirst)     # 打开摄像头
        self.actionOpenCamera.triggered.connect(self.OpenCameraFirst)
        self.pushButton_openVideo.clicked.connect(self.OpenVideoFirst)       # 打开视频
        self.actionOpenVideo.triggered.connect(self.OpenVideoFirst)
        self.actionSave.triggered.connect(self.SaveImg)                      # 保存图片
        self.actionImageEditor.triggered.connect(self.OpenEditor)            # 打开编辑图片界面
        self.facecheck = False   # 是否进行人脸识别
        self.pushButton_Start3.clicked.connect(self.SetFaceState)         # 人脸识别
        self.pushButton_videoResult.clicked.connect(self.VideoCheck)      # 视频识别

        self.file = None   # 要识别的图片文件
        self.movie = QMovie("./UI/loading.gif")  # 加载gif
        self.MyprogressBar.setValue(0)
        self.MyprogressBar.hide()           # 隐藏进度条

        # 设置预留文字
        self.lineEdit1.setPlaceholderText("起始刻")
        self.lineEdit2.setPlaceholderText("终止刻")

        # 限制文本输入为1到600的整数
        pIntValidator = QIntValidator(self)
        pIntValidator.setRange(1, 600)  # 设置输入整数的范围
        self.lineEdit1.setValidator(pIntValidator)
        self.lineEdit2.setValidator(pIntValidator)

        # 默认起始值
        self.FROM = -1
        self.TO = -1

        # 默认视频
        self.VideoFile = "D"

        # 隐藏视频截取输入框
        self.lineEdit1.hide()
        self.label_to.hide()
        self.lineEdit2.hide()

        # 当输入改变更新变量值
        self.lineEdit1.textChanged.connect(self.SetFROMText)
        self.lineEdit2.textChanged.connect(self.SetTOText)

        # 设置背景方式一
        # palette1 = QPalette()
        # palette1.setBrush(self.backgroundRole(), QBrush(QPixmap('./UI/background.png')))  # 设置背景图片
        # self.setPalette(palette1)

        self.pushButton_Start1.clicked.connect(self.StartCNN1)
        self.pushButton_Start2.clicked.connect(self.StartCNN2)

        self.Result_Img = None       # 处理结果图片

    def paintEvent(self, event):
        """设置背景方式二"""
        painter = QPainter(self)
        pixmap = QPixmap("./UI/bg7.jpg")
        # 绘制窗口背景，平铺到整个窗口，随着窗口改变而改变
        painter.drawPixmap(self.rect(), pixmap)

    def showTimeEditor(self):
        """显示时刻输入框"""
        self.lineEdit1.show()
        self.label_to.show()
        self.lineEdit2.show()

    def hideTimeEditor(self):
        """隐藏时刻输入框"""
        self.lineEdit1.hide()
        self.label_to.hide()
        self.lineEdit2.hide()

    def BaiduShow(self):
        """打开百度图片下载窗口"""
        try:
            self.Child_BaiduDownLoad.show()
            self.statusbar.showMessage("打开百度图片下载窗口成功")
        except Exception as e:
            print("打开百度图片下载窗口失败：", e)
            self.statusbar.showMessage("打开百度图片下载窗口失败")
        # self.statusbar.showMessage("成功下载图片到: ", FILE)

    def TFRecord(self):
        """打开数据集处理窗口"""
        try:
            self.Child_TFRecord.show()
            self.statusbar.showMessage("打开TFRecord数据集制作窗口成功")
        except Exception as e:
            print("打开TFRecord数据集制作窗口失败：", e)
            self.statusbar.showMessage("打开TFRecord数据集制作窗口失败")

    def AuthorInf(self):
        """开发者窗口"""
        self.Child_Author.show()

    @staticmethod
    def OpenTensorBoard():
        """打开生成的Tensorboard所在的文件夹"""
        # os.startfile(r"TensorBoard_Log")
        os.startfile(r"D:\Python\Train_Data\TensorFlow_Data\Train9_Log")

    @staticmethod
    def OpenJupyterNoteBook():
        """打开jupyter notebook所在文件夹"""
        try:
            os.startfile(r"D:\Python\Hello_everyone_Here_is_my_GitHub\TensorFlow_Models\models\research\object_detection")
        except Exception as e:
            print(e)

    @staticmethod
    def OpenDataPath():
        """打开原始数据集图片位置"""
        with open('./config/Information.txt', 'r') as f:
            ImgP = f.read()
        print(ImgP)
        os.startfile(ImgP)

    @staticmethod
    def OpenDataPathf():
        """打开处理后的数据集图片位置"""
        with open('./config/InformationRes.txt', 'r') as f:
            ImgR = f.read()
        print(ImgR)
        os.startfile(ImgR)

    def OpenMyProject(self):
        """打开本项目的文件夹"""
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.statusbar.showMessage(BASE_DIR)
        address = BASE_DIR + '/Detection'
        os.startfile(address)

    def OpenImg(self):
        """载入图片"""
        self.closeImg()            # 先清理
        self.MyprogressBar.hide()  # 隐藏进度条
        self.hideTimeEditor()      # 隐藏时刻框
        file, ok = QFileDialog.getOpenFileName(self, "打开", "D:/Python/Train_Data/TensorFlow_Data/Sample", "Image Files(*.jpg *.jpeg *.png)")
        self.file = file     # 保存图片
        if ok:
            pixmap = QPixmap(file)
            scaredPixmap = pixmap.scaled(500, 500, aspectRatioMode=Qt.KeepAspectRatio)  # 等比例缩放
            self.ImgLabel1.setPixmap(scaredPixmap)
            self.pushButton_Start1.setEnabled(True)   # 开始检测按钮1
            self.pushButton_Start2.setEnabled(True)   # 开始检测按钮2
            self.pushButton_Start3.setEnabled(False)  # 关闭检测按钮3
            self.pushButton_videoResult.setEnabled(False)  # 关闭检测按钮4
            self.statusbar.showMessage(file)
        else:
            print("获取图片地址信息失败")
            self.statusbar.showMessage("获取图片地址信息失败")

    def closeImg(self):
        self.MyprogressBar.hide()  # 隐藏进度条
        self.timer_camera.stop()
        self.facecheck = False     # 禁止检测人脸
        self.hideTimeEditor()      # 隐藏时刻框
        self.VideoFile = "D"       # 清理视频路径缓存
        try:
            self.cap.release()
            self.statusbar.showMessage("成功关闭摄像头")
        except Exception as e:
            pass
        try:
            self.capVideo.release()
            self.statusbar.showMessage("成功关闭视频")
        except Exception as e:
            pass
        self.pushButton_Start1.setEnabled(False)  # 关闭检测按钮1
        self.pushButton_Start2.setEnabled(False)  # 关闭检测按钮2
        self.pushButton_Start3.setEnabled(False)  # 关闭检测按钮3
        self.pushButton_videoResult.setEnabled(False)  # 关闭检测按钮4
        self.ImgLabel1.setText("清理成功")
        self.ImgLabel2.setText("清理成功")

    def OpenCameraFirst(self):
        self.closeImg()       # 先清理
        # 摄像头信息
        self.cap = cv2.VideoCapture(0)
        self.timer_camera.timeout.connect(self.OpenCamera)
        self.timer_camera.start(10)

    def OpenCamera(self):
        # cap = cv2.VideoCapture(0)
        success, frame = self.cap.read()
        if success:
            self.pushButton_Start1.setEnabled(False)  # 关闭检测按钮1
            self.pushButton_Start2.setEnabled(False)  # 关闭检测按钮2
            self.pushButton_Start3.setEnabled(True)   # 开启检测按钮3
            self.pushButton_videoResult.setEnabled(False)  # 关闭检测按钮4
            show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
            self.ImgLabel1.setPixmap(QPixmap.fromImage(showImage))

            if self.facecheck:
                # 人脸识别结果
                temp = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                face_cascade = cv2.CascadeClassifier(r'./cascades/haarcascade_frontalface_default.xml')
                faces = face_cascade.detectMultiScale(temp, 1.3, 5)
                img = frame
                for (x, y, w, h) in faces:
                    # print(x, y, w, h)    # 脸部位置
                    img = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # 绘制蓝色框
                show2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                showImageFace = QImage(show2.data, show2.shape[1], show2.shape[0], QImage.Format_RGB888)
                self.ImgLabel2.setPixmap(QPixmap.fromImage(showImageFace))

            self.timer_camera.start(10)
            self.statusbar.showMessage("成功打开摄像头")
        else:
            pass
            # print("读取摄像头视频流失败")

    def SetFaceState(self):
        self.facecheck = True
        print("是否进行人脸检测: ", self.facecheck)

    def OpenVideoFirst(self):
        """载入视频"""
        self.closeImg()  # 先清理
        file, ok = QFileDialog.getOpenFileName(self, "打开", "D:/", "Video Files(*.mp4 *.flv *.mkv)")
        if ok:
            self.VideoFile = file  # 缓存打开视频的路径
            self.capVideo = cv2.VideoCapture(file)
            self.timer_camera.timeout.connect(self.OpenVideo)
            self.timer_camera.start(10)
            self.pushButton_Start1.setEnabled(False)  # 关闭检测按钮1
            self.pushButton_Start2.setEnabled(False)  # 关闭检测按钮2
            self.pushButton_Start3.setEnabled(False)  # 关闭检测按钮3
            self.pushButton_videoResult.setEnabled(True)  # 开启检测按钮4
            self.statusbar.showMessage(file)
        else:
            print("获取视频地址信息失败")
            self.statusbar.showMessage("获取视频地址信息失败")

    def OpenVideoSecond(self, target):
        """载入结果视频"""
        self.capVideo2 = cv2.VideoCapture(target)
        self.timer_camera2.timeout.connect(self.OpenVideo2)
        self.timer_camera2.start(10)

    def OpenVideo(self):
        success, frame = self.capVideo.read()
        if success:
            show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
            showFin = QPixmap.fromImage(showImage)
            scaredPixmap = showFin.scaled(500, 500, aspectRatioMode=Qt.KeepAspectRatio)  # 等比例缩放
            self.ImgLabel1.setPixmap(scaredPixmap)
            self.showTimeEditor()  # 显示时刻框
            self.timer_camera.start(20)
            self.statusbar.showMessage("成功打开视频")

    def OpenVideo2(self):
        success, frame = self.capVideo2.read()
        if success:
            show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
            showFin = QPixmap.fromImage(showImage)
            scaredPixmap = showFin.scaled(500, 500, aspectRatioMode=Qt.KeepAspectRatio)  # 等比例缩放
            self.ImgLabel2.setPixmap(scaredPixmap)
            self.showTimeEditor()  # 显示时刻框
            self.timer_camera2.start(20)
            self.statusbar.showMessage("成功打开视频")

    def SaveImg(self):
        """保存图片结果"""
        filename, OK = QFileDialog.getSaveFileName(self, '保存结果图片', 'D:/', "Image Files(*.jpg *.jpeg *.png)")
        # print(filename, OK)
        if OK:
            if self.Result_Img is not None:
                fin = cv2.imwrite(filename, self.Result_Img)
                if fin:
                    mess = "保存图片成功 " + filename
                    self.statusbar.showMessage(mess)
                else:
                    self.statusbar.showMessage("保存图片失败")
            else:
                self.statusbar.showMessage("保存图片失败")
        else:
            self.statusbar.showMessage("载入保存图片路径失败")

    def StartCNN1(self):
        """使用我的CNN1进行检测"""
        self.MyprogressBar.show()   # 显示进度条
        if self.file is None:
            self.statusbar.showMessage("载入要识别的图片信息失败")
            self.MyprogressBar.hide()
            return
        self.statusbar.showMessage("载入要识别的图片信息成功")
        print(self.file)
        self.MyprogressBar.setValue(1)  # 进度条

        # try:
        #     mulithread = WorkThread(self.file, self.MyprogressBar)
        #     mulithread.trigger.connect(self.StartCNN1Second)
        #     mulithread.start()
        # except Exception as e:
        #     print(e)

        ##################
        Result, RectArea = Ando(Path=str(self.file), Is_Train=1, bar=self.MyprogressBar)   # 检测物体
        self.MyprogressBar.setValue(70)  # 进度条
        # print(Result, RectArea)
        img = cv2.imread(str(self.file))
        img = cv2.rectangle(img, (RectArea[0], RectArea[1]), (RectArea[2], RectArea[3]), (0, 255, 0), 3)  # 画出矩形区域
        # 参数：图片, 文字, 左下角坐标, 字体, 尺寸, 颜色, ?
        cv2.putText(img, Result, (RectArea[0] + 10, RectArea[3] - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        ##################

        self.MyprogressBar.setValue(80)  # 进度条
        height, width, bytesPerComponent = img.shape
        bytesPerLine = 3 * width
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
        QImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(QImg)
        scaredPixmap = pixmap.scaled(500, 500, aspectRatioMode=Qt.KeepAspectRatio)  # 等比例缩放
        self.MyprogressBar.setValue(99)  # 进度条
        self.ImgLabel2.setPixmap(scaredPixmap)   # 显示结果图片
        self.MyprogressBar.setValue(100)  # 进度条
        self.statusbar.showMessage("识别成功")
        self.MyprogressBar.hide()
        self.Result_Img = img

    def StartCNN1Second(self, imgs):
        self.MyprogressBar.setValue(80)  # 进度条
        height, width, bytesPerComponent = imgs.shape
        bytesPerLine = 3 * width
        cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB, imgs)
        QImg = QImage(imgs.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(QImg)
        scaredPixmap = pixmap.scaled(500, 500, aspectRatioMode=Qt.KeepAspectRatio)  # 等比例缩放
        self.MyprogressBar.setValue(99)  # 进度条
        self.ImgLabel2.setPixmap(scaredPixmap)  # 显示结果图片
        self.MyprogressBar.setValue(100)  # 进度条
        self.statusbar.showMessage("识别成功")
        self.MyprogressBar.hide()
        self.Result_Img = imgs

    def StartCNN2(self):
        """使用我的CNN2进行检测"""
        self.SetGif()
        self.MyprogressBar.show()  # 显示进度条
        # self.Child_WaitGif.show()  # 显示等待窗口
        if self.file is None:
            self.statusbar.showMessage("载入要识别的图片信息失败")
            self.MyprogressBar.hide()
            return
        self.statusbar.showMessage("载入要识别的图片信息成功")
        self.MyprogressBar.setValue(1)  # 进度条
        # th1 = MyCNN2Thread(self.file)
        # th1.start()
        # th1.join()
        # img_fin = th1.getImg()
        img_fin = Main_Detect_Image(self.file, self.MyprogressBar)
        self.MyprogressBar.setValue(95)  # 进度条
        height, width, bytesPerComponent = img_fin.shape
        bytesPerLine = 3 * width
        cv2.cvtColor(img_fin, cv2.COLOR_BGR2RGB, img_fin)
        QImg = QImage(img_fin.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(QImg)
        scaredPixmap = pixmap.scaled(500, 500, aspectRatioMode=Qt.KeepAspectRatio)  # 等比例缩放
        # self.movie.stop()
        self.MyprogressBar.setValue(100)  # 进度条
        self.ImgLabel2.setPixmap(scaredPixmap)                                      # 显示结果图片
        self.statusbar.showMessage("识别成功")
        self.MyprogressBar.hide()
        self.Result_Img = img_fin

    def SetGif(self):
        # 设置gif动画
        self.ImgLabel2.setMovie(self.movie)
        self.movie.start()

    def OpenEditor(self):
        """打开数据集图片编辑器"""
        try:
            self.Child_ImgEditor.show()
            self.statusbar.showMessage("打开数据集图片编辑器窗口成功")
        except Exception as e:
            print("打开数据集图片编辑器失败：", e)
            self.statusbar.showMessage("打开数据集图片编辑器窗口失败")

    def SetFROMText(self, text):
        """获取起始值"""
        # print("text", text)
        # print(type(text))
        if text == "":
            self.FROM = -1
        else:
            self.FROM = int(text)  # 注意变量类型

    def SetTOText(self, text):
        """获取终止值"""
        if text == "":
            self.TO = -1
        else:
            self.TO = int(text)  # 注意变量类型

    def VideoCheck(self):
        """视频检测"""
        # print("self.FROM  self.TO: ", self.FROM , self.TO)
        if self.FROM == -1 or self.TO == -1 or self.FROM >= self.TO:
            # 使用information信息框
            reply = QMessageBox.information(self, "警告", "请正确填写视频识别起始值", QMessageBox.Yes, QMessageBox.Yes)
            print(reply)
        else:
            Savefilename, OK = QFileDialog.getSaveFileName(self, '保存视频识别结果', 'D:/', "Video Files(*.mp4)")
            if OK:
                self.ImgLabel2.setText("距离识别结束可能需要十几分钟的时间，您可以出去走走散散心O(∩_∩)O哈哈~")
                if self.VideoFile == "D":
                    self.statusbar.showMessage("获取原视频地址信息失败")    # 默认视频地址
                    self.ImgLabel2.setText("清理成功")
                else:
                    Main_Detect_Video(self.VideoFile, Savefilename, self.FROM, self.TO)
                    self.OpenVideoSecond(Savefilename)
            else:
                print("获取视频保存地址信息失败")
                self.statusbar.showMessage("获取视频保存地址信息失败")


def MyMain():
    MyApp = QApplication(sys.argv)
    MainWin = MyMainWindow()
    MainWin.show()
    sys.exit(MyApp.exec_())

if __name__ == "__main__":
    MyMain()







