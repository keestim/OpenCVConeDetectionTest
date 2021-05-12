import cv2
import threading
import numpy as np
import random as rng
import math
from time import sleep
import copy
class ConeDetector(threading.Thread):
    def __init__(self, hsv_processor, frame_thread_Lock):
        threading.Thread.__init__(self)
        self.fhsv_processor = hsv_processor
        self.fdetected_cone_frame = None
        self.fminimum_hull_size = 500

        self.fframe_thread_Lock = frame_thread_Lock

    def run(self):
        while True:
            current_frame = copy.deepcopy(self.fhsv_processor.get_procesed_frame())
            processed_contours = self.__generate_contours(current_frame)

            try:
                self.fframe_thread_Lock.acquire()
            finally:
                self.fdetected_cone_frame = self.__render_valid_convex_hulls(current_frame, processed_contours)
                self.fframe_thread_Lock.release()
                sleep(0.01)

    #https://jdhao.github.io/2019/02/23/crop_rotated_rectangle_opencv/
    #generates a cropped frame from the input frame and rotated rectangle attributes
    def __crop_img_from_rotated_rect(self, frame, box, width, height):
        src_points = box.astype("float32")
        dst_points = np.array(
                        [[0, height - 1], 
                        [0, 0], 
                        [width - 1, 0], 
                        [width -1, height - 1]], 
                        dtype="float32")

        M = cv2.getPerspectiveTransform(src_points, dst_points)
        warped = cv2.warpPerspective(frame, M, (width, height))

        return warped 

    def get_detected_cone_frame(self):
        return self.fdetected_cone_frame

    def __get_convex_hulls(self, contours):
        #https://docs.opencv.org/3.4/d7/d1d/tutorial_hull.html
        hull_list = []
        for i in range(len(contours)):
            hull = cv2.convexHull(contours[i])
            hull_list.append(hull)

        return hull_list

    #https://stackoverflow.com/questions/6471023/how-to-calculate-convex-hull-area-using-opencv-functions
    def __get_convex_hull_area(self, hull):
        area = 0
        for i in  range(len(hull) - 1):
            next_i = (i + 1) % (len(hull))
            dX   = hull[next_i][0][0] - hull[i][0][0]
            avgY = (hull[next_i][0][1] + hull[i][0][1])/2
            area += dX * avgY;  # this is the integration step.

        return area

    def __get_extreme_points(self, hull):
        left_most = tuple(hull[hull[:, :, 0].argmin()][0])
        right_most = tuple(hull[hull[:, :, 0].argmax()][0])
        top_most = tuple(hull[hull[:, :, 1].argmin()][0])
        bottom_most = tuple(hull[hull[:, :, 1].argmax()][0])

        return {'left': left_most, 'right': right_most, 'top': top_most, 'bottom': bottom_most}

    def __generate_contours(self, ProcessedFrame):
        #https://towardsdatascience.com/edges-and-contours-basics-with-opencv-66d3263fd6d1
        #get edges and then contours from the processed frame
        edge = cv2.Canny(ProcessedFrame, 30, 200)
        contours, h = cv2.findContours(edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        processed_contours = []

        #select contours that are greater than 20
        #this removes any irrelevant data
        for contour in contours:
            if cv2.contourArea(contour) >= 20:
                processed_contours.append(contour) 

        return processed_contours

    def __is_valid_convex_hull(self, hull, ProcessedFrame):
        #A valid hull must have between 3 and 10 edges
        if ((len(hull) >= 3 or len(hull) <= 10) and 
            (self.__get_convex_hull_area(hull) > self.fminimum_hull_size or 
            (self.__get_convex_hull_area(hull) * -1) > self.fminimum_hull_size)):
                rect = cv2.minAreaRect(hull)
                (x, y), (width, height), angle = rect

                extreme_points = self.__get_extreme_points(hull)
                
                #Essentially the height, gets the average of the top and bottom points
                TBDistance = math.dist(extreme_points["bottom"], extreme_points["top"])

                #Essentially the width, get the average of the left and right points
                LRDistance = math.dist(extreme_points["left"], extreme_points["right"]) 

                #flip the rotated rectangle width and height
                #IF the angle is less than 0 (OPENCV angle is always reports as a negative (not sure why))
                #AND the width is greater than the height of the convex hull (calculated from the extreme points) 
                if (angle < 0) and (TBDistance > LRDistance):
                    width_clone = width
                    width = height
                    height = width_clone
                    
                aspect_ratio = float(width) / height

                box = cv2.boxPoints(rect)
                box = np.int0(box)

                #if greater than 1, then width is greater than height
                #we expect cones to be standing upright, hence being taller than they are wide
                #aspect ratio must be also greater than 0.15, which aids in removed irrelevant data
                if (aspect_ratio <= 1) and (aspect_ratio >= 0.15):
                    #gets the average of the left and right points
                    LRAvg = [
                        (extreme_points["left"][0] + extreme_points["right"][0])/2, 
                        (extreme_points["left"][1] + extreme_points["right"][1])/2]

                    distance_from_LR_avg = []

                    distance_from_LR_avg.append(math.dist(LRAvg, extreme_points["top"]))
                    distance_from_LR_avg.append(math.dist(LRAvg, extreme_points["bottom"]))

                    #either the length from the top to the LR average 
                    #or the length from the bottom to the LR average
                    #must be less than 35% of the total height
                    valid_ratio = list(filter(lambda x: x < TBDistance * 0.35, distance_from_LR_avg))

                    #width and height are from rotated rectange above
                    #area of the convex hull must be less than OR equal to 65% of the area fo the rotated rectangle
                    if (len(valid_ratio) > 0) and (self.__get_convex_hull_area(hull) <= (width * height) * 0.65):
                        #gets a cropped frame of just what's contained within the rotated rectangle
                        cropped_hull = self.__crop_img_from_rotated_rect(ProcessedFrame, box, int(width), int(height))

                        #gets the mean RBG values of the frame
                        #this mean determines how "solid" the convex hull is
                        #if the mean is lower, it means the source data for the convex hull contains more gaps/empty space
                        #from testing, 100 seems like an adequate value
                        if (cv2.mean(cropped_hull)[0] > 100):
                            return True
        
        return False

    def __render_valid_convex_hulls(self, ProcessedFrame, ProcessedContours):
        #Although the array isn't current being used, this will be utilized later!
        valid_hulls = []
        t =  0
        cones = 0
        for c in ProcessedContours:
            hull = cv2.convexHull(c)
            
            if (self.__is_valid_convex_hull(hull, ProcessedFrame)):
                valid_hulls.append  (hull)           
                cv2.drawContours(ProcessedFrame, [hull], 0, (255, 0, 255), 2)
            

        return ProcessedFrame

