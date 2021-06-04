from HSVAdjustor import *

class SaturationAdjustor(HSVAdjustor, threading.Thread):
    def __init__ (self, video_feed, adjustor_condition_var, decreasing_adjustor = True):
        HSVAdjustor.__init__(self, 
                            video_feed,
                            adjustor_condition_var,
                            decreasing_adjustor)
        
        threading.Thread.__init__(self)

    def updateValue(self):
        if self.getDecreasingAdjustor:
            self.fmax_value = self.ftemp_max_HSV[HSVType.Saturation]
        else:
            self.flow_H = self.ftemp_min_HSV[HSVType.Saturation]
    
    def decreaseTempThreshold(self):
        if self.getDecreasingAdjustor:
            self.ftemp_max_HSV[HSVType.Saturation] -= self.fincrement_value
        else:
            self.ftemp_min_HSV[HSVType.Saturation] += self.fincrement_value