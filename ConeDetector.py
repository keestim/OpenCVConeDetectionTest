import cv2
import threading
import numpy as np
import random as rng
import math
from time import sleep
import copy

class ConeDetector(threading.Thread):
    __MIN_HULL_EDGES = 3
    __MAX_HULL_EDGES = 10

    def __init__(self, video_thread, HSV_controller, frame_thread_Lock):
        threading.Thread.__init__(self)
        self.fvideo_thread = video_thread
        self.fHSV_controller = HSV_controller

        self.fraw_HSV_frame = None
        self.fprocessed_HSV_frame = None

        self.fdetected_cone_frame = None
        self.fminimum_hull_size = 200
        self.fminimum_contour_size = 10
        self.fminimum_rotated_rect_mean_brightness = 100

        self.fframe_thread_Lock = frame_thread_Lock

    def run(self):
        while True:
            self.fraw_HSV_frame = self.__getHSVThresholdFrame()
            self.fprocessed_HSV_image = self.__processRawHSVImg()
            processed_contours = self.__generateContours(self.fprocessed_HSV_image)

            try:
                self.fframe_thread_Lock.acquire()
            finally:
                self.fdetected_cone_frame = self.__renderValidConvexHulls(self.fprocessed_HSV_image, 
                                                                            processed_contours)
                self.fframe_thread_Lock.release()
                sleep(0.01)

    def __getHSVThresholdFrame(self):
        return cv2.inRange(
            self.fvideo_thread.getHSVFrame(),
            (self.fHSV_controller.getHSVValueContainer().low_H,
            self.fHSV_controller.getHSVValueContainer().low_S, 
            self.fHSV_controller.getHSVValueContainer().low_V),
            (self.fHSV_controller.getHSVValueContainer().high_H,
            self.fHSV_controller.getHSVValueContainer().high_S,
            self.fHSV_controller.getHSVValueContainer().high_V)) 

    def __processRawHSVImg(self):
        output_img = self.fraw_HSV_frame

        kernel = np.ones((3, 3), np.uint8)
        output_img = cv2.erode(output_img, kernel, iterations=1)
        output_img = cv2.dilate(output_img, kernel, iterations=1)
        output_img = cv2.GaussianBlur(output_img, (3, 3), 0)

        return cv2.cvtColor(output_img, cv2.COLOR_GRAY2RGB)

    #https://jdhao.github.io/2019/02/23/crop_rotated_rectangle_opencv/
    #generates a cropped frame from the input frame and rotated rectangle attributes
    def __cropImageFromRotatedRect(self, frame, box, width, height):
        src_points = box.astype("float32")
        dst_points = np.array(
                        [[0, height - 1], 
                        [0, 0], 
                        [width - 1, 0], 
                        [width -1, height - 1]], 
                        dtype="float32")

        m = cv2.getPerspectiveTransform(src_points, dst_points)
        warped = cv2.warpPerspective(frame, m, (width, height))

        return warped 

    def getDetectedConeFrame(self):
        return self.fdetected_cone_frame

    #https://stackoverflow.com/questions/6471023/how-to-calculate-convex-hull-area-using-opencv-functions
    def __getConvexHullArea(self, hull):
        area = 0
        for i in  range(len(hull) - 1):
            next_i = (i + 1) % (len(hull))
            dX   = hull[next_i][0][0] - hull[i][0][0]
            avg_y = (hull[next_i][0][1] + hull[i][0][1]) / 2
            area += dX * avg_y;  # this is the integration step.

        return area

    def __generateContours(self, processed_frame):
        #https://towardsdatascience.com/edges-and-contours-basics-with-opencv-66d3263fd6d1
        #get edges and then contours from the processed frame
        edge = cv2.Canny(processed_frame, 80, 160)
        contours, h = cv2.findContours(edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        processed_contours = []

        #select contours that are greater than 20
        #this removes any irrelevant data
        for contour in contours:
            if cv2.contourArea(contour) >= self.fminimum_contour_size:
                processed_contours.append(contour) 

        return processed_contours

    #https://github.com/mustafaezer/traffic-cone-detection/blob/master/main.py
    def __convexHullPointingUp(self, convex_hull):
        points_above_center = []
        points_below_center = []

        x, y, width, height = cv2.boundingRect(convex_hull)
        aspect_ratio = width / height

        if 0.15 <= aspect_ratio <= 0.8:
            vertical_center = y + (height / 2)

            for point in convex_hull:
                if point[0][1] < vertical_center:
                    points_above_center.append(point)
                elif point[0][1] >= vertical_center:
                    points_below_center.append(point)

            left_x = points_below_center[0][0][0]
            right_x = points_below_center[0][0][0]
            for point in points_below_center:
                if point[0][0] < left_x:
                    left_x = point[0][0]
                if point[0][0] > right_x:
                    right_x = point[0][0]

            for point in points_above_center:
                if (point[0][0] < left_x) or (point[0][0] > right_x):
                    return False
        else:
            return False

        return True

    def __getHullMeanBrightness(self, hull, processed_frame):
        rect = cv2.minAreaRect(hull)
        (x, y), (width, height), angle = rect

        box = cv2.boxPoints(rect)
        box = np.int0(box)

        #gets a cropped frame of just what's contained within the rotated rectangle
        cropped_hull = self.__cropImageFromRotatedRect(processed_frame, box, int(width), int(height))

        #gets the mean RBG values of the frame
        #this mean determines how "solid" the convex hull is
        #if the mean is lower, it means the source data for the convex hull contains more gaps/empty space
        #from testing, 100 seems like an adequate value
        return cv2.mean(cropped_hull)[0]

    def __isValidConvexHull(self, hull, processed_frame):
        #A valid hull must have between 3 and 10 edges
        if ((len(hull) >= self.__MIN_HULL_EDGES or len(hull) <= self.__MAX_HULL_EDGES) and 
            (self.__getConvexHullArea(hull) > self.fminimum_hull_size or 
            (self.__getConvexHullArea(hull) * -1) > self.fminimum_hull_size)):
                if self.__convexHullPointingUp(hull):
                    return (self.__getHullMeanBrightness(hull, processed_frame) > self.fminimum_rotated_rect_mean_brightness)        
        return False

    def __renderValidConvexHulls(self, processed_frame, processed_contours):
        for c in processed_contours:
            hull = cv2.convexHull(c)
            
            if (self.__isValidConvexHull(hull, processed_frame)):
                cv2.drawContours(processed_frame, [hull], 0, (255, 0, 255), 4)

        return processed_frame

