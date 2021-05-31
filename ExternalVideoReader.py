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

        self.fframe_counter = 0
        self.cap = cv2.VideoCapture(vid_path)

        self.ftotal_frames = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)

        self.fRGB_frame = self.getVideo()
        self.fdepth_frame = self.getDepth()
        
    def run(self):
        #https://stackoverflow.com/questions/59102833/python-opencv-cv2-videocapture-read-getting-stuck-indefinitely-after-running-t
        while self.cap.isOpened():
            self.fRGB_frame = self.getVideo()
            self.fdepth_frame = self.getDepth()

    #function to get RGB image from external video file
    #https://www.programcreek.com/python/example/85663/cv2.VideoCapture
    def getVideo(self):
        success, frame = self.cap.read()

        #returns frame too fast!

        if success:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
            self.fframe_counter += 1

            return frame
        else:
            print("Can't receive frame (stream end?). Exiting ...")   

            if (self.fframe_counter >= (self.ftotal_frames - 1)):
                print("Attempting to reset video")
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.fframe_counter = 0
                
                return self.fRGB_frame
    
    #function to get depth image from external video file
    def getDepth(self):
        #array,_ = freenect.sync_get_depth()
        #array = array.astype(np.uint8)
        return None
        