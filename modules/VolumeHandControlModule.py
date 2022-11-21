import cv2
import time
import numpy as np
import math
import pycaw
from modules import HandTrackingModule as htm
from ctypes import  cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class VolumeHandControlModule():

    def __init__(self):
        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))

        self.volRange = self.volume.GetVolumeRange()

        self.minVol = self.volRange[0]
        self.maxVol = self.volRange[1]

        # pTime = 0

        # detector = htm.handDetector(detectionCon=0.7)
        self.vol = 0
        self.volBar = 400
        self.volPer = 0

    def control(self, img, lmList):
        if len(lmList) != 0:
            # print(lmList[4], lmList[8])

            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]

            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)

            cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

            length = math.hypot(x2 - x1, y2 - y1)

            # print(length)

            if length > 30 and length < 350:
                # Hand range 30 - 300
                # Volume Range -65 - 0
                self.vol = np.interp(length, [30, 350], [self.minVol, self.maxVol])
                maxValRange = length
                self.volBar = np.interp(length, [30, 350], [400, 150])
                self.volPer = np.interp(length, [30, 350], [0, 100])
                self.volume.SetMasterVolumeLevel(self.vol, None)

                # print(f'min {self.minVol}, max {self.maxVol} '
                #       f'volBar {self.volBar}, volPer {self.volPer}')

                if length < 50:
                    cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
                if length > 250:
                    cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)

        # active volume rect
        cv2.rectangle(img, (50, int(self.volBar)), (85, 400), (255, 133, 0), cv2.FILLED)
        cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
        cv2.putText(img, f'{int(self.volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

        # cTime = time.time()
        # fps = 1 / (cTime - pTime)
        # pTime = cTime

        # cv2.putText(img, f'FPS: {int(fps)}', (10, 35), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)

        cv2.waitKey(10)
        return img

        # cv2.imshow("Image", img)
