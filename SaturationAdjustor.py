from HSVAdjustor import *

class SaturationAdjustor(HSVAdjustor, threading.Thread):
    def __init__ (self, decreasingAdjustor = True):
        HSVAdjustor.__init__(self, decreasingAdjustor)
        threading.Thread.__init__(self)


    def updateValue (self, newValue):
        if decreasingAdjustor:
            self.fhigh_S = newValue
        else:
            self.flow_S = newValue

    