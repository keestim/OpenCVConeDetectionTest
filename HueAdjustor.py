from HSVAdjustor import *

class HueAdjustor(HSVAdjustor, threading.Thread):
    def __init__ (self, video_feed, getDecreasingAdjustor = True):
        HSVAdjustor.__init__(self, video_feed, getDecreasingAdjustor)
        threading.Thread.__init__(self)
        self.fmax_value = 180

    def updateValue(self):
        if self.getDecreasingAdjustor:
            self.fmax_value = self.fTempMaxHSV[0]
        else:
            self.flow_H = self.fTempMinHSV[0]
    
    def decreaseTempThreshold(self):

        if self.getDecreasingAdjustor:
            self.fTempMaxHSV[0] -= 5
        else:
            self.fTempMinHSV[0] += 5


    