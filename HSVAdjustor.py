from HSVValueContainer import * 
from abc import ABC, ABCMeta, abstractmethod
import threading
import cv2
from enum import Enum, IntEnum

#https://stackoverflow.com/questions/24487405/enum-getting-value-of-enum-on-string-conversion
class HSVType(IntEnum):
    Hue = 0
    Saturation = 1
    Value = 2

class HSVAdjustorMode(Enum):
    Increasing = 0
    Decreasing = 1

class HSVMetaClass(ABCMeta, type(threading.Thread)):
    pass

##TODO change decreasing_adjustor from boolean to a custom enum!
class HSVAdjustor(ABC, metaclass = HSVMetaClass):
    def __init__(self, 
                video_feed, 
                adjustor_condition_var, 
                decreasing_adjustor = HSVAdjustorMode.Decreasing):

        self.fdecreasing_adjustor = decreasing_adjustor
        self.ffinish_processing = False

        self.fadjustor_condition_var = adjustor_condition_var        
        self.fHSV_container = HSVValueContainer()
        
        self.fprevious_values = []

        self.fthreshold_value = 0

        self.fvideo_feed = video_feed

        self.fmax_value = MAX_VALUE

        self.fincrement_value = 5

        self.fadjustor_name = ""

    def getAdjustorDirectionText(self):
        return "decreasing" if self.fdecreasing_adjustor == HSVAdjustorMode.Decreasing else "increasing"

    def getThreshholdValue(self):
        return self.fthreshold_value

    def getFinishedProcessing(self):
        return self.ffinish_processing

    def run(self):
        self.resetValues()

        while (True):
            if (not self.ffinish_processing):
                self.findTargetHSVValue()
   
    def findTargetHSVValue(self):
        mean_frame_value_arr = []
        
        while (not self.ffinish_processing):
            self.fHSV_frame = cv2.cvtColor(self.fvideo_feed.getRGBFrame(), 
                                            cv2.COLOR_BGR2HSV)

            self.fframe_threshold = cv2.inRange(self.fHSV_frame, 
                                                (self.fHSV_container.low_H,
                                                self.fHSV_container.low_S,
                                                self.fHSV_container.low_V),
                                                (self.fHSV_container.high_H,
                                                self.fHSV_container.high_S,
                                                self.fHSV_container.high_V))
            
            mean_value = cv2.mean(self.fframe_threshold)[0]
            mean_frame_value_arr.append(mean_value)
            
            self.decreaseSpecifiedThresholdValue()

            # TODO Improve this array code here
            # TODO No "magic" numbers!
            if (len(mean_frame_value_arr) > 3):
                step_diff = float(mean_frame_value_arr[len(mean_frame_value_arr) - 2]) - float(mean_value)
                
                # Fix this!!!
                #print(self.fadjustor_name + " | step_diff: " + str(step_diff))

                if float(step_diff) < 1:         
                    with self.fadjustor_condition_var:
                        #TODO Fix performance!
                        self.ffinish_processing = True
                        self.fadjustor_condition_var.wait()
                        
                    return

    def isAdjustorDecreasing(self):
        return self.fdecreasing_adjustor == HSVAdjustorMode.Decreasing

    def resetValues(self):
        self.ffinish_processing = False
        self.fprevious_values = []
        self.fHSV_container.reset()

    @abstractmethod
    def decreaseSpecifiedThresholdValue(self):
        pass

    @abstractmethod
    def setCalculatedThresholdValue(self, HSVThresholdValues):
        pass