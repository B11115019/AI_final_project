import cv2
import time
import excersice as ex

# 使用 OpenCV 从摄像头捕捉视频
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 1280)

excer = ex.pose()
record = 0

# store file
mylist = []
mylist.append(cv2.imread("data/data/default.png")) # 0
mylist.append(cv2.imread("data/data/jump_hover.png")) # 1
mylist.append(cv2.imread("data/data/jump.png")) # 2
mylist.append(cv2.imread("data/data/push_up_hover.png")) # 3
mylist.append(cv2.imread("data/data/push_up.png")) # 4
mylist.append(cv2.imread("data/data/sit_up_hover.png")) # 5
mylist.append(cv2.imread("data/data/sit_up.png")) # 6
mylist.append(cv2.imread("data/data/squat_hover.png")) # 7
mylist.append(cv2.imread("data/data/squat.png")) # 8

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
            if idx != 0 and int(ctime - start_time) == 2:
                if break_time == 0:
                    break_time = time.time()

                if idx == 7:
                    idx = 8
                elif idx == 5:            
                    idx = 6
                elif idx == 1:
                    idx = 2
                elif idx == 3:
                    idx = 4
            
            print(int(ctime - break_time))
            if idx == 8 or idx == 6 or idx == 2 or idx == 4:
                cv2.putText(img, str(2 - int(ctime - break_time)), (300, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                if int(ctime - break_time) == 2:
                    break
                
            # 移動選擇運動類型
            if right_index_x < 128:
                if 2 - int(ctime - start_time) > 0:
                    cv2.putText(img, str(2 - int(ctime - start_time)), (300, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                
                if break_time == 0:
                    if right_index_y < 120:
                        idx = 7
                    elif right_index_y < 320:
                        idx = 5
                    elif right_index_y < 465:
                        idx = 1
                    elif right_index_y < 595:
                        idx = 3
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