from VideoSource import *
from abc import ABC, abstractmethod

import threading
import cv2
import sys
import numpy as np

from time import sleep

class ExternalImageReader(VideoSource, threading.Thread):
    def __init__(self, fileSrc):
        super(VideoSource, self).__init__()
        threading.Thread.__init__(self)

        self.ffile_src = fileSrc
        self.RGB_frame = self.get_video()
        self.depth_frame = self.get_depth()

        
    def run(self):
        while True:
            self.RGB_frame = self.get_video()
            self.depth_frame = self.get_depth()

    def get_file_src(self):
        return self.ffile_src

    #function to get RGB image from kinect
    def get_video(self): 
        #array = cv2.imread(self.ffile_src)
        #array = cv2.cvtColor(array,cv2.COLOR_BGR2HSV)

        img = cv2.imread(self.ffile_src)

        return img
        
    
    #function to get depth image from kinect
    def get_depth(self):
        #array,_ = freenect.sync_get_depth()
        #array = array.astype(np.uint8)
        sleep(1)
        return None
        