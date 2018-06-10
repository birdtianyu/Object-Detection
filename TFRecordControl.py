import os
import tensorflow as tf
from PIL import Image
import glob
import cv2
import numpy as np

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog
from CallTFRecordBar import MyTFRecordProcessBar

### 控制TFRecord制作和读取过程

# 制作TFRecords数据
def create_record(orig_picture, classes, size, per_num, TFRecordname, Output, classes_num, save_path):
    Name = save_path + '/' + TFRecordname + ".tfrecords"
    writer = tf.python_io.TFRecordWriter(Name)
    # print("创建写者成功！")
    per_num = int(per_num)    # 这个类型错误找了好久
    size = int(size)
    classes_num = int(classes_num)
    for index, name in enumerate(classes):
        class_path = orig_picture + "/" + name + "/*.jpg"
        temp = 1
        for item in glob.glob(str(class_path)):
            # print("进入递归")
            if temp < int(per_num):
                try:
                    print("item: ", item)
                    img = cv2.imread(item, 0)  # 灰度模式打开图像
                    img = cv2.medianBlur(img, 7)  # 模糊图像，降噪
                    th1 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11,
                                                2)  # 背景黑色，物体白色
                    th2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11,
                                                2)  # 背景白色，物体黑色
                    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
                    closed = cv2.morphologyEx(th1, cv2.MORPH_CLOSE, kernel)
                    # img = img.resize((SIZE, SIZE))   # 设置需要转换的图片大小
                    image, cnts, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
                    rect = cv2.minAreaRect(c)
                    box = np.int0(cv2.boxPoints(rect))
                    cv2.drawContours(img, [box], -1, (0, 255, 0), 3)
                    # 矩形
                    Xs = [i[0] for i in box]
                    Ys = [i[1] for i in box]
                    x1 = min(Xs)
                    x2 = max(Xs)
                    y1 = min(Ys)
                    y2 = max(Ys)
                    if x1 < 0:
                        x1 = 0
                    if x2 < 0:
                        x2 = 0
                    if y1 < 0:
                        y1 = 0
                    if y2 < 0:
                        y2 = 0
                    hight = y2 - y1
                    width = x2 - x1
                    cropImg = th2[y1:y1 + hight, x1:x1 + width]  # 裁剪
                    finish = cv2.resize(cropImg, (size, size))  # 重新给定图像大小，缩放图像
                    img_raw = finish.tobytes()  # 将图片转化为原生bytes，numpy方法
                    print("分组:", index, "第", temp, "张")
                    no2 = "分组:" + str(index) + "第" + str(temp) + "张"
                    Output.setLabelText(no2)
                    example = tf.train.Example(
                        features=tf.train.Features(feature={
                            "label": tf.train.Feature(int64_list=tf.train.Int64List(value=[index])),
                            'img_raw': tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_raw]))
                        }))
                    temp = temp + 1
                    writer.write(example.SerializeToString())
                    Output.setPercent((temp / (per_num * classes_num)) * 100)
                    QApplication.processEvents()  # 实时显示
                except Exception as e:
                    print(e)
            else:
                break
    writer.close()

# 读取TFRecords数据
def read_and_decode(filename, size):
    size = int(size)
    # 创建文件队列,不限读取的数量
    filename_queue = tf.train.string_input_producer([filename])
    reader = tf.TFRecordReader()
    # reader从文件队列中读入一个序列化的样本
    _, serialized_example = reader.read(filename_queue)
    # get feature from serialized example
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
    img = tf.reshape(img, [size, size, 1])
    label = tf.cast(label, tf.int32)
    return img, label


def handle(orig_picture, classes, size, per_num, TFRecordname, save_path):
    per_num = int(per_num)   # 这个错误要命啊！！！
    size = int(size)
    # 创建一个进度条
    ProgressBarObject = MyTFRecordProcessBar()
    ProgressBarObject.show()  # 不能callable
    QApplication.processEvents()  # 实时显示
    print("创建进度条成功！")
    classes = list(classes)
    classes_num = len(classes)
    print("classes_num: ", classes_num)
    create_record(orig_picture, classes, size, per_num, TFRecordname, ProgressBarObject, classes_num, save_path)
    print("图片整理结束")
    ProgressBarObject.setLabelText("图片整理结束")
    QApplication.processEvents()  # 实时显示

    Name = save_path + '/' + TFRecordname + ".tfrecords"   # 这里也有错
    batch = read_and_decode(Name, size)
    print("载入图片结束")
    ProgressBarObject.setLabelText("载入图片结束")
    QApplication.processEvents()   # 实时显示

    init_op = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())

    with tf.Session() as sess:     # 开始一个会话
        sess.run(init_op)
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(coord=coord)

        print("*****************")
        ProgressBarObject.setLabelText("*****************")
        QApplication.processEvents()  # 实时显示

        try:
            for i in range(per_num * classes_num):
                example, lab = sess.run(batch)  # 在会话中取出image和label
                # img = Image.fromarray(example, 'RGB')    # 这里Image是之前提到的
                # img.save(save_path + '/' + str(i + 1) + '_' + str(list(classes)[lab]) + '.jpg')  # 存下图片;注意cwd后边加上‘/’
                path_save = save_path + '/' + str(i + 1) + '_' + str(classes[lab]) + '.jpg'
                cv2.imwrite(path_save, example)  # 保存图像
                # print(example, lab)
        except Exception as e:
            print(e)

        coord.request_stop()
        coord.join(threads)
        sess.close()

    with open('./config/InformationRes.txt', 'w') as f:
        f.write(save_path)
    os.startfile(save_path)



