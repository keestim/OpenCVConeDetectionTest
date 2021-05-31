from VideoSource import *
from abc import ABC, abstractmethod

import threading
import cv2
import sys
import numpy as np

from time import sleep

class WebcamReader(VideoSource, threading.Thread):
    def __init__(self):
        super(VideoSource, self).__init__()
        threading.Thread.__init__(self)

        self.fvideo_capture = cv2.VideoCapture("/dev/video0")
        self.fRGB_frame = self.getVideo()
        self.fdepth_frame = self.getDepth()

    def run(self):
        while True:
            self.fRGB_frame = self.getVideo()
            self.fdepth_frame = self.getDepth()

    #function to get RGB image from kinect
    def getVideo(self): 
        success, frame = self.fvideo_capture.read()

        if success:
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            return frame
        
    #function to get depth image from kinect
    def getDepth(self):
        return None
        
