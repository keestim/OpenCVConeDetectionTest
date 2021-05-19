from HSVAdjustor import *

class SaturationAdjustor(HSVAdjustor, threading.Thread):
    def __init__ (self, video_feed, getDecreasingAdjustor = True):
        HSVAdjustor.__init__(self, video_feed, getDecreasingAdjustor)
        threading.Thread.__init__(self)


    def updateValue(self):
        if self.getDecreasingAdjustor:
            self.fmax_value = self.fTempMaxHSV[1]
        else:
            self.flow_H = self.fTempMinHSV[1]
    
    def decreaseTempThreshold(self):
        if self.getDecreasingAdjustor:
            self.fTempMaxHSV[1] -= 5
        else:
            self.fTempMinHSV[1] += 5