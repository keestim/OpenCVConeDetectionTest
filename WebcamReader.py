from VideoSource import *

import threading
import cv2

class WebcamReader(VideoSource, threading.Thread):
    def __init__(self):
        super(VideoSource, self).__init__()
        threading.Thread.__init__(self)

        self.fvideo_capture = cv2.VideoCapture("/dev/video0")
        self.fRGB_frame = self.getVideo()
        self.fdepth_frame = self.getDepth()

    #function to get RGB image from kinect
    def getVideo(self): 
        success, frame = self.fvideo_capture.read()

        if success:
            return frame
        
    #function to get depth image from kinect
    def getDepth(self):
        return None
        
