from HSVAdjustor import *

class ValueAdjustor(HSVAdjustor, threading.Thread):
    def __init__ (self, video_feed, decreasing_adjustor = True):
        HSVAdjustor.__init__(self, 
                            video_feed, 
                            decreasing_adjustor)
        
        threading.Thread.__init__(self)
   
    def updateValue(self):
        if self.getDecreasingAdjustor:
            self.fmax_value = self.ftemp_max_HSV[HSVType.Value]
        else:
            self.flow_H = self.ftemp_min_HSV[HSVType.Value]
    
    def decreaseTempThreshold(self):
        if self.getDecreasingAdjustor:
            self.ftemp_max_HSV[HSVType.Value] -= self.fincrement_value
        else:
            self.ftemp_min_HSV[HSVType.Value] += self.fincrement_value