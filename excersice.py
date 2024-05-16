import mediapipe as mp
import numpy
import cv2
import numpy.typing

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

        if leftelbow < leftshoulder and rightelbow < rightshoulder and leftHand - rightHand < 20:
            if flag == False:
                point += 1
                flag = True
        elif leftelbow > leftshoulder and rightelbow > rightshoulder and leftHand - rightHand > 20:
            flag = False
        return img, point, flag
    
    def sit_up(self, img, lmlist, point, flag):
        # right
        RShoulder = numpy.array(lmlist[12][0:2])
        RHip = numpy.array(lmlist[24][0:2])
        RKnee = numpy.array(lmlist[26][0:2])

        # left
        LShoulder = numpy.array(lmlist[11][0:2])
        LHip = numpy.array(lmlist[23][0:2])
        LKnee = numpy.array(lmlist[25][0:2])

        def included_angle(v1: numpy.typing.ArrayLike, v2: numpy.typing.ArrayLike) -> float:
            """
            計算兩個向量v1和v2的夾角，回傳的是角度制
            """
            radian = (v1 @ v2) / numpy.linalg.norm(v1) / numpy.linalg.norm(v2)
            return radian * 180 / numpy.pi
        
        if included_angle(RShoulder - RHip, RKnee - RHip) < 90 or included_angle(LShoulder - LHip, LKnee - LHip) < 90:
            if flag == False:
                point += 1
                flag = True
        else:
            flag = False

        return img, point, flag