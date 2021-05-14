import threading
import cv2
from HueAdjustor import *
from SaturationAdjustor import *
from ValueAdjustor import *
from time import sleep

class HSVController(threading.Thread):
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
        self.fHSVprocessors = []

        self.fHSVprocessors.append(HueAdjustor(True))
        self.fHSVprocessors.append(SaturationAdjustor(True))

        self.fHSV_frame = None
        self.fframe_threshold = None


        
    def filterActiveAdjustorThreads(self, adjustorThread):
        return adjustorThread.getfinishProcessing()


    def run(self):
        '''
        while True:
            self.getMeanBrightness()
            sleep(1)
        '''
        for HSVAdjustor in self.fHSVprocessors:
            HSVAdjustor.start()

        while True:
            activeThreads = filter(self.fHSVprocessors,self.filterActiveAdjustorThreads)
            
            if len(activeThreads) == 0:
                for adjustorThread in self.fHSVprocessors:
                    if adjustorThread.getDecreasingAdjustor():
                        highHSVvalues = [self.fhigh_H,self.fhigh_S,self.fhigh_V]
                        highHSVvalues = updateValue(adjustorThread, highHSVvalues)
                        self.fhigh_H = highHSVvalues[0]
                        self.fhigh_S = highHSVvalues[1]
                        self.fhigh_V = highHSVvalues[2]
                    else:
                        lowHSVvalues = [self.flow_H,self.flow_S,self.flow_V]
                        lowHSVvalues = updateValue(adjustorThread, lowHSVvalues)
                        self.flow_H = lowHSVvalues[0]
                        self.flow_S = lowhHSVvalues[1]
                        self.flow_V = lowHSVvalues[2]

                    adjustorThread.resetValues()                        

    def assignHSVValue(self, HSVAdjustor, currentHSVValues):
        if type(HSVAdjustor) == HueAdjustor
            HSVIndex = 0
        else if type(HSVAdjustor) == SaturationAdjustor
            HSVIndex = 1
        else if type(HSVAdjustor) == ValueAdjustor
            HSVIndex = 2
        currentHSVValues[HSVIndex] = HSVAdjustor.getThreshholdValue()

    
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