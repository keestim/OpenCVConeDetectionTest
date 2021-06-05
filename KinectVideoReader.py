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
    def getVideo(self): 
        frame = freenect.sync_get_video()[0]
        return frame
    
    #function to get depth image from kinect
    def getDepth(self):
        frame = freenect.sync_get_depth()[0]
        frame = frame.astype(np.uint8)
        return frame
