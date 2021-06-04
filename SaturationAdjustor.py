from HSVAdjustor import *

class SaturationAdjustor(HSVAdjustor, threading.Thread):
    def __init__ (self, video_feed, adjustor_condition_var, decreasing_adjustor = HSVAdjustorMode.Decreasing):
        HSVAdjustor.__init__(self, 
                            video_feed,
                            adjustor_condition_var,
                            decreasing_adjustor)
        
        threading.Thread.__init__(self)

    def decreaseSpecifiedThresholdValue(self):
        if self.isAdjustorDecreasing:
            self.fHSV_container.high_S -= self.fincrement_value
        else:
            self.fHSV_container.low_S += self.fincrement_value

    def setCalculatedThresholdValue(self, HSVThresholdValues):
        if self.isAdjustorDecreasing:
            HSVThresholdValues.high_S = self.fHSV_container.high_S
        else:
            HSVThresholdValues.low_S = self.fHSV_container.low_S
            
        return HSVThresholdValues