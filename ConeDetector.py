import cv2
import threading
import numpy as np
import random as rng
import math

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
            if cv2.contourArea(contour) >= 75:
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
                        valid_ratio = list(filter(lambda x: x < TBDistance * 0.4, distance_from_LR_avg))

                        #width and height are from rotated rectange above
                        if (len(valid_ratio) > 0) and (self.ConvexHullArea(hull) <= (width * height) * 0.70):
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

