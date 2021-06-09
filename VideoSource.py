from abc import ABC, ABCMeta, abstractmethod
import threading
from time import sleep
import cv2

#see: https://docs.python.org/3/library/abc.html
#https://stackoverflow.com/questions/28799089/python-abc-multiple-inheritance
#https://stackoverflow.com/questions/9575409/calling-parent-class-init-with-multiple-inheritance-whats-the-right-way

class VideoMetaClass(ABCMeta, type(threading.Thread)):
    pass

class VideoSource(ABC, metaclass = VideoMetaClass):
    def __init__(self, frame_thread_lock):
        threading.Thread.__init__(self)
        self.fRGB_frame = self.getVideo()
        
        self.fHSV_frame = ~cv2.cvtColor(self.fRGB_frame, cv2.COLOR_RGB2HSV)

        self.fdepth_frame = self.getDepth()
        self.fframe_thread_Lock = frame_thread_lock

    def run(self):
        while True:
            try:
                self.fframe_thread_Lock.acquire()
            finally:
                self.fRGB_frame = self.getVideo()
                
                self.fHSV_frame = ~cv2.cvtColor(self.fRGB_frame, cv2.COLOR_RGB2HSV) 

                self.fdepth_frame = self.getDepth()

                self.fframe_thread_Lock.release()
                sleep(0.01)

    def getFrameMetaData(self):
        data_array = self.fRGB_frame.shape

        return {"height": data_array[0], 
                "width": data_array[1], 
                "channels": data_array[2]}

    @abstractmethod
    #function to get RGB image
    def getVideo(self):
        pass
    
    @abstractmethod
    #function to get depth image 
    def getDepth(self):
        pass

    def getRGBFrame(self):
        return self.fRGB_frame

    def getDepthFrame(self):
        return self.fdepth_frame

    def getHSVFrame(self):
        return self.fHSV_frame