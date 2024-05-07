import enum
import cv2

class GUIIndex(enum.IntEnum):
    """
    定義GUI要顯示的圖片的index
    """
    DEFAULT = 0
    JUMP_HOVER = 1
    JUMP = 2
    LIFT_FEET_HOVER = 3
    LIFT_FEET = 4
    SIT_UP_HOVER = 5
    SIT_UP = 6
    SQUAT_HOVER = 7
    SQUAT = 8

def load_GUI_list() -> list:
    """
    載入GUI會用到的圖片，list中的index可以參照GUIIndex
    """
    mylist = []
    mylist.append(cv2.imread("data/data/default.jpg")) # 0
    mylist.append(cv2.imread("data/data/jump_hover.jpg")) # 1
    mylist.append(cv2.imread("data/data/jump.jpg")) # 2
    mylist.append(cv2.imread("data/data/LiftFeet_hover.jpg")) # 3
    mylist.append(cv2.imread("data/data/LiftFeet.jpg")) # 4
    mylist.append(cv2.imread("data/data/sit_up_hover.jpg")) # 5
    mylist.append(cv2.imread("data/data/sit_up.jpg")) # 6
    mylist.append(cv2.imread("data/data/squat_hover.jpg")) # 7
    mylist.append(cv2.imread("data/data/squat.jpg")) # 8
    return mylist

class ExerciseChoise(enum.IntEnum):
    """
    定義可以選擇的運動
    """
    JUMP = 1
    LIFT_FEET = 2
    SQUAT = 3
    SIT_UP = 4
