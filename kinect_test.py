#theory from: 
#https://raw.githubusercontent.com/MicrocontrollersAndMore/Traffic_Cone_Detection_Visual_Basic/master/presentation/Steps%20With%20Images.pdf

#look at this:
#https://stackoverflow.com/questions/54288980/controlling-opencv-convex-hull
#https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_contours/py_contours_more_functions/py_contours_more_functions.html
#https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html

#import the necessary modules
import freenect
import cv2
import numpy as np
import time
from time import sleep
import random as rng
import math
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

class KinectVideoReader(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.RGB_frame = self.get_video()
        self.depth_frame = self.get_depth()

    def run(self):
        while True:
            self.RGB_frame = self.get_video()
            self.depth_frame = self.get_depth()

    #function to get RGB image from kinect
    def get_video(self):
        array,_ = freenect.sync_get_video()
        array = cv2.cvtColor(array,cv2.COLOR_BGR2HSV)
        return array
    
    #function to get depth image from kinect
    def get_depth(self):
        array,_ = freenect.sync_get_depth()
        array = array.astype(np.uint8)
        return array

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

class ConeDetector(threading.Thread):
    def __init__(self, HSVProcessor):
        threading.Thread.__init__(self)
        self.HSVProcessorObj = HSVProcessor
        self.DectedConeFrame = None

    def run(self):
        while True:
            self.DectedConeFrame = self.renderValidConvexHulls(self.HSVProcessorObj.procesed_frame)

    def getConvexHulls(self, contours):
        #https://docs.opencv.org/3.4/d7/d1d/tutorial_hull.html
        hull_list = []
        for i in range(len(contours)):
            hull = cv2.convexHull(contours[i])
            hull_list.append(hull)

        return hull_list

    #https://stackoverflow.com/questions/6471023/how-to-calculate-convex-hull-area-using-opencv-functions
    def ConvexHullArea(self, hull):
        area = 0
        for i in  range(len(hull) - 1):
            next_i = (i+1)%(len(hull))
            dX   = hull[next_i][0][0] - hull[i][0][0]
            avgY = (hull[next_i][0][1] + hull[i][0][1])/2
            area += dX * avgY;  # this is the integration step.

        return area

    def processHullData(self, hull):
        #transform the openCV generated array, to make it easier to interface with
        output_vectors = []

        for selected_hull in hull:
            vector_arr = []

            vector_arr.append(selected_hull[0][0])
            vector_arr.append(selected_hull[0][1])

            output_vectors.append(vector_arr)

        return output_vectors

    def getExtremePoints(self, hull):
        left_most = tuple(hull[hull[:,:,0].argmin()][0])
        right_most = tuple(hull[hull[:,:,0].argmax()][0])
        top_most = tuple(hull[hull[:,:,1].argmin()][0])
        bottom_most = tuple(hull[hull[:,:,1].argmax()][0])

        return {'left': left_most, 'right': right_most, 'top': top_most, 'bottom': bottom_most}

    def renderValidConvexHulls(self, ProcessedFrame):
        #https://towardsdatascience.com/edges-and-contours-basics-with-opencv-66d3263fd6d1

        #get edges and then contours from the processed frame
        edge = cv2.Canny(ProcessedFrame, 30, 200)
        contours, h = cv2.findContours(edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        processed_contours = []

        #select contours that are greater than 100
        #this removes any irrelevant data
        for contour in contours:
            if cv2.contourArea(contour) >= 100:
                processed_contours.append(contour) 

        valid_hulls = []

        for c in processed_contours:
            hull = cv2.convexHull(c)

            #A valid hull must have between 3 and 10 edges
            if ((len(hull) >= 3 or len(hull) <= 10) and 
                (self.ConvexHullArea(hull) > minimum_hull_size or 
                (self.ConvexHullArea(hull) * -1) > minimum_hull_size)):
                    rect = cv2.minAreaRect(hull)
                    (x, y), (width, height), angle = rect

                    aspect_ratio = float(width) / height

                    box = cv2.boxPoints(rect)
                    box = np.int0(box)

                    #draws the rotated rectangle
                    #cv2.drawContours(ProcessedFrame, [box], 0, (255, 0, 255), 2)

                    #if greater than 1, then width is greater than height
                    #we expect cones to be standing upright, hence being taller than they are wide
                    if aspect_ratio <= 1:
                        extreme_points = self.getExtremePoints(hull)

                        #gets the average of the left and right points
                        LRAvg = [
                            (extreme_points["left"][0] + extreme_points["right"][0])/2, 
                            (extreme_points["left"][1] + extreme_points["right"][1])/2]

                        #visualize Left - Right average point
                        #cv2.circle(ProcessedFrame, (int(LRAvg[0]), int(LRAvg[1])), 3, (255, 0, 255), 7)

                        #Essentially the height, gets the average of the top and bottom points
                        TBDistance = math.dist(extreme_points["bottom"], extreme_points["top"])

                        distance_from_LR_avg = []

                        distance_from_LR_avg.append(math.dist(LRAvg, extreme_points["top"]))
                        distance_from_LR_avg.append(math.dist(LRAvg, extreme_points["bottom"]))

                        #either the length from the top to the LR average 
                        #or the lenght from the bottom to the LR average
                        #must be less than 35% of the total height
                        valid_ratio = list(filter(lambda x: x < TBDistance * 0.35, distance_from_LR_avg))

                        #width and height are from rotated rectange above
                        if (len(valid_ratio) > 0) and (self.ConvexHullArea(hull) <= (width * height) * 0.5):
                            valid_hulls.append(hull)

        for hull in valid_hulls:
            cv2.drawContours(ProcessedFrame, [hull], 0, (255, 0, 255), 2)

            #https://stackoverflow.com/questions/66953166/how-to-find-the-direction-of-triangles-in-an-image-using-opencv
            #https://stackoverflow.com/questions/49799057/how-to-draw-a-point-in-an-image-using-given-co-ordinate-with-python-opencv
            #https://stackoverflow.com/questions/16615662/how-to-write-text-on-a-image-in-windows-using-python-opencv2

            #https://customers.pyimagesearch.com/lesson-sample-advanced-contour-properties/
            #https://docs.opencv.org/3.4/d1/d32/tutorial_py_contour_properties.html

        return ProcessedFrame


minimum_hull_size = 500

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