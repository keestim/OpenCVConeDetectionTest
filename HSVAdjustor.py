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

class HSVAdjustor(ABC, metaclass = HSVMetaClass):
    __BENCHMARK_STEP_VALUE = 5

    def __init__(self, 
                video_feed, 
                adjustor_condition_var, 
                decreasing_adjustor = HSVAdjustorMode.Decreasing):

        self.fdecreasing_adjustor = decreasing_adjustor
        self.ffinish_processing = False

        self.fadjustor_condition_var = adjustor_condition_var        
        self.fHSV_container = HSVValueContainer()
        
        self.fthreshold_value = 0

        self.fvideo_feed = video_feed

        self.fmax_value = MAX_VALUE

        self.fincrement_value = self.__BENCHMARK_STEP_VALUE

        self.finitial_frame_mean = 0

        self.fadjustor_name = ""

    def getAdjustorDirectionText(self):
        return ("de" if (self.fdecreasing_adjustor == HSVAdjustorMode.Decreasing) else "in") + "creasing"

    def getThreshholdValue(self):
        return self.fthreshold_value

    def getFinishedProcessing(self):
        return self.ffinish_processing

    def run(self):
        self.resetValues()

        while (True):
            if (not self.ffinish_processing):
                self.findTargetHSVValue()
    
    def findNewStepAmt(self, frame_adjustment_value_arr):
        # gets the step amount to adjust in a logarithmic way, account the previously recorded rate of change
        # scale formula was decided such that:
        #   output can never be less than 1 (impossible to have a divide by 0 error)
        #       y intercept is (0, 1)
        #   y values of function plateau towards 11
        #   f(20) = 5
        #       data has shown that 

        prev_change = float(frame_adjustment_value_arr[-2]["frame_mean"] - frame_adjustment_value_arr[-1]["frame_mean"])
        return int(round(10 * ((-1/((prev_change / 30) + 1)) + 1) + 1)) 

    def findTargetHSVValue(self):
        frame_adjustment_value_arr = []
        
        while (not self.ffinish_processing):
            self.fHSV_frame = self.fvideo_feed.getHSVFrame()

            self.fframe_threshold = cv2.inRange(self.fHSV_frame, 
                                                (self.fHSV_container.low_H,
                                                self.fHSV_container.low_S,
                                                self.fHSV_container.low_V),
                                                (self.fHSV_container.high_H,
                                                self.fHSV_container.high_S,
                                                self.fHSV_container.high_V))
            
            mean_value = cv2.mean(self.fframe_threshold)[0]

            # Need atleast 2 elements in array to calculate relative step value
            if len(frame_adjustment_value_arr) >= 2:
                self.fincrement_value = self.findNewStepAmt(frame_adjustment_value_arr)    
            elif len(frame_adjustment_value_arr) == 0:
                self.finitial_frame_mean = mean_value 

            frame_adjustment_value_arr.append({"frame_mean" : mean_value, 
                                                "step_amt" : self.fincrement_value, 
                                                "target_value" : self.getSpecifiedThresholdValue()})

            self.decreaseSpecifiedThresholdValue()

            # Need atleast 3 data points, to get atleast 2 difference values 
            if (len(frame_adjustment_value_arr) >= 3):
                
                last_mean_difference = float(frame_adjustment_value_arr[-2]["frame_mean"] - frame_adjustment_value_arr[-1]["frame_mean"])
                #make the mean value proportional to the base of 5 (when was utilized previously)
                #I (tim) found it to be a good benchmark for evaluating rate of change
                
                try:
                    proportional_step_amt = round(self.__BENCHMARK_STEP_VALUE / (self.__BENCHMARK_STEP_VALUE / frame_adjustment_value_arr[-1]["step_amt"]))
                except:
                    print("Error: " + str(frame_adjustment_value_arr))

                last_relative_mean = last_mean_difference / proportional_step_amt

                # guarantee that some meaningful adjustment is made, but ensuring that the last record mean is less than or equal to 97% of the initial value 
                if (float(last_relative_mean) < 1) and (frame_adjustment_value_arr[-1]["frame_mean"] <= (self.finitial_frame_mean * 0.97)):
                #if (float(last_relative_mean) < 1):         

                    with self.fadjustor_condition_var:
                        self.ffinish_processing = True

                        self.fadjustor_condition_var.wait()
                    return

    def isAdjustorDecreasing(self):
        return (self.fdecreasing_adjustor == HSVAdjustorMode.Decreasing)

    def resetValues(self):
        self.ffinish_processing = False
        self.fincrement_value = self.__BENCHMARK_STEP_VALUE
        self.finitial_frame_mean = 0
        self.fHSV_container.reset()

    @abstractmethod
    def decreaseSpecifiedThresholdValue(self):
        pass

    @abstractmethod
    def getSpecifiedThresholdValue(self):
        pass

    @abstractmethod
    def setCalculatedThresholdValue(self, HSVThresholdValues):
        pass