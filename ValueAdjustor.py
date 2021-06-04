from HSVAdjustor import *

class ValueAdjustor(HSVAdjustor, threading.Thread):
    def __init__ (self, video_feed, adjustor_condition_var, decreasing_adjustor = HSVAdjustorMode.Decreasing):
        HSVAdjustor.__init__(self, 
                            video_feed, 
                            adjustor_condition_var,
                            decreasing_adjustor)
        
        threading.Thread.__init__(self)
       
    def decreaseSpecifiedThresholdValue(self):
        if self.isAdjustorDecreasing:
            self.fHSV_container.high_V -= self.fincrement_value
        else:
            self.fHSV_container.low_V += self.fincrement_value

    def setCalculatedThresholdValue(self, HSVThresholdValues):
        if self.isAdjustorDecreasing:
            HSVThresholdValues.high_V = self.fHSV_container.high_V
        else:
            HSVThresholdValues.low_V = self.fHSV_container.low_V
            
        return HSVThresholdValues