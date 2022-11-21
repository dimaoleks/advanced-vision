from pydub import AudioSegment
from pydub.playback import play
from playsound import playsound
import threading
import multiprocessing


class MusicManager():
    def __init__(self):
        # self.path = ""
        self.isPlaying = False

    # def playMusic(self, musicPath):
    #     # self.path = musicPath
    #     playsound(musicPath, False)
    #     self.isPlaying = True
    #
    # def playMusicAsync(self, musicPath):
    #     # self.path = musicPath
    #     t = threading.Thread(
    #         target=playsound,
    #         args=(musicPath,),
    #         daemon=True)
    #     t.start()
    #     self.isPlaying = True
    #     return t

    def playMusicAsync(self, musicPath):
        # self.path = musicPath
        p = multiprocessing.Process(
            target=playsound,
            args=(musicPath,),
            daemon=True)
        p.start()
        self.isPlaying = True
        return p

    def disableMusic(self):
        self.isPlaying = False

# "../../materials/music/1.mp3"
