from abc import ABC, ABCMeta, abstractmethod
import threading
from time import sleep
import cv2

class HSVMetaClass(ABCMeta, type(threading.Thread)):
    pass

class HSVAdjustor(ABC, metaclass = HSVMetaClass):
    def __init__(self, video_feed, decreasingAdjustor = True):
        self.fdecreasingAdjustor = decreasingAdjustor
        self.ffinishProcessing = False

        self.flow_H = 0
        self.flow_S = 0
        self.flow_V = 25
        self.fhigh_H = 51
        self.fhigh_S = 173
        self.fhigh_V = 255

        self.fmax_value = 255
        self.fmax_value_H = 180
        
        self.fpreviousValues = []

        self.fThreshholdValue = 0

        self.fTempMinHSV = []
        self.fTempMaxHSV = []

        self.fvideo_feed = video_feed

    def getThreshholdValue(self):
        return self.fThreshholdValue

    def getfinishProcessing(self):
        return self.ffinishProcessing

    def run(self):
        self.resetValues()

        while (True):
            if (not self.ffinishProcessing):
                self.getMeanBrightness()
               
    def getMeanBrightness(self):
        meanFrameValueArr = []
        change_step = 5
        while (True):
            self.fHSV_frame = cv2.cvtColor(self.fvideo_feed.get_RGB_frame(), cv2.COLOR_BGR2HSV)


            self.fframe_threshold = cv2.inRange(
                                    self.fHSV_frame, 
                                    (self.fTempMinHSV[0], self.fTempMinHSV[1], self.fTempMinHSV[2]), 
                                    (self.fTempMaxHSV[0], self.fTempMaxHSV[1], self.fTempMaxHSV[2]))
            meanVal = cv2.mean(self.fframe_threshold)[0]
            meanFrameValueArr.append(meanVal)
            
            self.decreaseTempThreshold()

            if (len(meanFrameValueArr) > 3):
                step_diff = float(meanFrameValueArr[len(meanFrameValueArr) - 2]) - float(meanVal)
                
                if (step_diff) < 1:
                    self.updateValue()
                    self.ffinishProcessing = True
                    
                    return

    def getDecreasingAdjustor(self):
        return self.fdecreasingAdjustor
        
    def getFinalHighHSVArray(self):
        return [self.fhigh_H, self.fhigh_S, self.fhigh_V]

    def getFinalLowHSVArray(self):
        return [self.flow_H, self.flow_S, self.flow_V]
    #decrease temp threshold
    #decrease appropiate threshold value, by pre-set increment
    #takes in array, modifies array, outputs array

    @abstractmethod
    #adjust array!
    def decreaseTempThreshold(self):
        pass

    @abstractmethod
    def updateValue(self):
        pass

    def resetValues(self):
        self.ffinishProcessing = False
        self.fpreviousValues = []
        self.fTempMinHSV = [0, 0, 0]
        self.fTempMaxHSV = [self.fmax_value_H, self.fmax_value, self.fmax_value]

        


            

        