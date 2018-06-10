from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore  import *


class ImageWidget(QWidget):
    """一小块图片"""
    # 单选,上一个被选择的对象
    prevSelected = None

    def __init__(self):
        super(ImageWidget, self).__init__()
        self.id = 0
        self.displayText = ''  # 显示的文字
        self.version = ''
        self.status = 0
        self.path = ''
        self.showStatus = True
        self.selected = False
        self.isHightlight = False
        self.thumb = QImage()
        self.initAttrib()

    def initAttrib(self):
        """初始属性"""
        self.name_font = QFont()
        self.bg_color = QColor(50, 50, 50)
        self.hightlight = QColor(255, 255, 255, 100)
        self.edge_size = 5
        self.pen_selected = QPen(QColor(255, 255, 0))
        self.pen_selected.setWidth(self.edge_size)
        self.pen_selected.setJoinStyle(Qt.MiterJoin)


    def setThumb(self, thumb=None):
        if not thumb:
            thumb = self.thumbFile()
        if os.path.isfile(thumb):
            self.thumb.load(thumb)
            self.repaint()
            return True

    def paintAsThumb(self, painter):
        name_height = max(self.height() * 0.15, 20)
        name_ty = self.height() - self.edge_size * 2
        # draw background
        painter.fillRect(self.rect(), self.bg_color)
        painter.drawImage(self.rect(), self.thumb)
        # draw hightlight
        if self.isHightlight and not self.selected:
            painter.fillRect(self.rect(), self.hightlight)
        # draw name
        painter.setPen(QPen(QColor(255, 255, 255)))
        self.name_font.setPixelSize(name_height)
        painter.setFont(self.name_font)
        # 脚标字符
        painter.drawText(self.edge_size, name_ty, str(self.displayText))

        if self.status:
            title_height = self.edge_size + name_height
            p1 = QPoint(0, 0)
            p2 = QPoint(0, title_height)
            p3 = QPoint(title_height, 0)
            painter.setPen(Qt.NoPen)
            painter.fillRect(0, 0, self.width(), title_height, QColor(40, 40, 40, 40))
            if self.status == 1:
                painter.setBrush(QBrush(QColor(255, 0, 0)))
            elif self.status == 2:
                painter.setBrush(QBrush(QColor(0, 255, 0)))
            elif self.status == 3:
                painter.setBrush(QBrush(QColor(0, 0, 255)))
            painter.drawConvexPolygon(p1, p2, p3)

        if self.version:
            version_x = self.width() - self.edge_size - name_height * 1.5
            version_y = name_height
            painter.setPen(QPen(QColor(255, 255, 255)))
            painter.drawText(version_x, version_y, '%s' % self.version)

        # draw selected
        if self.selected:
            painter.setPen(self.pen_selected)
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(self.edge_size / 2, self.edge_size / 2, \
                             self.width() - self.edge_size, self.height() - self.edge_size)

    # def paintEvent(self, event):
    #     painter = QPainter(self)
    #     self.paintAsThumb(painter)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            try:
                self.setSelected()
            except Exception as e:
                print("运行错误:", e)

    # def mouseDoubleClickEvent(self, event):
    #     # self.emit(SIGNAL('doubleClick'))
    #     pass

    def enterEvent(self, event):
        self.isHightlight = True
        self.repaint()

    def leaveEvent(self, event):
        self.isHightlight = False
        self.repaint()

    # 设定当前为选中状态
    def setSelected(self):
        # 取消其他缩略图的选择状态, 当前设为选择状态
        if ImageWidget.prevSelected != None:
            ImageWidget.prevSelected.selected = False
            ImageWidget.prevSelected.repaint()
        self.selected = True
        self.repaint()
        ImageWidget.prevSelected = self

        self.onWidgetClicked()
        # self.emit(SIGNAL("click"), self.id)

    def onWidgetClicked(self):
        print('on widget clicked')



