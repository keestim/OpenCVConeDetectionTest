from VideoSource import *
from abc import ABC, abstractmethod

import freenect
import threading
import cv2
import numpy as np

class KinectVideoReader(VideoSource, threading.Thread):
    def __init__(self, frame_thread_Lock):
        VideoSource.__init__(self, frame_thread_Lock)
        threading.Thread.__init__(self)
        
    #function to get RGB image from kinect
    def get_video(self): 
        array,_ = freenect.sync_get_video()
        array = cv2.cvtColor(array,cv2.COLOR_BGR2HSV)
        return array
    
    #function to get depth image from kinect
    def getDepth(self):
        array = freenect.sync_get_depth()[0]
        array = array.astype(np.uint8)
        return array
