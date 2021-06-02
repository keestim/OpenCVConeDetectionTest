from abc import ABC, ABCMeta, abstractmethod
import threading
import cv2
from enum import IntEnum

#https://stackoverflow.com/questions/24487405/enum-getting-value-of-enum-on-string-conversion
class HSVType(IntEnum):
    Hue = 0
    Saturation = 1
    Value = 2

class HSVMetaClass(ABCMeta, type(threading.Thread)):
    pass

class HSVAdjustor(ABC, metaclass = HSVMetaClass):
    def __init__(self, video_feed, decreasing_adjustor = True):
        self.fdecreasing_adjustor = decreasing_adjustor
        self.ffinish_processing = False

        self.flow_H = 0
        self.flow_S = 0
        self.flow_V = 25
        self.fhigh_H = 51
        self.fhigh_S = 173
        self.fhigh_V = 255

        self.fmax_value = 255
        self.fmax_value_H = 180
        
        self.fprevious_values = []

        self.fthreshold_value = 0

        self.ftemp_min_HSV = []
        self.ftemp_max_HSV = []

        self.fvideo_feed = video_feed

        self.fincrement_value = 5

    def getThreshholdValue(self):
        return self.fthreshold_value

    def getfinishProcessing(self):
        return self.ffinish_processing

    def run(self):
        self.resetValues()

        while (True):
            if (not self.ffinish_processing):
                self.getMeanBrightness()
               
    def getMeanBrightness(self):
        mean_frame_value_arr = []
        
        while (True):
            self.fHSV_frame = cv2.cvtColor(self.fvideo_feed.getRGBFrame(), 
                                            cv2.COLOR_BGR2HSV)
            
            self.fframe_threshold = cv2.inRange(
                                        self.fHSV_frame, 
                                        (self.ftemp_min_HSV[HSVType.Hue], 
                                        self.ftemp_min_HSV[HSVType.Saturation], 
                                        self.ftemp_min_HSV[HSVType.Value]), 
                                        (self.ftemp_min_HSV[HSVType.Hue], 
                                        self.ftemp_min_HSV[HSVType.Saturation], 
                                        self.ftemp_min_HSV[HSVType.Value]))
            
            mean_value = cv2.mean(self.fframe_threshold)[0]
            mean_frame_value_arr.append(mean_value)
            
            self.decreaseTempThreshold()

            if (len(mean_frame_value_arr) > 3):
                step_diff = float(mean_frame_value_arr[len(mean_frame_value_arr) - 2]) - float(mean_value)
                
                if (step_diff) < 1:
                    self.updateValue()
                    self.ffinish_processing = True
                    
                    return

    def getDecreasingAdjustor(self):
        return self.fdecreasing_adjustor
        
    def getFinalHighHSVArray(self):
        return [self.fhigh_H, self.fhigh_S, self.fhigh_V]

    def getFinalLowHSVArray(self):
        return [self.flow_H, self.flow_S, self.flow_V]

    @abstractmethod
    def decreaseTempThreshold(self):
        pass

    @abstractmethod
    def updateValue(self):
        pass

    def resetValues(self):
        self.ffinish_processing = False
        self.fprevious_values = []
        self.ftemp_min_HSV = [0, 0, 0]
        self.ftemp_max_HSV = [self.fmax_value_H, self.fmax_value, self.fmax_value]