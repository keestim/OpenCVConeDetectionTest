import threading
from VideoSource import *
import cv2
import numpy as np
from time import sleep

class HSVProcessor(threading.Thread):
    def __init__(self, HSVAdjustor, video_thread, frame_thread_Lock):
        threading.Thread.__init__(self)
        self.fvideo_thread = video_thread
        self.fprocesed_frame = None
        self.fHSV_frame = None
        self.fframe_threshold = None
        self.fHSV_adjustor_thread = HSVAdjustor
        self.fframe_thread_Lock = frame_thread_Lock
        
    def run(self):
        while True:
            try:
                self.fframe_thread_Lock.acquire()
            finally:
                #try:
                self.fHSV_frame = cv2.cvtColor(self.fvideo_thread.get_RGB_frame(), cv2.COLOR_BGR2HSV)
                self.fframe_threshold = cv2.inRange(
                                            self.fHSV_frame, 
                                            (self.fHSV_adjustor_thread.get_low_H(), 
                                            self.fHSV_adjustor_thread.get_low_S(), 
                                            self.fHSV_adjustor_thread.get_low_V()), 
                                            (self.fHSV_adjustor_thread.get_high_H(), 
                                            self.fHSV_adjustor_thread.get_high_S(), 
                                            self.fHSV_adjustor_thread.get_high_V()))
                                            
                self.fprocesed_frame = self.__processImg(self.fframe_threshold)
                #except:
                #    print("HSVProcessor Error")

                self.fframe_thread_Lock.release()
                sleep(0.01)

    def __processImg(self, input_frame):  
        #processing steps: https://imgur.com/a/9Muz1LN
        output_img = cv2.erode(input_frame, np.ones((3, 3), np.uint8))
        output_img = cv2.dilate(output_img, np.ones((7, 7), np.uint8), iterations=2)
        output_img = cv2.GaussianBlur(output_img, (15, 15), 0)
        
        return cv2.cvtColor(output_img, cv2.COLOR_GRAY2BGR)

    def get_video_thread(self):
        return self.fvideo_thread

    def get_procesed_frame(self):
        return self.fprocesed_frame 

    def get_HSV_frame(self):
        return self.fHSV_frame 

    def get_frame_threshold(self):
        return self.fframe_threshold

  
