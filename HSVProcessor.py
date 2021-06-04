import threading
from VideoSource import *
import cv2
import numpy as np
from time import sleep

class HSVProcessor(threading.Thread):
    def __init__(self, HSV_adjustor, video_thread, frame_thread_Lock):
        threading.Thread.__init__(self)
        self.fvideo_thread = video_thread
        self.fprocesed_frame = None
        self.fHSV_frame = None
        self.fframe_threshold = None
        self.fHSV_adjustor_thread = HSV_adjustor
        self.fframe_thread_Lock = frame_thread_Lock

        self.fmax_value = 255
        self.fmax_value_H = 360//2

        self.fdilation_amt = 5
        self.fdilation_itterations = 2

        self.ferode_amt = 2

        self.fblur_amt = 15
        
    def run(self):
        while True:
            try:
                self.fframe_thread_Lock.acquire()
            finally:
                self.fHSV_frame = cv2.cvtColor(self.fvideo_thread.getRGBFrame(), 
                                                cv2.COLOR_BGR2HSV)
                
                self.fframe_threshold = cv2.inRange(
                                            self.fHSV_frame, 
                                            (self.fHSV_adjustor_thread.getHSVValueContainer().low_H, 
                                            self.fHSV_adjustor_thread.getHSVValueContainer().low_S, 
                                            self.fHSV_adjustor_thread.getHSVValueContainer().low_V), 
                                            (self.fHSV_adjustor_thread.getHSVValueContainer().high_H, 
                                            self.fHSV_adjustor_thread.getHSVValueContainer().high_S, 
                                            self.fHSV_adjustor_thread.getHSVValueContainer().high_V))
                
                self.fprocesed_frame = self.__processImg(self.fframe_threshold)

                self.fframe_thread_Lock.release()
                sleep(0.01)

    def __processImg(self, input_frame):  
        #processing steps: https://imgur.com/a/9Muz1LN
        output_img = cv2.erode(input_frame, 
                                np.ones((self.ferode_amt, self.ferode_amt), np.uint8))


        output_img = cv2.dilate(output_img, 
                                np.ones((self.fdilation_amt, self.fdilation_amt), np.uint8), 
                                iterations = 2)
        
        output_img = cv2.GaussianBlur(output_img, (self.fblur_amt, self.fblur_amt), 0)
        
        return cv2.cvtColor(output_img, cv2.COLOR_GRAY2BGR)

    def getVideoThread(self):
        return self.fvideo_thread

    def getProcesedFrame(self):
        return self.fprocesed_frame 

    def getHSVFrame(self):
        return self.fHSV_frame 

    def getFrameThreshold(self):
        return self.fframe_threshold

    def getMaxValue(self):
        return self.fmax_value

    def getMaxValueH(self):
        return self.fmax_value_H