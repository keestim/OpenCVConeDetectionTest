from VideoSource import *
from abc import ABC, abstractmethod

import threading
import cv2
import sys
import numpy as np

from time import sleep

class ExternalVideoReader(VideoSource, threading.Thread):
    def __init__(self, vid_path):
        super(VideoSource, self).__init__()
        threading.Thread.__init__(self)

        self.cap = cv2.VideoCapture(vid_path)
        self.fRGB_frame = self.getVideo()
        self.fdepth_frame = self.getDepth()

    def run(self):
        while True:
            self.fRGB_frame = self.getVideo()
            self.fdepth_frame = self.getDepth()

    #function to get RGB image from kinect
    def getVideo(self):
        ret, frame = self.cap.read()
        # if frame is read correctly ret is True

        print("gg man")
        frame = cv2.cvtColor(frame,cv2.COLOR_RGB2HSV)
        return frame
        
    
    #function to get depth image from kinect
    def getDepth(self):
        #array,_ = freenect.sync_get_depth()
        #array = array.astype(np.uint8)
        sleep(1)
        return None
        