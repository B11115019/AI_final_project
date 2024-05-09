import mediapipe as mp
import cv2

class pose():
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(static_image_mode=False, 
                    model_complexity=1, 
                    enable_segmentation=False, 
                    min_detection_confidence=0.5)
        
    def detect_pose(self, img, result):
    # 检查是否检测到姿态
        if result.pose_landmarks:
            # 绘制关键点和骨架
            self.mp_drawing.draw_landmarks(img, result.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

        return img

    def find_pose(self, img, result):
        lmlist = list()
        if result.pose_landmarks:   
            for id, lm in enumerate(result.pose_landmarks.landmark):
                # print("1")
                h, w, c = img.shape 
                cx, cy = int(w * lm.x), int(h * lm.y)
                lmlist.append([cx, cy])

        return lmlist

    def Squat(self, img, lmlist, point, flag):
        pos1 = lmlist[11][1]
        pos2 = lmlist[25][1]

        if abs(pos1 - pos2) < 200:
            if(flag == False):
                point += 1
                flag = True
        else:
            flag = False

        return img, point, flag

    def LiftFeet(self, img, lmlist, point, flag):
        leftHip = lmlist[23][1]
        leftKnee = lmlist[25][1]
        rightHip = lmlist[24][1]
        rightKnee = lmlist[26][1]

        # if 
        if rightHip - rightKnee > 10 or leftHip - leftKnee > 10:
            if(flag == False):
                point += 1
                flag = True
        else:
            flag = False

        return img, point, flag

    def jumpingJacks(self, img, lmlist, point, flag):
        leftHand = lmlist[19][0]
        rightHand = lmlist[20][0]
        leftelbow = lmlist[13][1]
        rightelbow = lmlist[14][1]
        leftshoulder = lmlist[11][1]
        rightshoulder = lmlist[12][1]

        if leftelbow < leftshoulder and rightelbow < rightshoulder and leftHand - rightHand < 15:
            if(flag == False):
                point += 1
                flag = True
        else:
            flag = False

        return img, point, flag