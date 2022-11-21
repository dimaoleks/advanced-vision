import cv2
from PIL import Image, ImageTk


class VideoAreaManager():
    def __init__(self,
                 label="",
                 xPos=0,
                 yPos=0,
                 weight=0,
                 height=0):
        self.label = label
        self.xPos = xPos
        self.yPos = yPos
        self.weight = weight
        self.height = height

    def videoAreaProcess(self, img, flip=False):
        img = cv2.resize(img, (self.weight, self.height))
        if flip:
            img = cv2.flip(img, 1)
        img = Image.fromarray(img)
        pic = ImageTk.PhotoImage(img)
        self.label.configure(image=pic)
        self.label.image = pic
        self.label.place(x=self.xPos, y=self.yPos)
