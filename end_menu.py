import cv2

class EndMenu:
    def __init__(self):
        self.init_img = cv2.imread("data/end_menu/init.png")
        self.restart_img = cv2.imread("data/end_menu/restart.png")
        self.quit_img = cv2.imread("data/end_menu/quit.png")

    def put_init_img(self, img : cv2.Mat):
        img[0:720, 0:128] = self.init_img

    def put_restart_img(self, img : cv2.Mat):
        img[0:720, 0:128] = self.restart_img

    def put_quit_img(self, img : cv2.Mat):
        img[0:720, 0:128] = self.quit_img
        