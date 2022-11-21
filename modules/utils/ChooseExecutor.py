from modules.utils import HandRecognizer as hr


class ChooseExecutor():

    def __init__(self):
        self.state = hr.Command.Unknown
        self.isExecuting = False

    def execute(self, stateCommand, stateChoose, task):
        if stateCommand == hr.Command.Unknown:
            return self.isExecuting

        if stateChoose == hr.Decision.Yes:
            if stateCommand == hr.Command.MusicStart:
                if self.isExecuting == False:
                    task.start()
                    self.isExecuting = True
        if stateChoose == hr.Decision.No:
            if stateCommand == hr.Command.MusicStop:
                if task != None:
                    task.terminate()
                    self.isExecuting = False

        return self.isExecuting