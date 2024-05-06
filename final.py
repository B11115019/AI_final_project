import cv2
import time
import excersice as ex

# 使用 OpenCV 从摄像头捕捉视频
cap = cv2.VideoCapture(0)
cap.set(3, 800)
cap.set(4, 800)

excer = ex.pose()
record = 0

# store file
mylist = []
mylist.append(cv2.imread("data/data/default.png"))
mylist.append(cv2.imread("data/data/jump_hover.png"))
mylist.append(cv2.imread("data/data/jump.png"))
mylist.append(cv2.imread("data/data/push_up_hover.png"))
mylist.append(cv2.imread("data/data/push_up.png"))
mylist.append(cv2.imread("data/data/sit_up_hover.png"))
mylist.append(cv2.imread("data/data/sit_up.png"))
mylist.append(cv2.imread("data/data/squat_hover.png"))
mylist.append(cv2.imread("data/data/squat.png"))

while True:
    while True:
        ret, img = cap.read()
        img[0:100, 0:700] = mylist[0]
        
        cv2.imshow(img)
        cv2.waitKey(2)
    # excercise_option = ["jumpingJacks", "LiftFeet", "Squat"]

    # for idx, name in enumerate(excercise_option):
    #     print(f"{idx+1}: {name}")

    # choice = int(input("請輸入想要做的運動: "))

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