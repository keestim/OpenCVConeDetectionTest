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

        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        self.RGB_frame = self.get_video()
        self.depth_frame = self.get_depth()

    def run(self):
        while True:
            self.RGB_frame = self.get_video()
            self.depth_frame = self.get_depth()

    #function to get RGB image from kinect
    def get_video(self): 
        frame = self.cap.read()[1]
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        return frame
        
    
    #function to get depth image from kinect
    def get_depth(self):
        #array,_ = freenect.sync_get_depth()
        #array = array.astype(np.uint8)
        sleep(1)
        return None
        