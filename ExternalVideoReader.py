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
        self.RGB_frame = self.get_video()
        self.depth_frame = self.get_depth()

    def run(self):
        while True:
            self.RGB_frame = self.get_video()
            self.depth_frame = self.get_depth()

    #function to get RGB image from kinect
    def get_video(self):

        ret, frame = self.cap.read()
        # if frame is read correctly ret is True

        print("gg man")
        frame = cv2.cvtColor(frame,cv2.COLOR_RGB2HSV)
        return frame
        
    
    #function to get depth image from kinect
    def get_depth(self):
        #array,_ = freenect.sync_get_depth()
        #array = array.astype(np.uint8)
        sleep(1)
        return None
        