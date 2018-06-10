import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'   # 忽略掉TensorFlow给的有关我的CPU计算速度的问题

from CNNtools import *
from PyQt5 import QtCore, QtGui, QtWidgets

# 1. 设置模型参数参数
# Is_Train = 0                    # 是训练新模型还是使用旧模型
# Do_Painting = False             # 分类动态画出来
# Length = 100                    # 图形尺寸
# BATCH_SIZE = 10                 # 分片(批处理): 为了在内存效率和内存容量之间寻找最佳平衡。
# generations = 501               # 迭代多少代
# LearningRate = 0.0001           # 学习率
# num_targets = 3                 # 几类数据
# num_channels = 3                # 输入图片通道数（暂时废除）

CheckPath = r"D:/Python/Train_Data/TensorFlow_Data/Inputdata2"    # 模型实例化检测图片来源, 用于可视化最后一层过程
ContinuePath = r"D:/Python/Train_Data/TensorFlow_Data/Inputdata"  # 继续训练路径

def Ando(Path=None, Is_Train=1, Do_Painting=False, Length=100, BATCH_SIZE=10, generations=501, bar=None):
    """核心函数"""
    if Is_Train == 1 and Path is None:
        print("检测失败:请输入要检测的图片路径")
        return

    if Length != 100:
        print("注意训练图片尺寸输入值不等于100！！！")

    if bar is not None:
        processBar = bar          # 进度条
        processBar.setValue(0)  # 初始值
    else:
        print("bar必须有值")
        processBar = QtWidgets.QProgressBar()

    ###################################################
    #
    # 训练用户自己的模型方法：
    # 1.把下面这个地址改成您处理好的训练集地址
    # 2.修改目标种类数目
    # 3.修改每类输出的文字 -> 216行 264行
    # 4.调用本函数
    #   格式:Ando(Is_Train=0)
    #
    dataset_address = r"./Data/Detection9.tfrecords"  # 导入数据集地址
    num_targets = 3                                   # 几类数据
    ###################################################

    image_width = Length         # 输入图片宽度
    image_height = Length        # 输入图片高度
    SIZE = Length                # 调整宽度
    # TEST_SIZE = 20               # 一次网络使用读取几张图片, 用于在训练中读入数据进行预测, 下面给注释掉了
    LearningRate = 0.0001        # 学习率
    max_pool_size1 = 2           # 最大池化第一层 NxN window
    max_pool_size2 = 2           # 最大池化第二层 NxN window
    fully_connected_size1 = 100  # 全连接第一层结点数
    save_address = r"./TensorBoard_Log"                      # tensorboard数据存储地址
    # testset_address = r"./Data/Detection2_test.tfrecords"    # 导入测试集地址
    Saver_address = r'./My_Train_model/my_model.ckpt'        # 参数和模型保存地址
    print("进入Ando函数")
    processBar.setValue(5)     # 进度条

    ###########################################模型结构##########################################
    tf.reset_default_graph()     # 清除默认图的堆栈，并设置全局图为默认图: 修复只能识别一次的问题

    # 2. 初始化变量和占位符
    x_input = tf.placeholder(tf.float32,
                             [None, image_width, image_height, 1],
                             name="x_input") / 255.  # 输入图片占位符, 这里/255.是为了将像素值归一化到[0.0, 1.0]
    y_label = tf.placeholder(tf.int32, [None, num_targets], name="y_label")  # 输入标签占位符
    keep_prob = tf.placeholder(tf.float32, name="keep_out_percent")          # dropout率

    # 3. 导入训练数据集
    image, label = read_and_decode(dataset_address, SIZE)
    image_batches, label_batches = tf.train.shuffle_batch(
        [image, label],
        batch_size=BATCH_SIZE,
        capacity=64,
        min_after_dequeue=4
    )  # 使用shuffle_batch可以随机打乱输入, 保证min_after_dequeue小于capacity, 否则会报错

    # 4. 转换和归一化数据
    label_batches = tf.expand_dims(label_batches, 1)
    indices = tf.expand_dims(tf.range(0, BATCH_SIZE, 1), 1)
    concated = tf.concat([indices, label_batches], 1)
    onehot_labels = tf.sparse_to_dense(concated, tf.stack([BATCH_SIZE, 3]), 1, 0)

    # 5. 定义模型结构
    # 卷积层1
    conv1 = tf.layers.conv2d(
        inputs=x_input,
        filters=8,
        kernel_size=5,
        strides=1,
        padding='SAME',
        activation=tf.nn.relu,
        name="conv1"
    )  # shape (64, 64, 1) -> (64, 64, 8)

    # 最大池化层1
    max_pool1 = tf.layers.max_pooling2d(
        conv1,
        pool_size=max_pool_size1,
        strides=2,
        name="max_pool1"
    )  # (64, 64, 8) -> (32, 32, 8)

    # 卷积层2
    conv2 = tf.layers.conv2d(
        max_pool1,
        filters=16,
        kernel_size=5,
        strides=1,
        padding='SAME',
        activation=tf.nn.relu,
        name="conv2"
    )  # (32, 32, 8) -> (32, 32, 16)

    # 最大池化层2
    max_pool2 = tf.layers.max_pooling2d(
        conv2,
        pool_size=max_pool_size2,
        strides=2,
        name="max_pool2"
    )  # (32, 32, 16) -> (16, 16, 16)

    # 全连接层变量
    resulting_width = image_width // (max_pool_size1 * max_pool_size2)
    resulting_height = image_height // (max_pool_size1 * max_pool_size2)
    resulting = resulting_width * resulting_height * 16
    flat_output = tf.reshape(max_pool2, [-1, resulting])  # 不然不能写None

    # 全连接层1
    fully_connected1 = tf.layers.dense(
        inputs=flat_output,
        units=fully_connected_size1,
        activation=tf.nn.relu,
        name="fully_connected1"
    )  # 100个结点     ->[BATCH_SIZE,100]

    # 全连接层2
    output = tf.layers.dense(
        inputs=fully_connected1,
        units=num_targets,
        name="fully_connected2"
    )  # 输出层3个结点  ->[BATCH_SIZE,3]

    # dropout层
    output = tf.nn.dropout(
        output,
        keep_prob,
        name="dropout"
    )  # -> shape=(10, 3), dtype=float32

    # 6. 定义损失函数
    loss = tf.reduce_sum(tf.nn.softmax_cross_entropy_with_logits(logits=output, labels=y_label))  # 损失函数
    train_op = tf.train.AdamOptimizer(LearningRate).minimize(loss)  # 优化器
    tf.summary.scalar('loss', loss)  # Tensorboard

    # 估计值与实际值之间的差别
    accuracy = tf.metrics.accuracy(labels=tf.argmax(y_label, axis=1), predictions=tf.argmax(output, axis=1))[1]
    # return (accuracy, update_op), and create 2 local variables

    ##############################################################################################################
    print("定义结构结束")
    processBar.setValue(10)  # 进度条

    if Is_Train == 0:

        # 保存模型和参数
        saver = tf.train.Saver()
        # saver = tf.train.Saver(max_to_keep=5, keep_checkpoint_every_n_hours=2)  #只保存最新的5个模型和参数, 每隔2个小时保存一次模型

        # 开始训练
        with tf.Session() as sess:
            init_op = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())
            sess.run(init_op)

            writer = tf.summary.FileWriter(str(save_address), sess.graph)  ## Tensorboard
            merge_op = tf.summary.merge_all()                              ## Tensorboard

            coord = tf.train.Coordinator()
            threads = tf.train.start_queue_runners(coord=coord)
            print("*************************************************************************")

            plt.ion()  # 开启交互模式
            for step in range(generations):
                example, lab = sess.run([image_batches, onehot_labels])     # 在会话中取出image和label
                _, loss_ = sess.run([train_op, loss], {x_input: example, y_label: lab, keep_prob: 0.5})

                _, result = sess.run([train_op, merge_op],
                                     {x_input: example, y_label: lab, keep_prob: 0.5})  # Tensorboard
                writer.add_summary(result, step)                                        # Tensorboard

                # 每隔50步打印一次
                if step % 100 == 0:
                    accuracy_ = sess.run(accuracy, {x_input: example, y_label: lab, keep_prob: 1.0})
                    print('Step:', step, '| train loss: %.4f' % loss_, '| test accuracy: %.2f' % accuracy_)
                    train_output = sess.run(output, {x_input: example, keep_prob: 1})
                    print("train_output :\n", train_output)
                    print('lab :\n', lab)
                    # saver.save(sess, save_path=Saver_address, global_step=step)
                    # 不用每次都保存计算图，计算图是不变的,所以可以下面这么写。
                    # saver.save(sess, save_path=Saver_address, global_step=step, write_meta_graph=False)
                    saver.save(sess, Saver_address)

                    if Do_Painting and step % 300 == 0 and step != 0:
                        # 可视化预测过程
                        tsne = TSNE(perplexity=30, n_components=2, init='pca', n_iter=5000)
                        Input, Name = load_imgs(CheckPath, 200, SIZE)     # 一次读200条数据
                        plot_only = 180                                   # 记住如果像上面那样，我一共只能放10个数据
                        flat_representation = sess.run(flat_output, {x_input: Input, keep_prob: 1.0})
                        low_dim_embs = tsne.fit_transform(flat_representation[:plot_only, :])
                        # 文件名称 --> 类别编号
                        for i, item in enumerate(Name):
                            a = item.split("__")[-1].split(".")[0]  # Gun
                            if a == "Gun":
                                Name[i] = 0
                            elif a == "Knife":
                                Name[i] = 1
                            elif a == "Lighter":
                                Name[i] = 2
                            else:
                                Name[i] = 3
                        # print(Name)
                        labels = Name[:plot_only]
                        plot_with_labels(low_dim_embs, labels)
                        # 在训练中读入数据进行预测
                        # if step % 500 == 0 and step != 0:
                        #     Input, Name = load_imgs(CheckPath, TEST_SIZE)
                        #     test_output = sess.run(output, {x_input: Input, keep_prob: 1})
                        #     pred_y = np.argmax(test_output, 1)   # 沿轴最大值的索引
                        #     for index, i in enumerate(pred_y):
                        #         if i == 0:
                        #             print('prediction number: ', i, " Gun", Name[index])
                        #         elif i == 1:
                        #             print('prediction number: ', i, " Knife", Name[index])
                        #         else:
                        #             print('prediction number: ', i, " Lighter", Name[index])
            plt.ioff()

            coord.request_stop()
            coord.join(threads)
            sess.close()

    elif Is_Train == 1:
        print("开始检测")
        processBar.setValue(15)  # 进度条
        saver = tf.train.Saver()
        processBar.setValue(18)  # 进度条
        Input, Rects = Read_Img(Path, SIZE)
        processBar.setValue(40)  # 进度条
        Input = np.reshape(Input, [1, SIZE, SIZE, 1])
        Result = "None"
        processBar.setValue(42)  # 进度条
        with tf.Session() as sess:
            saver.restore(sess, Saver_address)  # 注意此处路径前添加"./"
            processBar.setValue(50)  # 进度条
            test_output = sess.run(output, {x_input: Input, keep_prob: 1})
            processBar.setValue(60)  # 进度条
            print("预测概率: ", test_output)
            pred_y = np.argmax(test_output, 1)  # 沿轴最大值的索引
            # 每类输出文字
            for index, i in enumerate(pred_y):
                if i == 0:
                    # print('prediction: Gun')
                    Result = "Gun"
                elif i == 1:
                    # print('prediction: Knife')
                    Result = "Knife"
                else:
                    # print('prediction: Lighter')
                    Result = "Lighter"

            if test_output[0][pred_y] < 0:
                Result = "Unknown"     # 区分其它不相关物体

                # 卷积层1特征图
                # convOut1 = sess.run(conv1, {x_input: Input, keep_prob: 1})
                # print("conv1:shape", convOut1.shape)  # (1, 100, 100, 8)
                # conv1_transpose = sess.run(tf.transpose(convOut1, [3, 0, 1, 2]))
                # fig1, ax1 = plt.subplots(nrows=1, ncols=8, figsize=(8, 1))
                # for i in range(8):
                #     ax1[i].imshow(conv1_transpose[i][0])  # tensor的切片[row, column]
                # plt.title('Conv1 8x100x100')
                # plt.show()

                # 池化层1特征图
                # pooling1 = sess.run(max_pool1, {x_input: Input, keep_prob: 1})
                # print("max_pool1:shape", pooling1.shape)  # (1, 50, 50, 8)
                # pooling1_transpose = sess.run(tf.transpose(pooling1, [3, 0, 1, 2]))
                # fig2, ax2 = plt.subplots(nrows=1, ncols=8, figsize=(8, 1))
                # for i in range(8):
                #     ax2[i].imshow(pooling1_transpose[i][0])  # tensor的切片[row, column]
                # plt.title('max pooling1 8x50x50')
                # plt.show()

                # 卷积层2特征图
                # convOut2 = sess.run(conv2, {x_input: Input, keep_prob: 1})
                # print("conv2:shape", convOut2.shape)  # (1, 50, 50, 16)
                # conv2_transpose = sess.run(tf.transpose(convOut2, [3, 0, 1, 2]))
                # fig3, ax3 = plt.subplots(nrows=1, ncols=16, figsize=(16, 1))
                # for i in range(16):
                #     ax3[i].imshow(conv2_transpose[i][0])  # tensor的切片[row, column]
                # plt.title('Conv2 16x50x50')
                # plt.show()

                # 池化层2特征图
                # pooling2 = sess.run(max_pool2, {x_input: Input, keep_prob: 1})
                # print("max_pool2:shape", pooling2.shape)  # (1, 25, 25, 16)
                # pooling2_transpose = sess.run(tf.transpose(pooling2, [3, 0, 1, 2]))
                # fig4, ax4 = plt.subplots(nrows=1, ncols=16, figsize=(16, 1))
                # for i in range(16):
                #     ax4[i].imshow(pooling2_transpose[i][0])  # tensor的切片[row, column]
                # plt.title('max pooling2 16x25x25')
                # plt.show()

        print('prediction: ', Result)
        processBar.setValue(65)  # 进度条
        return Result, Rects

    elif Is_Train == 2:
        """继续训练"""
        print("非常抱歉, 此项功能待开发")

    else:
        print("Input error: 不要乱输入Is_Train的值")


if __name__ == "__main__":
    # Ando(Is_Train=0)  # OK
    # Ando(Is_Train=0, Do_Painting=True)  # 可视化训练结果OK
    # TensorBoard OK

    # Ok
    # Res, Rec = Ando(Path="D:\Python\car\Gun3.jpg", Is_Train=1)   # OK
    # print(Res, Rec)
    # img = cv2.imread("D:\Python\car\Gun3.jpg")
    # img = cv2.rectangle(img, (Rec[0], Rec[1]), (Rec[2], Rec[3]), (0, 255, 0), 3)                  # 画出矩形区域
    # cv2.putText(img, Res, (Rec[0]+10 , Rec[3]-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)   # 图片, 文字, 左下角坐标, 字体, 尺寸, 颜色, ?
    # cv2.imshow("name", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    First = 0
    while True:
        name = input("请输入地址：")
        Res, Rec = Ando(First=First, Path=name, Is_Train=1)
        First = 1
        print(Res, Rec)












