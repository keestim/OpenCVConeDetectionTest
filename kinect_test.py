#theory from: 
#https://raw.githubusercontent.com/MicrocontrollersAndMore/Traffic_Cone_Detection_Visual_Basic/master/presentation/Steps%20With%20Images.pdf

#look at this:
#https://stackoverflow.com/questions/54288980/controlling-opencv-convex-hull
#https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_contours/py_contours_more_functions/py_contours_more_functions.html
#https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html

#import the necessary modules
from KinectVideoReader import *
from ConeDetector import *
import cv2
import numpy as np
import time
from time import sleep
from enum import Enum 
import threading

#https://docs.opencv.org/3.4/da/d97/tutorial_threshold_inRange.html
#UI Stuff
max_value = 255
max_value_H = 360//2

low_H = 0
low_S = 85
low_V = 123
high_H = 53
high_S = 189
high_V = 255

class ImageViewer(Enum):
    HSVThresholdBW = 1
    ProcessedThreshold = 2
    ShapesOnly = 3


class HSVProcessor(threading.Thread):
    def __init__(self, kinectVideoThread):
        threading.Thread.__init__(self)
        self.kinectVideoObj = kinectVideoThread
        self.procesed_frame = None
        self.HSV_frame = None
        self.frame_threshold = None
        
    def run(self):
        while True:
            try:
                self.HSV_frame = cv2.cvtColor(self.kinectVideoObj.RGB_frame, cv2.COLOR_BGR2HSV)
                self.frame_threshold = cv2.inRange(self.HSV_frame, (low_H, low_S, low_V), (high_H, high_S, high_V))
                self.procesed_frame = self.processImg(self.frame_threshold)
            except:
                print("HSVProcessor Error")

    def processImg(self, input_frame):  
        #processing steps: https://imgur.com/a/9Muz1LN

        output_img = cv2.erode(input_frame, np.ones((3, 3), np.uint8))
        output_img = cv2.dilate(output_img, np.ones((7, 7), np.uint8), iterations=2)
        output_img = cv2.GaussianBlur(output_img, (15, 15), 0)
        
        return cv2.cvtColor(output_img, cv2.COLOR_GRAY2BGR)

#UI Stuff
window_capture_name = 'Video Capture'
window_detection_name = 'Object Detection'
window_processedimg_name = 'Processed Capture'
window_depth_name = 'Depth Capture'
low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'

def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H-1, low_H)
    cv2.setTrackbarPos(low_H_name, window_detection_name, low_H)

def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H+1)
    cv2.setTrackbarPos(high_H_name, window_detection_name, high_H)

def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S-1, low_S)
    cv2.setTrackbarPos(low_S_name, window_detection_name, low_S)

def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S+1)
    cv2.setTrackbarPos(high_S_name, window_detection_name, high_S)

def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V-1, low_V)
    cv2.setTrackbarPos(low_V_name, window_detection_name, low_V)

def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V+1)
    cv2.setTrackbarPos(high_V_name, window_detection_name, high_V)
    
if __name__ == "__main__":
    cv2.namedWindow(window_capture_name)
    cv2.namedWindow(window_detection_name)
    cv2.namedWindow(window_processedimg_name)

    cv2.createTrackbar(low_H_name, window_detection_name, low_H, max_value_H, on_low_H_thresh_trackbar)
    cv2.createTrackbar(high_H_name, window_detection_name, high_H, max_value_H, on_high_H_thresh_trackbar)
    cv2.createTrackbar(low_S_name, window_detection_name, low_S, max_value, on_low_S_thresh_trackbar)
    cv2.createTrackbar(high_S_name, window_detection_name, high_S, max_value, on_high_S_thresh_trackbar)
    cv2.createTrackbar(low_V_name, window_detection_name, low_V, max_value, on_low_V_thresh_trackbar)
    cv2.createTrackbar(high_V_name, window_detection_name, high_V, max_value, on_high_V_thresh_trackbar)

    kinectVideoThread = KinectVideoReader()
    kinectVideoThread.start()

    sleep(0.5)

    HSVProcessorThread = HSVProcessor(kinectVideoThread)
    HSVProcessorThread.start()

    sleep(0.5)

    ConeDetectorThread = ConeDetector(HSVProcessorThread)
    ConeDetectorThread.start()

    sleep(0.5)

    while True:     
        cv2.imshow(window_capture_name, kinectVideoThread.RGB_frame)        

        cv2.imshow(window_detection_name, HSVProcessorThread.frame_threshold)

        cv2.imshow(window_processedimg_name, ConeDetectorThread.DectedConeFrame)
        cv2.imshow(window_depth_name, kinectVideoThread.depth_frame)     

        k = cv2.waitKey(5) & 0xFF

        if k == 27:
            break
    cv2.destroyAllWindows()
