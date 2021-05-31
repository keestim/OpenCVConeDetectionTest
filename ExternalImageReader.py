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
        self.fRGB_frame = self.getVideo()
        self.fdepth_frame = self.getDepth()
   
    def run(self):
        while True:
            self.fRGB_frame = self.getVideo()
            self.fdepth_frame = self.getDepth()

    def get_file_src(self):
        return self.ffile_src

    #function to get RGB image from kinect
    def getVideo(self):
        img = cv2.imread(self.ffile_src)
        img = cv2.cvtColor(img,cv2.COLOR_RGB2HSV)

        return img
        
    #function to get depth image from kinect
    def getDepth(self):
        sleep(1)
        return None
        
