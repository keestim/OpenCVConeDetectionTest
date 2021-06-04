import threading
from HueAdjustor import *
from SaturationAdjustor import *
from ValueAdjustor import *

class HSVController(threading.Thread):
    def __init__(self, video_feed):
        super().__init__()

        #TODO Remove these default values!
        self.flow_H = 0
        self.flow_S = 0
        self.flow_V = 25
        self.fhigh_H = 51
        self.fhigh_S = 173
        self.fhigh_V = 255

        self.fmax_value = 255
        self.fmax_value_H = 360//2

        self.fvideo_feed = video_feed
        self.fHSV_processors = []

        self.fshared_adjustor_condition_var  = threading.Condition()

        self.fHSV_processors.append(HueAdjustor(video_feed, self.fshared_adjustor_condition_var, False))
        self.fHSV_processors.append(HueAdjustor(video_feed, self.fshared_adjustor_condition_var, True))

        self.fHSV_processors.append(SaturationAdjustor(video_feed, self.fshared_adjustor_condition_var, False))
        self.fHSV_processors.append(SaturationAdjustor(video_feed, True))

        self.fHSV_processors.append(ValueAdjustor(video_feed, self.fshared_adjustor_condition_var, True))
        self.fHSV_processors.append(ValueAdjustor(video_feed, self.fshared_adjustor_condition_var, False))

        self.fHSV_frame = None
        self.fframe_threshold = None
        
    def filterActiveAdjustorThreads(self, adjustor_thread):
        return adjustor_thread.getfinishProcessing()

    def run(self):
        for HSV_adjustor in self.fHSV_processors:
            HSV_adjustor.start()

        while (True):
            self.fshared_adjustor_condition_var.acquire()    

            if len(self.fHSV_processors) > 0:

                active_threads = list(filter(lambda x: not x.getfinishProcessing(), self.fHSV_processors))

                if len(active_threads) == 0:
                    for adjustor_thread in self.fHSV_processors:
                        if adjustor_thread.getDecreasingAdjustor():
                            high_HSV_values = [self.fhigh_H, self.fhigh_S, self.fhigh_V]

                            high_HSV_values = adjustor_thread.getFinalHighHSVArray()
                            self.fhigh_H = high_HSV_values[HSVType.Hue]
                            self.fhigh_S = high_HSV_values[HSVType.Saturation]
                            self.fhigh_V = high_HSV_values[HSVType.Value]
                        else:
                            low_HSV_values = [self.flow_H, self.flow_S, self.flow_V]

                            low_HSV_values = adjustor_thread.getFinalLowHSVArray()
                            self.flow_H = low_HSV_values[HSVType.Hue]
                            self.flow_S = low_HSV_values[HSVType.Saturation]
                            self.flow_V = low_HSV_values[HSVType.Value]

                        adjustor_thread.resetValues()   

                    print("waking threads!")
                    self.fshared_adjustor_condition_var.notifyAll()      

            self.fshared_adjustor_condition_var.release()  

    def assignHSVValue(self, HSV_adjustor, current_HSV_values):
        if type(HSV_adjustor) == HueAdjustor:
            HSV_index = HSVType.Hue
        elif type(HSV_adjustor) == SaturationAdjustor:
            HSV_index = HSVType.Saturation
        elif type(HSV_adjustor) == ValueAdjustor:
            HSV_index = HSVType.Value
        
        current_HSV_values[HSV_index] = HSV_adjustor.getThreshholdValue()

    def getLowH(self):
        return self.flow_H 

    def getLowS(self):
        return self.flow_S 

    def getLowV(self):
        return self.flow_V 

    def getHighH(self):
        return self.fhigh_H 

    def getHighS(self):
        return self.fhigh_S 

    def getHighV(self):
        return self.fhigh_V 
    
    def setLowH(self, input_value):
        self.flow_H = input_value 

    def setLowS(self, input_value):
        self.flow_S = input_value 

    def setLowV(self, input_value):
        self.flow_V = input_value 

    def setHighH(self, input_value):
        self.fhigh_H = input_value 

    def setHighS(self, input_value):
        self.fhigh_S = input_value 

    def setHighV(self, input_value):
        self.fhigh_V = input_value 
          
    def getMaxValue(self):
        return self.fmax_value

    def getMaxValueH(self):
        return self.fmax_value_H