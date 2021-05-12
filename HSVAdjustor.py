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

        self.fmax_value = 255
        self.fmax_value_H = 360//2

        self.fvideo_feed = video_feed
        self.fHSV_frame = None
        self.fframe_threshold = None

        

    def run(self):
        while True:
            self.getMeanBrightness()
            sleep(1)

    def getMeanBrightness(self):

        initial_low_H = 0
        initial_low_S = 0
        initial_low_V = 0
        initial_fhigh_H = self.fmax_value_H
        initial_fhigh_S = self.fmax_value
        initial_fhigh_V = self.fmax_value

        meanFrameValueArr = []
        change_step = 5
        while (True):
            self.fHSV_frame = cv2.cvtColor(self.fvideo_feed.get_RGB_frame(), cv2.COLOR_BGR2HSV)
            self.fframe_threshold = cv2.inRange(
                                    self.fHSV_frame, 
                                    (initial_low_H, initial_low_S, initial_low_V), 
                                    (initial_fhigh_H, initial_fhigh_S, initial_fhigh_V))
            meanVal = cv2.mean(self.fframe_threshold)[0]
            meanFrameValueArr.append(meanVal)
            initial_fhigh_H = initial_fhigh_H - change_step
            
            if (len(meanFrameValueArr) > 3):
                print(meanFrameValueArr[len(meanFrameValueArr) - 2])
                step_diff = float(meanFrameValueArr[len(meanFrameValueArr) - 2]) - float(meanVal)
                
                if (step_diff) < 1:
                    self.fhigh_H = initial_fhigh_H
                    return

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
          
    def get_max_value(self):
        return self.fmax_value

    def get_max_value_H(self):
        return self.fmax_value_H