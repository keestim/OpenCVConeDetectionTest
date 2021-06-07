import threading
from HueAdjustor import *
from SaturationAdjustor import *
from ValueAdjustor import *
from HSVValueContainer import * 
from time import sleep

class HSVController(threading.Thread):
    def __init__(self, video_feed):
        super().__init__()

        self.fHSV_value_container = HSVValueContainer()

        self.fvideo_feed = video_feed
        
        self.fshared_adjustor_condition_var  = threading.Condition()

        self.fHSV_processors = []

        self.fHSV_processors.append(HueAdjustor(video_feed, 
                                                self.fshared_adjustor_condition_var, 
                                                HSVAdjustorMode.Decreasing))

        self.fHSV_processors.append(SaturationAdjustor(video_feed, 
                                                self.fshared_adjustor_condition_var,
                                                HSVAdjustorMode.Decreasing))

        self.fHSV_processors.append(ValueAdjustor(video_feed, 
                                            self.fshared_adjustor_condition_var, 
                                            HSVAdjustorMode.Decreasing))

        self.fHSV_processors.append(HueAdjustor(video_feed, 
                                                self.fshared_adjustor_condition_var, 
                                                HSVAdjustorMode.Increasing))

        self.fHSV_frame = None
        self.fframe_threshold = None
        
    def filterActiveAdjustorThreads(self, adjustor_thread):
        return adjustor_thread.getFinishedProcessing()

    def run(self):
        for HSV_adjustor in self.fHSV_processors:
            HSV_adjustor.start()

        while (True):
            self.fshared_adjustor_condition_var.acquire()    

            if len(self.fHSV_processors) > 0:
                active_threads = list(filter(lambda x: not x.getFinishedProcessing(), self.fHSV_processors))

                if len(active_threads) == 0:
                    for adjustor_thread in self.fHSV_processors:
                        self.fHSV_value_container = adjustor_thread.setCalculatedThresholdValue(self.fHSV_value_container)
                        
                        adjustor_thread.resetValues()   

                    self.fshared_adjustor_condition_var.notify()      

            self.fshared_adjustor_condition_var.release()  

    def getHSVValueContainer(self):
        return self.fHSV_value_container