from VideoSource import *
from abc import ABC, abstractmethod

import threading
import cv2
import sys
import numpy as np

class ExternalImageReader(VideoSource, threading.Thread):
    def __init__(self, fileSrc):
        VideoSource.__init__(self)
        threading.Thread.__init__(self)
        self.ffileSrc = fileSrc
        
    def run(self):
        while True:
            self.RGB_frame = self.get_video()
            self.depth_frame = self.get_depth()

    #function to get RGB image from kinect
    def get_video(self): 
        #array,_ = freenect.sync_get_video()
        #array = cv2.cvtColor(array,cv2.COLOR_BGR2HSV)

        array = cv2.imread(self.ffileSrc)
        
        return array
    
    #function to get depth image from kinect
    def get_depth(self):
        #array,_ = freenect.sync_get_depth()
        #array = array.astype(np.uint8)
        return None

'''class ImageInput()
    def __init__(self)
        input_img = input("Enter image name: ")
        print ("importing image " + input_img)



        return 
'''