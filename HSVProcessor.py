import threading
from VideoSource import *
import cv2
import numpy as np

class HSVProcessor(threading.Thread):
    def __init__(self, video_thread):
        threading.Thread.__init__(self)
        self.fvideo_thread = video_thread
        self.fprocesed_frame = None
        self.fHSV_frame = None
        self.fframe_threshold = None

        self.fmax_value = 255
        self.fmax_value_H = 360//2

        self.flow_H = 0
        self.flow_S = 85
        self.flow_V = 123
        self.fhigh_H = 53
        self.fhigh_S = 189
        self.fhigh_V = 255
        
    def run(self):
        while True:
            self.fHSV_frame = cv2.cvtColor(self.fvideo_thread.RGB_frame, cv2.COLOR_BGR2HSV)
            self.fframe_threshold = cv2.inRange(self.fHSV_frame, (self.flow_H, self.flow_S, self.flow_V), (self.fhigh_H, self.fhigh_S, self.fhigh_V))
            self.fprocesed_frame = self.__processImg(self.fframe_threshold)

    def __processImg(self, input_frame):  
        #processing steps: https://imgur.com/a/9Muz1LN
        output_img = cv2.erode(input_frame, np.ones((3, 3), np.uint8))
        output_img = cv2.dilate(output_img, np.ones((7, 7), np.uint8), iterations=2)
        output_img = cv2.GaussianBlur(output_img, (15, 15), 0)
        
        return cv2.cvtColor(output_img, cv2.COLOR_GRAY2BGR)

    def get_video_thread(self):
        return self.fvideo_thread

    def get_procesed_frame(self):
        return self.fprocesed_frame 

    def get_HSV_frame(self):
        return self.fHSV_frame 

    def get_frame_threshold(self):
        return self.fframe_threshold

    def get_max_value(self):
        return self.fmax_value

    def get_max_value_H(self):
        return self.fmax_value_H

    def get_low_H(self):
        return self.flow_H 

    def get_low_S(self):
        return self.flow_S 

    def get_low_V(self):
        return self.flow_V 

    def get_high_H(self):
        return self.fhigh_H 

    def get_high_S(self):
        return self.fhigh_S 

    def get_high_V(self):
        return self.fhigh_V 
    
    def set_low_H(self, input_value):
        self.flow_H = input_value 

    def set_low_S(self, input_value):
        self.flow_S = input_value 

    def set_low_V(self, input_value):
        self.flow_V = input_value 

    def set_high_H(self, input_value):
        self.fhigh_H = input_value 

    def set_high_S(self, input_value):
        self.fhigh_S = input_value 

    def set_high_V(self, input_value):
        self.fhigh_V = input_value 