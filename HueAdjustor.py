from HSVAdjustor import *

class HueAdjustor(HSVAdjustor, threading.Thread):
    def __init__ (self, video_feed, decreasing_adjustor = True):
        HSVAdjustor.__init__(self, 
                            video_feed, 
                            decreasing_adjustor)
        
        threading.Thread.__init__(self)
        self.fmax_value = 180

    def updateValue(self):
        if self.getDecreasingAdjustor:
            self.fmax_value = self.ftemp_max_HSV[HSVType.Hue]
        else:
            self.flow_H = self.ftemp_min_HSV[HSVType.Hue]
    
    def decreaseTempThreshold(self):
        if self.getDecreasingAdjustor:
            self.ftemp_max_HSV[HSVType.Hue] -= self.fincrement_value
        else:
            self.ftemp_min_HSV[HSVType.Hue] += self.fincrement_value