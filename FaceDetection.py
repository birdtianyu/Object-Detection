"""摄像头人脸检测"""
import cv2

face_cascade = cv2.CascadeClassifier(r'./cascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(r'./cascades/haarcascade_eye.xml')

"""构建过程"""
cameraCapture = cv2.VideoCapture(0)         #传入设备索引号构建
cv2.namedWindow('My Window')

"""一帧一帧判断显示"""
success, frame = cameraCapture.read()
while success:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    """绘制人脸"""
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    # print('faces', faces)
    for (x, y, w, h) in faces:
        img = cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)         #绘制蓝色框
        """绘制眼睛"""
        eye_gray = gray[y:y+h, x:x+w]                                          #缩小眼睛搜索范围
        eyes = eye_cascade.detectMultiScale(eye_gray, 1.03, 5, 0, (50, 50))
        # print('eyes', eyes)
        for (ex, ey, ew, eh) in eyes:
            # pass
            cv2.rectangle(img, (ex+x, ey+y), (ex+ew, ey+eh), (0, 255, 0), 2)  #绘制两个红色框
    cv2.imshow('My Window', frame)
    success, frame = cameraCapture.read()

cv2.destroyWindow('My Window')
cameraCapture.release()

