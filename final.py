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


def capture_and_detect_pose():
    """
    從相機讀入一幀，並做姿態檢測 + 繪製骨架
    ## Return:
    - img - 圖片
    - lmlist - 檢測到的骨架的節點
    """
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    assert(img.shape == (720, 1280, 3))

    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # 处理图像并获取姿态结果
    result = excer.pose.process(rgb_img)

    # 检测姿态并绘制结果
    img = excer.detect_pose(img, result)
    lmlist = excer.find_pose(img, result)

    return img, lmlist


def select_exercise_with_cam() -> ExerciseChoise:
    """
    使用相機來選擇動作
    """
    idx = 0
    start_time = time.time()

    while True:
        # 目前的時間
        ctime = time.time()
        # 經過的時間
        pass_time = int(ctime - start_time)

        img, lmlist = capture_and_detect_pose()

        # 顯示倒數秒數
        if idx != GUIIndex.DEFAULT:
            cv2.putText(img, str(2 - pass_time), (300, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

        # set up GUI
        img[0:720, 0:128] = mylist[idx]

        cv2.imshow("Image", img)
        cv2.waitKey(2)

        if len(lmlist) == 0 :
            continue

        # state transtition #########################
        # Steps
        # 1. 先檢查有沒有選中不同的動作
        # 2. 檢查有沒有過兩秒
        right_index_x = lmlist[20][0]
        right_index_y = lmlist[20][1]

        # 移動選擇運動類型
        if right_index_x < 128:
            if right_index_y < 120:
                # 從其他運動改選 SQUAT
                if idx != GUIIndex.SQUAT_HOVER and idx != GUIIndex.SQUAT:
                    start_time = ctime
                    idx = GUIIndex.SQUAT_HOVER
                    continue
            elif right_index_y < 320:
                # 從其他動作改選 SIT_UP
                if idx != GUIIndex.SIT_UP_HOVER and idx != GUIIndex.SIT_UP:
                    start_time = ctime
                    idx = GUIIndex.SIT_UP_HOVER
                    continue
            elif right_index_y < 465:
                # 從其他動作改選 JUMP
                if idx != GUIIndex.JUMP_HOVER and idx != GUIIndex.JUMP:
                    start_time = ctime
                    idx = GUIIndex.JUMP_HOVER
                    continue
            elif right_index_y < 595:
                # 從其他動作改選 LIFT_FEET
                if idx != GUIIndex.LIFT_FEET_HOVER and idx != GUIIndex.LIFT_FEET:
                    start_time = ctime
                    idx = GUIIndex.LIFT_FEET_HOVER
                    continue
        else:
            # 沒有選中任何動作
            start_time = ctime
            idx = GUIIndex.DEFAULT
            continue

        # 檢查有沒有過2秒
        if pass_time >= 2:
            if idx == GUIIndex.SQUAT_HOVER:
                start_time = ctime
                idx = GUIIndex.SQUAT
            elif idx == GUIIndex.SQUAT:
                return ExerciseChoise.SQUAT

            elif idx == GUIIndex.SIT_UP_HOVER:
                start_time = ctime
                idx = GUIIndex.SIT_UP
            elif idx == GUIIndex.SIT_UP:
                return ExerciseChoise.SIT_UP

            elif idx == GUIIndex.JUMP_HOVER:
                start_time = ctime
                idx = GUIIndex.JUMP
            elif idx == GUIIndex.JUMP:
                return ExerciseChoise.JUMP
            
            elif idx == GUIIndex.LIFT_FEET_HOVER:
                start_time = ctime
                idx = GUIIndex.LIFT_FEET
            elif idx == GUIIndex.LIFT_FEET:
                return ExerciseChoise.LIFT_FEET
pass # select_exercise_with_cam


while True:
    choice = select_exercise_with_cam()
    print(choice)


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