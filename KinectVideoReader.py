import freenect
import threading
import cv2
import numpy as np

class KinectVideoReader(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.RGB_frame = self.get_video()
        self.depth_frame = self.get_depth()

    def run(self):
        while True:
            self.RGB_frame = self.get_video()
            self.depth_frame = self.get_depth()

    #function to get RGB image from kinect
    def get_video(self):
        array,_ = freenect.sync_get_video()
        array = cv2.cvtColor(array,cv2.COLOR_BGR2HSV)
        return array
    
    #function to get depth image from kinect
    def get_depth(self):
        array,_ = freenect.sync_get_depth()
        array = array.astype(np.uint8)
        return array
