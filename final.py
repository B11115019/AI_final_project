import cv2
import time
import numpy as np
import excersice as ex
import party_popper
import end_menu
from exercise_enum import *
import gaming_sound

winWidth = 1280
winHeight = 720
# 使用 OpenCV 从摄像头捕捉视频
cap = cv2.VideoCapture(0)
cap.set(3, winWidth)
cap.set(4, winHeight)

excer = ex.pose()

# store file
UIlist = load_GUI_list()
END_GIF = party_popper.PartyPopper()
END_MENU = end_menu.EndMenu()

for i in range(len(UIlist)):
    UIlist[i] = cv2.resize(UIlist[i], (128, 720)) # width = 128, height = 720


def capture_and_detect_pose():
    """
    從相機讀入一幀，並做姿態檢測 + 繪製骨架
    ## Return:
    - img - 圖片
    - lmlist - 檢測到的骨架的節點
    """
    ret, img = cap.read()
    img = cv2.flip(img, 1)

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

    gaming_sound.MainMenu()
    while True:
        # 目前的時間
        ctime = time.time()
        # 經過的時間
        pass_time = int(ctime - start_time)

        img, lmlist = capture_and_detect_pose()

        # 顯示倒數秒數
        if idx != GUIIndex.DEFAULT:
            cv2.rectangle(img, (150, 0), (200, 50), (0, 0, 0), cv2.FILLED)
            cv2.putText(img, str(2 - pass_time), (165, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)


        # set up GUI
        img[0:720, 0:128] = UIlist[idx]

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
                    gaming_sound.PressButton()
                    continue
            elif right_index_y < 320:
                # 從其他動作改選 SIT_UP
                if idx != GUIIndex.SIT_UP_HOVER and idx != GUIIndex.SIT_UP:
                    start_time = ctime
                    idx = GUIIndex.SIT_UP_HOVER
                    gaming_sound.PressButton()
                    continue
            elif right_index_y < 465:
                # 從其他動作改選 JUMP
                if idx != GUIIndex.JUMP_HOVER and idx != GUIIndex.JUMP:
                    start_time = ctime
                    idx = GUIIndex.JUMP_HOVER
                    gaming_sound.PressButton()
                    continue
            elif right_index_y < 595:
                # 從其他動作改選 LIFT_FEET
                if idx != GUIIndex.LIFT_FEET_HOVER and idx != GUIIndex.LIFT_FEET:
                    start_time = ctime
                    idx = GUIIndex.LIFT_FEET_HOVER
                    gaming_sound.PressButton()
                    continue
        else:
            # 沒有選中任何動作
            start_time = ctime
            idx = GUIIndex.DEFAULT
            continue
        

        """
        討論要不要加
        """
        # cv2.rectangle(img, (300, 0), (800, 50), (0, 0, 0), cv2.FILLED)
        # cv2.putText(img, excercise_Type[idx], (350, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

        # 檢查有沒有過2秒
        if pass_time >= 2:
            if idx == GUIIndex.SQUAT_HOVER:
                gaming_sound.PressConfirm()
                start_time = ctime
                idx = GUIIndex.SQUAT
            elif idx == GUIIndex.SQUAT:
                return ExerciseChoise.SQUAT

            elif idx == GUIIndex.SIT_UP_HOVER:
                gaming_sound.PressConfirm()
                start_time = ctime
                idx = GUIIndex.SIT_UP
            elif idx == GUIIndex.SIT_UP:
                return ExerciseChoise.SIT_UP

            elif idx == GUIIndex.JUMP_HOVER:
                gaming_sound.PressConfirm()
                start_time = ctime
                idx = GUIIndex.JUMP
            elif idx == GUIIndex.JUMP:
                return ExerciseChoise.JUMP
            
            elif idx == GUIIndex.LIFT_FEET_HOVER:
                gaming_sound.PressConfirm()
                start_time = ctime
                idx = GUIIndex.LIFT_FEET
            elif idx == GUIIndex.LIFT_FEET:
                return ExerciseChoise.LIFT_FEET
pass # select_exercise_with_cam

def restart_or_not() -> bool:
    """
    進入選單來選擇要不要重新開始
    ## Return
    - restart - 若為true，代表要重新開始
    """
    start_time = time.time()
    # 0 -> 沒選中, 1 -> 選中 restart, 2 -> 選中 quit
    state = 0

    while True:
        pass_time = int(time.time() - start_time)
        img, lmlist = capture_and_detect_pose()

        hand_x = lmlist[20][0]
        hand_y = lmlist[20][1]

        # 顯示倒數秒數
        if state != 0:
            cv2.rectangle(img, (150, 0), (200, 50), (0, 0, 0), cv2.FILLED)
            cv2.putText(img, str(4 - pass_time), (165, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

        if state == 0:
            END_MENU.put_init_img(img)
        elif state == 1:
            END_MENU.put_restart_img(img)
        else:
            END_MENU.put_quit_img(img)

        cv2.imshow("Image", img)
        cv2.waitKey(2)

        #############################################
        # State Transition
        restart_timer = False
        if hand_x < 128:
            if hand_y < 360 and state != 1:
                state, restart_timer = 1, True
            elif hand_y > 360 and state != 2:
                state, restart_timer = 2, True
        else:
            state, restart_timer = 0, True

        if restart_timer:
            if state != 0: gaming_sound.PressButton()
            start_time = time.time()
            continue
            
        if pass_time >= 4: # 過4秒
            gaming_sound.PressConfirm()
            return state == 1
            
pass # restart_or_not

"""
全域變數
"""
record = [0, 0, 0, 0]
point = 0
border = -1000
"""
討論要不要加
"""
# excercise_Type = ["", "jumpingJacks", "", "LIFT_FEET", "", "SQUAT", "", "SIT_UP", ""]

# main
while True:
    """
    初始化
    """
    endGame = False
    end_Animation_counter = 0
    delta = 1000

    choice = select_exercise_with_cam()
    print(choice)
    
    # 分數紀錄
    record[choice] = max(record[choice], point)
    print(record[choice])

    # 變數
    point = 0
    idx = 0
    flag = True

    # 顯示倒數的字串
    countDown = ["", "Five", "Four", "Three", "Two", "One"]

    # 時間計數
    count_start_time = time.time()
    start_time = 0

    while True:
        try:
            ret, img = cap.read()
        except cv2.error as e:
            print("There was a problem with your camera")

        img = cv2.flip(img,1)

        # 将 BGR 轉為 RGB
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # 楚里圖像並獲得姿態
        result = excer.pose.process(rgb_img)

        # 檢測姿態並繪製
        img = excer.detect_pose(img, result)
        lmlist = excer.find_pose(img, result)

        ctime = time.time()

        if endGame == False:
            # 放置遊戲開始倒數畫面
            if idx <= 5:
                if idx == 0: gaming_sound.CountDown()

                cv2.putText(img, countDown[idx], (300, 460), cv2.FONT_HERSHEY_TRIPLEX, 10, (129, 240, 240), 3)
                if int(ctime - count_start_time) == idx:
                    idx += 1
                start_time = time.time()

                if idx == 6: gaming_sound.Gaming()
            else:
                if len(lmlist) != 0:
                    if choice == ExerciseChoise.SQUAT:
                        img, point, flag = excer.Squat(img, lmlist, point, flag)
                    elif choice == ExerciseChoise.JUMP:
                        img, point, flag = excer.jumpingJacks(img, lmlist, point, flag)
                    elif choice == ExerciseChoise.LIFT_FEET:
                        img, point, flag = excer.LiftFeet(img, lmlist, point, flag)
                    elif choice == ExerciseChoise.SIT_UP:
                        img, point, flag = excer.sit_up(img, lmlist, point, flag)

                # 放置文字
                cv2.putText(img, "time: " + str(60 - int(ctime - start_time)) + "sec", (30, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                cv2.putText(img, "point = " + str(point), (30,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                cv2.putText(img, f"Highest record = {record[choice]}", (900, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                
                if ctime - start_time > 10:
                    endGame = True
                    end_Animation_counter = time.time()
        #顯示結果畫面
        elif endGame == True:
            ctime = time.time()

            if int(ctime - end_Animation_counter) >= 0.01:
                end_Animation_counter = ctime
                delta -= 200
                
            END_GIF.next_frame()
            END_GIF.put_on_image(img)

            if point > record[choice]:
                cv2.putText(img, "Congratulation you break the record!!", (delta, 400), cv2.FONT_HERSHEY_TRIPLEX, 3, (39, 242, 198), 2)
                cv2.putText(img, f"Record becomes {point} points", (150, 600), cv2.FONT_HERSHEY_TRIPLEX, 2, (235, 19, 227), 2)
            else:
                cv2.putText(img, "You have to work harder!!", (delta, 400), cv2.FONT_HERSHEY_TRIPLEX, 3, (39, 242, 198), 2)
                cv2.putText(img, f"Highest record is {point} points", (150, 600), cv2.FONT_HERSHEY_TRIPLEX, 2, (235, 19, 227), 2)


        # 顯示結果img
        cv2.imshow("Image", img)
        cv2.waitKey(2)

        if delta <= border:
            break
    pass # while loop for 遊戲中和結算畫面

    if restart_or_not() == True:
        continue
    else:
        break
