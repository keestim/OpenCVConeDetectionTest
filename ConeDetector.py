import cv2
import threading
import numpy as np
import random as rng
import math
from time import sleep
import copy

class ConeDetector(threading.Thread):
    def __init__(self, video_thread, HSV_controller, frame_thread_Lock):
        threading.Thread.__init__(self)
        self.fvideo_thread = video_thread
        self.fHSV_controller = HSV_controller

        self.fraw_HSV_frame = None
        self.fprocessed_HSV_frame = None

        self.fdetected_cone_frame = None
        self.fminimum_hull_size = 2000
        self.fminimum_contour_size = 10
        self.fminimum_rotated_rect_mean_brightness = 100

        self.fframe_thread_Lock = frame_thread_Lock

        self.fdilation_amt = 5
        self.fdilation_itterations = 2

        self.ferode_amt = 2

        self.fblur_amt = 15

    def run(self):
        while True:
            self.fraw_HSV_frame = self.__getHSVThresholdFrame()
            self.fprocessed_HSV_image = self.__processRawHSVImg()
            processed_contours = self.__generateContours(self.fprocessed_HSV_image)

            try:
                self.fframe_thread_Lock.acquire()
            finally:
                self.fdetected_cone_frame = self.__renderValidConvexHulls(self.fprocessed_HSV_image, processed_contours)
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

    def __getConvexHulls(self, contours):
        #https://docs.opencv.org/3.4/d7/d1d/tutorial_hull.html
        hull_list = []
        for i in range(len(contours)):
            hull = cv2.convexHull(contours[i])
            hull_list.append(hull)

        return hull_list

    #https://stackoverflow.com/questions/6471023/how-to-calculate-convex-hull-area-using-opencv-functions
    def __getConvexHullArea(self, hull):
        area = 0
        for i in  range(len(hull) - 1):
            next_i = (i + 1) % (len(hull))
            dX   = hull[next_i][0][0] - hull[i][0][0]
            avg_y = (hull[next_i][0][1] + hull[i][0][1])/2
            area += dX * avg_y;  # this is the integration step.

        return area

    def __getExtremePoints(self, hull):
        left_most = tuple(hull[hull[:, :, 0].argmin()][0])
        right_most = tuple(hull[hull[:, :, 0].argmax()][0])
        top_most = tuple(hull[hull[:, :, 1].argmin()][0])
        bottom_most = tuple(hull[hull[:, :, 1].argmax()][0])

        return {'left': left_most, 'right': right_most, 'top': top_most, 'bottom': bottom_most}

    def __generateContours(self, ProcessedFrame):
        #https://towardsdatascience.com/edges-and-contours-basics-with-opencv-66d3263fd6d1
        #get edges and then contours from the processed frame
        edge = cv2.Canny(ProcessedFrame, 80, 160)
        contours, h = cv2.findContours(edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        processed_contours = []

        #select contours that are greater than 20
        #this removes any irrelevant data
        for contour in contours:
            if cv2.contourArea(contour) >= self.fminimum_contour_size:
                processed_contours.append(contour) 

        return processed_contours

    def __convexHullPointingUp(self, ch):
        pointsAboveCenter, poinstBelowCenter = [], []

        x, y, w, h = cv2.boundingRect(ch)
        aspectRatio = w / h

        if aspectRatio < 0.8:
            verticalCenter = y + h / 2

            for point in ch:
                if point[0][1] < verticalCenter:
                    pointsAboveCenter.append(point)
                elif point[0][1] >= verticalCenter:
                    poinstBelowCenter.append(point)

            leftX = poinstBelowCenter[0][0][0]
            rightX = poinstBelowCenter[0][0][0]
            for point in poinstBelowCenter:
                if point[0][0] < leftX:
                    leftX = point[0][0]
                if point[0][0] > rightX:
                    rightX = point[0][0]

            for point in pointsAboveCenter:
                if (point[0][0] < leftX) or (point[0][0] > rightX):
                    return False

        else:
            return False

        return True

    def __isValidConvexHull(self, hull, ProcessedFrame):
        #A valid hull must have between 3 and 10 edges
        if ((len(hull) >= 3 or len(hull) <= 10) and 
            (self.__getConvexHullArea(hull) > self.fminimum_hull_size or 
            (self.__getConvexHullArea(hull) * -1) > self.fminimum_hull_size)):
                return self.__convexHullPointingUp(hull)

                rect = cv2.minAreaRect(hull)
                (x, y), (width, height), angle = rect

                extreme_points = self.__getExtremePoints(hull)
                
                #Essentially the height, gets the average of the top and bottom points
                top_bottom_distance = math.dist(extreme_points["bottom"], extreme_points["top"])

                #Essentially the width, get the average of the left and right points
                left_right_distance = math.dist(extreme_points["left"], extreme_points["right"]) 

                #flip the rotated rectangle width and height
                #IF the angle is less than 0 (OPENCV angle is always reports as a negative (not sure why))
                #AND the width is greater than the height of the convex hull (calculated from the extreme points) 
                if (angle < 0 or angle == 90) and (top_bottom_distance > left_right_distance):
                    width_clone = width
                    width = height
                    height = width_clone
                    
                aspect_ratio = float(width) / height

                box = cv2.boxPoints(rect)
                box = np.int0(box)

                #if greater than 1, then width is greater than height
                #we expect cones to be standing upright, hence being taller than they are wide
                #aspect ratio must be also greater than 0.15, which aids in removed irrelevant data

                #TODO look for issues here onwards!!!
                if (aspect_ratio <= 1) and (aspect_ratio >= 0.15):

                    #gets the average of the left and right points
                    left_right_avg = [
                        (extreme_points["left"][0] + extreme_points["right"][0])/2, 
                        (extreme_points["left"][1] + extreme_points["right"][1])/2]

                    distance_from_left_right_avg = []
                    distance_from_left_right_avg.append(math.dist(left_right_avg, extreme_points["top"]))
                    distance_from_left_right_avg.append(math.dist(left_right_avg, extreme_points["bottom"]))

                    #either the length from the top to the LR average 
                    #or the length from the bottom to the LR average
                    #must be less than 35% of the total height
                    valid_ratio = list(filter(lambda x: x < top_bottom_distance * 0.5, distance_from_left_right_avg))

                    #width and height are from rotated rectange above
                    #area of the convex hull must be less than OR equal to 65% of the area fo the rotated rectangle
                    if (len(valid_ratio) > 0) and (self.__getConvexHullArea(hull) <= (width * height) * 0.7):
                        #gets a cropped frame of just what's contained within the rotated rectangle
                        cropped_hull = self.__cropImageFromRotatedRect(ProcessedFrame, box, int(width), int(height))

                        #gets the mean RBG values of the frame
                        #this mean determines how "solid" the convex hull is
                        #if the mean is lower, it means the source data for the convex hull contains more gaps/empty space
                        #from testing, 100 seems like an adequate value
                        if (cv2.mean(cropped_hull)[0] > self.fminimum_rotated_rect_mean_brightness):
                            return True
        
        return False

    def __renderValidConvexHulls(self, ProcessedFrame, ProcessedContours):
        #Although the array isn't current being used, this will be utilized later!
        valid_hulls = []
        t =  0
        cones = 0
        for c in ProcessedContours:
            hull = cv2.convexHull(c)
            
            if (self.__isValidConvexHull(hull, ProcessedFrame)):
                valid_hulls.append(hull)       

                cv2.drawContours(ProcessedFrame, [hull], 0, (255, 0, 255), 2)

        return ProcessedFrame

