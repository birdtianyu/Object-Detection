import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'   # 忽略掉TensorFlow给的有关我的CPU计算速度的问题

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import glob
import cv2

# 用于可视化过程
from matplotlib import cm
from sklearn.manifold import TSNE


# tfrecord数据读取函数
def read_and_decode(filename, SIZE):
    # 创建文件队列,不限读取的数量
    filename_queue = tf.train.string_input_producer([filename])
    reader = tf.TFRecordReader()
    # reader从文件队列中读入一个序列化的样本
    _, serialized_example = reader.read(filename_queue)
    # 解析符号化的样本
    features = tf.parse_single_example(
        serialized_example,
        features={
            'label': tf.FixedLenFeature([], tf.int64),
            'img_raw': tf.FixedLenFeature([], tf.string)
        })
    label = features['label']
    img = features['img_raw']
    img = tf.decode_raw(img, tf.uint8)
    img = tf.reshape(img, [SIZE, SIZE, 1])
    #img = tf.cast(img, tf.float32) * (1. / 255) - 0.5
    label = tf.cast(label, tf.int32)
    return img, label


# 可视化最后一层
def plot_with_labels(lowDWeights, labels):
    plt.cla()  # 清空当前图像
    X, Y = lowDWeights[:, 0], lowDWeights[:, 1]
    for x, y, s in zip(X, Y, labels):
        c = cm.rainbow(int(255 * s / 9))
        plt.text(x, y, s, backgroundcolor=c, fontsize=9)
    plt.xlim(X.min(), X.max())
    plt.ylim(Y.min(), Y.max())
    plt.title('Visualize last layer')     # 图表名称
    plt.show()
    plt.pause(0.01)


# 导入指定数量的图片
def load_imgs(path, batch_size, SIZE):
    Imgs = []
    Name = []
    temp = 0
    class_path = path + "/*.jpg"
    for item in glob.glob(class_path):
        if temp < batch_size:
            img = cv2.imread(item, 0)                  # 灰度模式打开图像
            img = np.reshape(img, [SIZE, SIZE, 1])
            Imgs.append(img)
            Name.append(item.split('\\')[-1])
            temp = temp + 1
        else:
            break
    print("成功取出", len(Imgs), "张图片")
    # Imgs = np.reshape(Imgs, [batch_size, SIZE, SIZE, 1])
    Imgs = np.reshape(Imgs, [batch_size, SIZE, SIZE, 1])
    return Imgs, Name


# 读取一张图片并进行预处理
def Read_Img(path, SIZE):
    """返回处理后的图像和裁剪坐标"""
    img = cv2.imread(path, 0)               # 灰度模式打开图像
    img = cv2.medianBlur(img, 7)            # 模糊图像，降噪
    th1 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)  # 背景黑色，物体白色
    th2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)      # 背景白色，物体黑色
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
    closed = cv2.morphologyEx(th1, cv2.MORPH_CLOSE, kernel)
    image, cnts, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
    rect = cv2.minAreaRect(c)
    box = np.int0(cv2.boxPoints(rect))
    # print("box ", box)
    # cv2.drawContours(img, [box], -1, (0, 255, 0), 3)   # 画出矩形区域
    # 矩形
    Xs = [i[0] for i in box]
    Ys = [i[1] for i in box]
    x1 = min(Xs)
    x2 = max(Xs)
    y1 = min(Ys)
    y2 = max(Ys)
    # 防止出边界
    if x1 < 0:
        x1 = 0
    if x2 < 0:
        x2 = 0
    if y1 < 0:
        y1 = 0
    if y2 < 0:
        y2 = 0
    cropImg = th2[y1:y2, x1:x2]    # 裁剪
    Rect = (x1, y1, x2, y2)                      # 裁剪坐标
    finish = cv2.resize(cropImg, (SIZE, SIZE))   # 重新给定图像大小，缩放图像
    return finish, Rect

if __name__ == "__main__":
    img, Rect = Read_Img("D:/Python/car/car1.jpg", 100)
    print(Rect)
    cv2.imshow("name", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


