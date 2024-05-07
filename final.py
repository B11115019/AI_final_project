import cv2
import time
import excersice as ex
from exercise_enum import *

# 使用 OpenCV 从摄像头捕捉视频
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 1280)

excer = ex.pose()
record = 0

# store file
mylist = load_GUI_list()

for i in range(len(mylist)):
    mylist[i] = cv2.resize(mylist[i], (128, 720)) # width = 128, height = 720


idx = 0
start_time = 0
break_time = 0
while True:
    while True:
        ctime = time.time()

        ret, img = cap.read()
        img = cv2.flip(img, 1)
        assert(img.shape == (720, 1280, 3))
        img[0:720, 0:128] = mylist[idx]
        
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # 处理图像并获取姿态结果
        result = excer.pose.process(rgb_img)

        # 检测姿态并绘制结果
        img = excer.detect_pose(img, result)
        lmlist = excer.find_pose(img, result)

        if len(lmlist) != 0:
            right_index_x = lmlist[20][0]
            right_index_y = lmlist[20][1]

            # 判斷是否確定要選擇這個運動
            if idx != GUIIndex.DEFAULT and int(ctime - start_time) == 2:
                if break_time == 0:
                    break_time = time.time()

                if idx == GUIIndex.SQUAT_HOVER:
                    idx = GUIIndex.SQUAT
                elif idx == GUIIndex.SIT_UP_HOVER:            
                    idx = GUIIndex.SIT_UP
                elif idx == GUIIndex.JUMP_HOVER:
                    idx = GUIIndex.JUMP
                elif idx == GUIIndex.LIFT_FEET_HOVER:
                    idx = GUIIndex.LIFT_FEET
            
            print(int(ctime - break_time))
            if idx == GUIIndex.SQUAT or idx == GUIIndex.SIT_UP or idx == GUIIndex.JUMP or idx == GUIIndex.LIFT_FEET:
                cv2.putText(img, str(2 - int(ctime - break_time)), (300, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                if int(ctime - break_time) == 2:
                    break
                
            # 移動選擇運動類型
            if right_index_x < 128:
                if 2 - int(ctime - start_time) > 0:
                    cv2.putText(img, str(2 - int(ctime - start_time)), (300, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                
                if break_time == 0:
                    if right_index_y < 120:
                        idx = GUIIndex.SQUAT_HOVER
                    elif right_index_y < 320:
                        idx = GUIIndex.SIT_UP_HOVER
                    elif right_index_y < 465:
                        idx = GUIIndex.JUMP_HOVER
                    elif right_index_y < 595:
                        idx = GUIIndex.LIFT_FEET_HOVER
            else:
                start_time = time.time()
                idx = 0
                break_time = 0

        cv2.imshow("Image", img)
        cv2.waitKey(2)


    break # 先測試前面
    point = 0
    flag = True
    record = max(record, point)
    start = time.time()

    while True:
        ret, img = cap.read()
        if not ret:
            print("failed")
        # img.resize(800, 800)
        img = cv2.flip(img,1)

        # 将 BGR 帧转换为 RGB
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # 处理图像并获取姿态结果
        result = excer.pose.process(rgb_img)

        # 检测姿态并绘制结果
        img = excer.detect_pose(img, result)
        lmlist = excer.find_pose(img, result)

        if len(lmlist) != 0:   
            if choice == 1:
                img, point, flag = excer.jumpingJacks(img, lmlist, point, flag)
            elif choice == 2:
                img, point, flag = excer.LiftFeet(img, lmlist, point, flag)
            elif choice == 3:
                img, point, flag = excer.Squat(img, lmlist, point, flag)

        ctime = time.time()

        cv2.putText(img, "time: " + str(60 - int(ctime - start)) + "sec", (30, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        # 显示处理后的视频帧
        cv2.imshow("Image", img)
        cv2.waitKey(2)

        if ctime - start > 10:
            break