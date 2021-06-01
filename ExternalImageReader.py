from VideoSource import *

import threading
import cv2

class ExternalImageReader(VideoSource, threading.Thread):
    def __init__(self, frame_thread_Lock, file_src):
        self.ffile_src = file_src

        VideoSource.__init__(self, frame_thread_Lock)
        threading.Thread.__init__(self)

        self.fRGB_frame = self.getVideo()
        self.fdepth_frame = self.getDepth()
   
    def getFileSrc(self):
        return self.ffile_src

    #function to get RGB image from external image
    def getVideo(self):
        img = cv2.imread(self.ffile_src)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

        return img
        
    #function to get depth image from external image
    def getDepth(self):
        return None
        
