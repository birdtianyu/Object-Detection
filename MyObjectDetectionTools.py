import os
from matplotlib import pyplot as plt
import numpy as np
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import cv2

from collections import defaultdict
from io import StringIO
from PIL import Image

from object_detection.utils import ops as utils_ops
from utils import label_map_util
from utils import visualization_utils as vis_util
from moviepy.editor import *          # VideoFileClip
import imageio
imageio.plugins.ffmpeg.download()

sys.path.append("..")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # 只显示 Error

def DownLoad_Model(model_name='ssd_mobilenet_v1_coco_2017_11_17'):
    # 下载模型
    MODEL_FILE = model_name + '.tar.gz'
    DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'
    opener = urllib.request.URLopener()
    opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)  # 下载模型
    print("下载完毕")
    tar_file = tarfile.open(MODEL_FILE)  # 打开下载后的压缩包
    print("打开成功")
    for file in tar_file.getmembers():
        file_name = os.path.basename(file.name)
        if 'frozen_inference_graph.pb' in file_name:
            tar_file.extract(file, os.getcwd())  # 解压


def load_image_into_numpy_array(image):
    """把彩色图片转换成numpy矩阵"""
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)


def run_inference_for_single_image(image, graph):
    """识别一张图片"""
    with graph.as_default():
        with tf.Session() as sess:
            # 找到输入层和输出层的tensors名称
            ops = tf.get_default_graph().get_operations()
            all_tensor_names = {output.name for op in ops for output in op.outputs}
            tensor_dict = {}
            for key in [
                'num_detections', 'detection_boxes', 'detection_scores',
                'detection_classes', 'detection_masks'
            ]:
                tensor_name = key + ':0'
                if tensor_name in all_tensor_names:
                    tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(tensor_name)

            if 'detection_masks' in tensor_dict:
                detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
                detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
                # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
                real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
                detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
                detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
                detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                    detection_masks, detection_boxes, image.shape[0], image.shape[1])
                detection_masks_reframed = tf.cast(
                    tf.greater(detection_masks_reframed, 0.5), tf.uint8)
                # Follow the convention by adding back the batch dimension
                tensor_dict['detection_masks'] = tf.expand_dims(
                    detection_masks_reframed, 0)
            image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

            # Run inference
            output_dict = sess.run(tensor_dict, feed_dict={image_tensor: np.expand_dims(image, 0)})

            # output float32 numpy arrays --> int numpy arrays
            output_dict['num_detections'] = int(output_dict['num_detections'][0])
            output_dict['detection_classes'] = output_dict['detection_classes'][0].astype(np.uint8)
            output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
            output_dict['detection_scores'] = output_dict['detection_scores'][0]
            if 'detection_masks' in output_dict:
                output_dict['detection_masks'] = output_dict['detection_masks'][0]

    return output_dict


def My_Detect(image_path, category_index, detection_graph):
    """我的识别函数"""
    # 载入最终绘制图片
    # image_fin = cv2.imread(image_path)
    # 打开图片
    image = Image.open(image_path).convert("RGB")
    # 转换成numpy矩阵
    image_np = load_image_into_numpy_array(image)
    # 增加维度 [None, None, 3] --> [1, None, None, 3]
    image_np_expanded = np.expand_dims(image_np, axis=0)
    # 探测一张图片
    output_dict = run_inference_for_single_image(image_np, detection_graph)

    # 可视化探测结果
    vis_util.visualize_boxes_and_labels_on_image_array(
        image_np,
        output_dict['detection_boxes'],
        output_dict['detection_classes'],
        output_dict['detection_scores'],
        category_index,
        instance_masks=output_dict.get('detection_masks'),
        use_normalized_coordinates=True,
        line_thickness=8)

    # 窗口显示
    cv2.imshow(r'Finish Images', image_np)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def detect_objects(image_np, sess, detection_graph, category_index):
    """探测一张图片"""
    # images shape: [1, None, None, 3]
    image_np_expanded = np.expand_dims(image_np, axis=0)  # 增加一个维度
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    boxes = detection_graph.get_tensor_by_name('detection_boxes:0')  # 框选区域
    scores = detection_graph.get_tensor_by_name('detection_scores:0')  # 得分
    classes = detection_graph.get_tensor_by_name('detection_classes:0')  # 分类
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    # 探测结果
    (boxes, scores, classes, num_detections) = sess.run(
        [boxes, scores, classes, num_detections],
        feed_dict={image_tensor: image_np_expanded})

    # 可视化最终结果
    vis_util.visualize_boxes_and_labels_on_image_array(
        image_np,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=8)
    return image_np


def process_image(image, detection_graph, category_index):
    # 返回一张图片（RGB）
    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
            image_process = detect_objects(image, sess, detection_graph, category_index)
            return image_process


def Main_Detect_Image(imagePath, bar, MODEL_NAME='ssd_mobilenet_v1_coco_2017_11_17'):
    # 使用的模型地址
    PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
    # 标签路径 "./data/mscoco_label_map.pbtxt"
    PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')
    # mscoco_label_map.pbtxt中有90类物体
    NUM_CLASSES = 90
    processbar = bar        # 进度条
    processbar.setValue(5)  # 进度条
    # 载入模型
    detection_graph = tf.Graph()
    processbar.setValue(10)  # 进度条
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        processbar.setValue(20)       # 进度条
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            processbar.setValue(30)     # 进度条
            serialized_graph = fid.read()
            processbar.setValue(40)     # 进度条
            od_graph_def.ParseFromString(serialized_graph)
            processbar.setValue(50)     # 进度条
            tf.import_graph_def(od_graph_def, name='')
            processbar.setValue(60)     # 进度条

    # 载入标签
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                                use_display_name=True)
    category_index = label_map_util.create_category_index(categories)
    processbar.setValue(70)  # 进度条
    # 方式一: 使用OpenCV载入图片
    image_np = cv2.imread(imagePath)
    processbar.setValue(75)  # 进度条

    # 方式二: 使用Image载入图片
    # image = Image.open(image_path).convert("RGB")
    # 转换成numpy矩阵
    # image_np = load_image_into_numpy_array(image)

    image_fin = process_image(image_np, detection_graph, category_index)
    processbar.setValue(80)  # 进度条
    return image_fin    # 返回numpy数组


def Main_Detect_Video(videoPath, outPutPath, startTime, finishTime, MODEL_NAME='ssd_mobilenet_v1_coco_2017_11_17'):

    # 使用的模型地址
    PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
    # 标签路径 "./data/mscoco_label_map.pbtxt"
    PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')
    # mscoco_label_map.pbtxt中有90类物体
    NUM_CLASSES = 90

    # 载入模型
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

    # 载入标签
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                                use_display_name=True)
    category_index = label_map_util.create_category_index(categories)

    def special_process_image(image):
        result = process_image(image, detection_graph, category_index)
        return result

    clip1 = VideoFileClip(videoPath).subclip(int(startTime), int(finishTime))
    white_clip = clip1.fl_image(special_process_image)         # 必须是RGB图像才行
    print("white_clip:", type(white_clip))
    print()
    white_clip.write_videofile(outPutPath, audio=False)

def convert2gif(videoPath, outputPath):
    # 转换成gif格式文件
    clip1 = VideoFileClip(videoPath)
    clip1.write_gif(outputPath)


if __name__ == '__main__':
    # finish = Main_Detect_Image("D:/CZAAsMBVAAEjZtn.jpg")
    # # 窗口显示
    # cv2.imshow(r'Image', finish)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    Main_Detect_Video("D:/CutNEU.mp4", 'video_output3.mp4', 30, 32)



