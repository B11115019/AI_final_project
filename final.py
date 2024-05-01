import cv2
import mediapipe as mp
import time

# 初始化 MediaPipe 姿态检测
mp_pose = mp.solutions.pose
ptime = 0
pose = mp_pose.Pose(static_image_mode=False, 
                    model_complexity=1, 
                    enable_segmentation=False, 
                    min_detection_confidence=0.5)

# 初始化 MediaPipe 绘图工具
mp_drawing = mp.solutions.drawing_utils

def detect_pose(img):
    # 将 BGR 帧转换为 RGB
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # 处理图像并获取姿态结果
    result = pose.process(rgb_img)
    # 检查是否检测到姿态
    if result.pose_landmarks:
        # 绘制关键点和骨架
        mp_drawing.draw_landmarks(img, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    return img

# 使用 OpenCV 从摄像头捕捉视频
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        continue
    
    # 检测姿态并绘制结果
    annotated_frame = detect_pose(img)
    
    ctime = time.time()
    fps = 1/(ctime - ptime)
    ptime = ctime

    cv2.putText(img, "fps: " + str(int(fps)), (30, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, )
    # 显示处理后的视频帧
    cv2.imshow("Image", img)
    cv2.waitKey(2)

# 释放资源并关闭窗口
cap.release()
cv2.destroyAllWindows()