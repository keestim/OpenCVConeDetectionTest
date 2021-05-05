from abc import ABC, ABCMeta, abstractmethod
import threading

#see: https://docs.python.org/3/library/abc.html
#https://stackoverflow.com/questions/28799089/python-abc-multiple-inheritance
#https://stackoverflow.com/questions/9575409/calling-parent-class-init-with-multiple-inheritance-whats-the-right-way

class VideoMetaClass(ABCMeta, type(threading.Thread)):
    pass

class VideoSource(ABC, metaclass = VideoMetaClass):
    def __init__(self):
        threading.Thread.__init__(self)
        self.RGB_frame = self.get_video()
        self.depth_frame = self.get_depth()

    def run(self):
        while True:
            self.RGB_frame = self.get_video()
            self.depth_frame = self.get_depth()

    @abstractmethod
    #function to get RGB image
    def get_video(self):
        pass
    
    @abstractmethod
    #function to get depth image 
    def get_depth(self):
        pass