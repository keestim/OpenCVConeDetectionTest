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

minimum_hull_size = 250

#https://docs.opencv.org/3.4/da/d97/tutorial_threshold_inRange.html
#UI Stuff
max_value = 255
max_value_H = 360//2

low_H = 0
low_S = 61
low_V = 0
high_H = 116
high_S = 165
high_V = 255

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

#function to get RGB image from kinect
def get_video():
    array,_ = freenect.sync_get_video()
    array = cv2.cvtColor(array,cv2.COLOR_BGR2HSV)
    return array
 
#function to get depth image from kinect
def get_depth():
    array,_ = freenect.sync_get_depth()
    array = array.astype(np.uint8)
    return array

def getConvexHulls(contours):
    #https://docs.opencv.org/3.4/d7/d1d/tutorial_hull.html
    hull_list = []
    for i in range(len(contours)):
        hull = cv2.convexHull(contours[i])
        hull_list.append(hull)

    return hull_list

#https://stackoverflow.com/questions/6471023/how-to-calculate-convex-hull-area-using-opencv-functions
def ConvexHullArea(hull):
    area = 0
    for i in  range(len(hull) - 1):
        next_i = (i+1)%(len(hull))
        dX   = hull[next_i][0][0] - hull[i][0][0]
        avgY = (hull[next_i][0][1] + hull[i][0][1])/2
        area += dX * avgY;  # his is the integration step.

    return area

def processHullData(hull):
    output_vectors = []

    for selected_hull in hull:
        vector_arr = []

        vector_arr.append(selected_hull[0][0])
        vector_arr.append(selected_hull[0][1])

        output_vectors.append(vector_arr)

    return output_vectors

def twovVectGradient(vector_a, vector_b):
    try:
        gradient = (vector_b[1] - vector_a[1])/(vector_b[0] - vector_a[0])
    except:
        gradient = 0
    finally:
        return gradient

def hullPointingUp(hull):
    cloned_hull = hull.copy()

    y_axis_sorted = sorted(processHullData(cloned_hull), key=lambda a_entry: a_entry[1]) 
    x_axis_sorted = sorted(processHullData(cloned_hull), key=lambda a_entry: a_entry[0]) 

    left_point = x_axis_sorted[0]
    right_point = x_axis_sorted[len(x_axis_sorted) - 1]

    bottom_point = y_axis_sorted[0]
    top_point = y_axis_sorted[len(y_axis_sorted) - 1]

    left_avg_gradient = twovVectGradient(left_point, top_point)

    right_avg_gradient = twovVectGradient(right_point, top_point)

    #print("Left:" + str(left_point[0]) + ", " + str(left_point[1]))
    #print("Right:" + str(right_point[0]) + ", " + str(right_point[1]))
    #print("Top:" + str(top_point[0]) + ", " + str(top_point[1]))
    #print(str(left_avg_gradient) + " | " + str(right_avg_gradient) + " | " + str(left_avg_gradient <= 1 and right_avg_gradient <= -1))

    return (
        (left_avg_gradient <= 1.5 and left_avg_gradient >= 0) and 
        right_avg_gradient <= -0.5)

#next, find if convex hull is pointing up!
#geomalgorithms.com/a14-_extreme_pts.html

def getHullTopWidth(vector_arr):

    cloned_arr = vector_arr.copy()


def processImg(HSVThresholdFrame):  
    #print("New Loop!")

    kernel = np.ones((5, 5), np.uint8)

    output_img = cv2.erode(HSVThresholdFrame, kernel)
    output_img = cv2.dilate(output_img, kernel, iterations=2)
    output_img = cv2.GaussianBlur(output_img, (15, 15), 0)

    ret,thresh = cv2.threshold(output_img, 100, 255, 0)
    
    #https://towardsdatascience.com/edges-and-contours-basics-with-opencv-66d3263fd6d1
    edge = cv2.Canny(output_img, 30, 200)
    contours, h = cv2.findContours(edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    #cv2.drawContours(HSVThresholdFrame, contours[0], -1, (255,0,0), thickness = 5)

    processed_contours = []

    for contour in contours:
        if cv2.contourArea(contour) >= 20:
           processed_contours.append(contour) 

    valid_hulls = []

    for c in processed_contours:
        hull = cv2.convexHull(c)

        if ((len(hull) >= 3 or len(hull) <= 10) and 
            (ConvexHullArea(hull) > minimum_hull_size or 
            (ConvexHullArea(hull) * -1) > minimum_hull_size)
            and hullPointingUp(hull)):
            valid_hulls.append(hull)

    #whiteFrame = 255 * np.ones((1000,1000,3), np.uint8)

    for hull in valid_hulls:
        cv2.drawContours(output_img, [hull], 0, (255, 0, 255), 2)
    
    return output_img
    
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

    while 1:
        #get a frame from RGB camera
        frame = get_video()
        #get a frame from depth sensor
        depth = get_depth()

        #HSV (hue, saturation, value)
        frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frame_threshold = cv2.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))
        
        cv2.imshow(window_capture_name, frame)
        cv2.imshow(window_detection_name, frame_threshold)
        cv2.imshow(window_processedimg_name, processImg(frame_threshold))

        cv2.imshow(window_depth_name, depth)        

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()