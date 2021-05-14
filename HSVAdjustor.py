from abc import ABC, ABCMeta, abstractmethod
import threading
from time import sleep

class HSVMetaClass(ABCMeta, type(threading.Thread)):
    pass

class HSVAdjustor(ABC, metaclass = HSVMetaClass):
    def __init__(self, decreasingAdjustor = True):
        self.fdecreasingAdjustor = decreasingAdjustor
        self.ffinishProcessing = False

        self.flow_H = 0
        self.flow_S = 0
        self.flow_V = 25
        self.fhigh_H = 51
        self.fhigh_S = 173
        self.fhigh_V = 255

        self.fmax_value = 255
        
        self.fpreviousValues = []

        self.fThreshholdValue = 0

    def getThreshholdValue(self):
        return self.fThreshholdValue

    def getfinishProcessing(self):
        return self.ffinishProcessing

    def run(self)
        while (True):
            if (not self.ffinishProcessing):
                self.getMeanBrightness()
                sleep(1)
               
    def getMeanBrightness(self):
        #convert to array
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
                    self.updateValue(initial_fhigh_H)
                    return


    def getDecreasingAdjustor(self):
        return self.fdecreasingAdjustor

    #decrease temp threshold
    #decrease appropiate threshold value, by pre-set increment
    #takes in array, modifies array, outputs array

    @abstractmethod
    def decreaseTempThreshold(self,)
    @abstractmethod
    def updateValue(self, newValue):
        pass

    def resetValues(self):
        self.ffinishProcessing = False
        self.fpreviousValues = []


            

        