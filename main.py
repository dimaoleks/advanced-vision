import cv2
import time
from modules import HandTrackingModule as htm
from modules.utils import HandRecognizer as hr
from modules.managers.music import MusicManager as mm
from modules import VolumeHandControlModule as vhcm
from modules.utils import ChooseExecutor as ce


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS, 30)

    detector = htm.handDetector()
    handR = hr.HandRecognizer()
    music = mm.MusicManager()
    volume = vhcm.VolumeHandControlModule()
    choose = ce.ChooseExecutor()

    # /////////////////////////////////////
    isExecuting = False
    volumeControlEnabled = False
    musicT = None
    state = hr.Command.Unknown
    allCommands = [hr.Command.Unknown,
                   hr.Command.Music,
                   hr.Command.Volume]
    commandCounter = 0
    currentCommand = allCommands[commandCounter]
    # /////////////////////////////////////

    frameCounter = 0
    handType = None
    while cap.isOpened():
        success, img = cap.read()
        img = detector.findHands(img, draw=True)
        lmList = detector.findPosition(img, draw=True)
        if frameCounter == 0 or handType == None:
            handType = detector.recognizeHand(img)
        state = handR.recognizeCommand(lmList)

        # print(frameCounter)
        #
        # print(handType)

        frameCounter = frameCounter + 1
        if frameCounter == 50 or len(lmList) < 15:
            frameCounter = 0

        if handType == 'Right':
            if state == hr.Decision.ChangeCommand:
                if len(allCommands) == commandCounter:
                    commandCounter = 0
                    currentCommand = allCommands[commandCounter]
                else:
                    currentCommand = allCommands[commandCounter]
                    commandCounter = commandCounter + 1

            if state == hr.Decision.Yes:
                if currentCommand == hr.Command.Music:
                    if isExecuting == False:
                        isExecuting = True
                        musicT = music.playMusicAsync("D:/Projects/advanced-vision/materials/music/1.mp3")

            if currentCommand == hr.Command.Volume:
                volumeControlEnabled = True
                # img = volume.control(img, lmList)

            if state == hr.Decision.No:
                if currentCommand == hr.Command.Music:
                    if isExecuting == True:
                        if musicT != None:
                            musicT.terminate()
                            musicT = None
                            isExecuting = False

            if currentCommand != hr.Command.Volume:
                volumeControlEnabled = False

            if volumeControlEnabled == True:
                img = volume.control(img, lmList)
        # print(f'Volume Control Enabled: {volumeControlEnabled}')

        # if isExecuting == False:
        #    isExecuting = choose.execute(currentCommand, state, music.playMusicProcessAsync("D:/Projects/advanced-vision/materials/music/1.mp3"))

        # if state == hr.Command.MusicStart:
        #     if musicIsPlaying == False:
        #         musicIsPlaying = True
        #         musicT = music.playMusicProcessAsync("D:/Projects/advanced-vision/materials/music/1.mp3")
        # if state == hr.Command.MusicStop:
        #     if musicIsPlaying == True:
        #         musicIsPlaying = False
        #         if musicT == None:
        #             continue
        #         if musicT != None:
        #             musicT.terminate()
        #             musicT = None

        # if state == hr.Command.VolumeIncrease:
        #     volumeControlEnabled = True
        #     if volumeControlEnabled == True:
        #         img = volume.control(img, lmList)
        #         volumeControlEnabled = False
        #     else:
        #         volumeControlEnabled = False

        # print(state)
        # print(f'{currentCommand}    {state}')

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.putText(img, str(currentCommand).split('.')[1], (590, 680), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(10)

    cap.release()

if __name__ == "__main__":
    main()
