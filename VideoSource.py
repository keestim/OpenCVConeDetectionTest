from abc import ABC, ABCMeta, abstractmethod
import threading
from time import sleep

#see: https://docs.python.org/3/library/abc.html
#https://stackoverflow.com/questions/28799089/python-abc-multiple-inheritance
#https://stackoverflow.com/questions/9575409/calling-parent-class-init-with-multiple-inheritance-whats-the-right-way

class VideoMetaClass(ABCMeta, type(threading.Thread)):
    pass

class VideoSource(ABC, metaclass = VideoMetaClass):
    def __init__(self, frame_thread_Lock):
        threading.Thread.__init__(self)
        self.fRGB_frame = self.get_video()
        self.fdepth_frame = self.get_depth()
        self.fframe_thread_Lock = frame_thread_Lock

    def run(self):
        while True:
            try:
                self.fframe_thread_Lock.acquire()
            finally:
                self.fRGB_frame = self.get_video()
                self.fdepth_frame = self.get_depth()

                self.fframe_thread_Lock.release()
                sleep(0.01)

    @abstractmethod
    #function to get RGB image
    def get_video(self):
        pass
    
    @abstractmethod
    #function to get depth image 
    def get_depth(self):
        pass

    def get_RGB_frame(self):
        return self.fRGB_frame

    def get_depth_frame(self):
        return self.fdepth_frame