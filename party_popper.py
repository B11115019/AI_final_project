import cv2

class PartyPopper:
    def __init__(self):
        self.current_frame : int
        self.current_frame = 0

        self.imgs = []
        for i in range(1, 9):
            self.imgs.append(cv2.imread(f"data/party_popper/{i:03d}.png"))

    def next_frame(self):
        if self.current_frame == len(self.imgs) - 1:
            self.current_frame = 0
        else:
            self.current_frame += 1

    def put_on_image(self, img : cv2.Mat):
        img[320:720, 0:400] = self.imgs[self.current_frame]
        
        """
        for row in range(400):
            for col in range(400):
                color = self.imgs[self.current_frame][row][col]

                if any(color < [250, 250, 250]):
                    img[320 + row][col] = color
        """