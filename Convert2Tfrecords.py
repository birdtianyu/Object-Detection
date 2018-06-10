import os
import tensorflow as tf
from PIL import Image
import glob
import cv2

"""将原始图片转换成需要的大小，并将其保存 """

# 原始图片的存储位置
orig_picture = r'D:/Python/Train_Data/TensorFlow_Data/Sample'

# 生成图片的存储位置
gen_picture = r'D:/Python/Train_Data/TensorFlow_Data/Inputdata'

# 需要的识别类型
classes = {'Gun', 'Knife', 'Lighter'}

# 每个文件夹选取多少张图片
num_one_class = 100

# 样本总数
num_samples = 3 * num_one_class


# 制作TFRecords数据
def create_record():
    writer = tf.python_io.TFRecordWriter("Detection_train.tfrecords")
    for index, name in enumerate(classes):
        class_path = orig_picture + "/" + name + "/*.jpg"
        temp = 1    # 计数器
        for item in glob.glob(class_path):
            if temp <= num_one_class:
                print("item: ", item)
                img = Image.open(item).convert("RGB")      # 我的天啊，少了这个.convert("RGB")要了我的命
                img = img.resize((64, 64))                 # 设置需要转换的图片大小
                img_raw = img.tobytes()                    # 将图片转化为原生bytes
                print("分组:", index, "第", temp, "张")
                example = tf.train.Example(
                    features=tf.train.Features(feature={
                        "label": tf.train.Feature(int64_list=tf.train.Int64List(value=[index])),
                        'img_raw': tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_raw]))
                    }))
                temp = temp + 1
                writer.write(example.SerializeToString())
            else:
                break
    writer.close()


def read_and_decode(filename):
    # 创建文件队列,不限读取的数量
    filename_queue = tf.train.string_input_producer([filename])
    # create a reader from file queue
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
    img = tf.reshape(img, [64, 64, 3])
    # img = tf.cast(img, tf.float32) * (1. / 255) - 0.5
    label = tf.cast(label, tf.int32)
    return img, label


if __name__ == '__main__':
    create_record()
    print("图片整理结束")
    batch = read_and_decode('Detection_train.tfrecords')
    print("载入图片结束")
    init_op = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())

    with tf.Session() as sess:  # 开始一个会话
        sess.run(init_op)
        coord = tf.train.Coordinator()                          # 创建一个协调器，管理线程
        threads = tf.train.start_queue_runners(coord=coord)     # 启动QueueRunner, 此时文件名队列已经进队。
        print("*************************************************************************")
        for i in range(num_samples):
            example, lab = sess.run(batch)  # 在会话中取出image和label
            img = Image.fromarray(example, 'RGB')  # 这里Image是之前提到的
            img.save(gen_picture + '/' + str(i + 1) + '_' + str(list(classes)[lab]) + '.jpg')  # 存下图片;注意cwd后边加上‘/’
            # print(example, lab)
            # print("stop")
        coord.request_stop()
        coord.join(threads)
        sess.close()
