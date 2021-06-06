from HSVAdjustor import *

class HueAdjustor(HSVAdjustor, threading.Thread):
    def __init__ (self, video_feed, adjustor_condition_var, decreasing_adjustor = HSVAdjustorMode.Decreasing):
        HSVAdjustor.__init__(self, 
                            video_feed, 
                            adjustor_condition_var,
                            decreasing_adjustor)
        
        threading.Thread.__init__(self)
        self.fmax_value = MAX_HUE_VALUE

        self.fadjustor_name = "Hue " + self.getAdjustorDirectionText()
    
    def decreaseSpecifiedThresholdValue(self):
        if self.isAdjustorDecreasing():
            self.fHSV_container.high_H -= self.fincrement_value
        else:
            self.fHSV_container.low_H += self.fincrement_value

    def getSpecifiedThresholdValue(self):
        return self.fHSV_container.high_H if (self.isAdjustorDecreasing()) else self.fHSV_container.low_H

    def setCalculatedThresholdValue(self, HSVThresholdValues):
        if self.isAdjustorDecreasing():
            HSVThresholdValues.high_H = self.fHSV_container.high_H
        else:
            HSVThresholdValues.low_H = self.fHSV_container.low_H

        return HSVThresholdValues