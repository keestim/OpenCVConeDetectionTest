from HSVAdjustor import *

class SaturationAdjustor(HSVAdjustor, threading.Thread):
    def __init__ (self, decreasingAdjustor = True):
        HSVAdjustor.__init__(self, decreasingAdjustor)
        threading.Thread.__init__(self)
        self.fmax_value = 180

    def updateValue (self, newValue):
        if decreasingAdjustor:
            self.fhigh_H = newValue
        else:
            self.flow_H = newValue