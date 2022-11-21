from enum import Enum


class HandRecognizer():

    def recognizeCommand(self, lmList):
        if len(lmList) != 0 and len(lmList) == 21:

            if lmList[8][2] - 30 > lmList[5][2]:
                return Decision.Yes
            if lmList[4][1] < lmList[12][1]:
                return Decision.No
            if lmList[16][2] > lmList[14][2]:
                return Decision.ChangeCommand

        return Decision.Unknown


class Command(Enum):
    Unknown = 0,
    Music = 1,
    Volume = 2


class Decision(Enum):
    Unknown = 0,
    No = 1,
    Yes = 2,
    ChangeCommand = 3
