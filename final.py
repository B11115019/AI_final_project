import cv2
import time
import excersice as ex

# 使用 OpenCV 从摄像头捕捉视频
cap = cv2.VideoCapture(0)

ptime = 0
point = 0
flag = True
excer = ex.pose()

while True:
    ret, img = cap.read()
    if not ret:
        print("failed")
    img = cv2.flip(img,1)

    # 将 BGR 帧转换为 RGB
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # 处理图像并获取姿态结果
    result = excer.pose.process(rgb_img)

    # 检测姿态并绘制结果
    img = excer.detect_pose(img, result)
    lmlist = excer.find_pose(img, result)

    if(len(lmlist) != 0):   
        # img, point, flag = excer.jumpingJacks(img, lmlist, point, flag)
        # img, point, flag = excer.LiftFeet(img, lmlist, point, flag)
        img, point, flag = excer.Squat(img, lmlist, point, flag)

    ctime = time.time()
    fps = 1/(ctime - ptime)
    ptime = ctime

    cv2.putText(img, "fps: " + str(int(fps)), (30, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    # 显示处理后的视频帧
    cv2.imshow("Image", img)
    cv2.waitKey(2)