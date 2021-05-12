import threading
import cv2
from time import sleep

class HSVAdjustor(threading.Thread):
    def __init__(self, video_feed):
        super().__init__()
        self.flow_H = 0
        self.flow_S = 0
        self.flow_V = 25
        self.fhigh_H = 51
        self.fhigh_S = 173
        self.fhigh_V = 255
        self.fvideo_feed = video_feed
        self.fHSV_frame = None
        self.fframe_threshold = None
    def run(self):
        while True:
            self.getMeanBrightness()
            sleep(1)

    def getMeanBrightness(self):
        self.fHSV_frame = cv2.cvtColor(self.fvideo_feed.get_RGB_frame(), cv2.COLOR_BGR2HSV)
        self.fframe_threshold = cv2.inRange(self.fHSV_frame, (self.flow_H, self.flow_S, self.flow_V), (self.fhigh_H, self.fhigh_S, self.fhigh_V))
        print(cv2.mean(self.fframe_threshold))

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