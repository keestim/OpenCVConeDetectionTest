#https://docs.opencv.org/3.4/da/d97/tutorial_threshold_inRange.html
#UI Stuff

from ConeDetector import *
from HSVProcessor import *
from HSVController import *
from time import sleep

class GUIInformation:
    def __init__(self, video_feed, generate_frame_lock, render_frame_lock):
        self.fvideo_feed_thread = video_feed
        self.frender_frame_lock = render_frame_lock

        self.fHSV_controller_thread = HSVController(video_feed)
        self.fHSV_controller_thread.start()

        self.fHSV_processor_thread = HSVProcessor(
                                        self.fHSV_controller_thread, 
                                        self.fvideo_feed_thread, 
                                        generate_frame_lock)

        self.fHSV_processor_thread.start()
        sleep(0.2)

        self.fcone_detector_thread = ConeDetector(
                                        self.fHSV_processor_thread,
                                        render_frame_lock)
        self.fcone_detector_thread.start()

        sleep(0.2)

        #UI Window and Input names
        self.fwindow_capture_name = 'Video Capture'
        self.fwindow_detection_name = 'Object Detection'
        self.fwindow_processedimg_name = 'Processed Capture'
        self.fwindow_depth_name = 'Depth Capture'
        self.flow_H_name = 'Low H'
        self.flow_S_name = 'Low S'
        self.flow_V_name = 'Low V'
        self.fhigh_H_name = 'High H'
        self.fhigh_S_name = 'High S'
        self.fhigh_V_name = 'High V'

        self.__create_UI_elements()

    def __on_low_H_thresh_trackbar(self, val):
        self.fHSV_controller_thread.set_low_H(val)
        self.fHSV_controller_thread.low_H = min(self.fHSV_controller_thread.get_high_H() - 1, self.fHSV_controller_thread.get_low_H())
        cv2.setTrackbarPos(self.flow_H_name, self.fwindow_detection_name, self.fHSV_controller_thread.get_low_H())

    def __on_high_H_thresh_trackbar(self, val):
        self.fHSV_controller_thread.set_high_H(val)
        self.fHSV_controller_thread.high_H = max(self.fHSV_controller_thread.get_high_H(), self.fHSV_controller_thread.get_low_H() + 1)
        cv2.setTrackbarPos(self.fhigh_H_name, self.fwindow_detection_name, self.fHSV_controller_thread.get_high_H())

    def __on_low_S_thresh_trackbar(self, val):
        self.fHSV_controller_thread.set_low_S(val)
        self.fHSV_controller_thread.low_S = min(self.fHSV_controller_thread.get_high_S() - 1, self.fHSV_controller_thread.get_low_S())
        cv2.setTrackbarPos(self.flow_S_name, self.fwindow_detection_name, self.fHSV_controller_thread.get_low_S())

    def __on_high_S_thresh_trackbar(self, val):
        self.fHSV_controller_thread.set_high_S(val)
        self.fHSV_controller_thread.high_S = max(self.fHSV_controller_thread.get_high_S(), self.fHSV_controller_thread.get_low_S() + 1)
        cv2.setTrackbarPos(self.fhigh_S_name, self.fwindow_detection_name, self.fHSV_controller_thread.get_high_S())

    def __on_low_V_thresh_trackbar(self, val):
        self.fHSV_controller_thread.set_low_V(val)
        self.fHSV_controller_thread.low_V = min(self.fHSV_controller_thread.get_high_V() - 1, self.fHSV_controller_thread.get_low_V())
        cv2.setTrackbarPos(self.flow_V_name, self.fwindow_detection_name, self.fHSV_controller_thread.get_low_V())

    def __on_high_V_thresh_trackbar(self, val):
        self.fHSV_controller_thread.set_high_V(val)
        self.fHSV_controller_thread.high_V = max(self.fHSV_controller_thread.get_high_V(), self.fHSV_controller_thread.get_low_V() + 1)
        cv2.setTrackbarPos(self.fhigh_V_name, self.fwindow_detection_name, self.fHSV_controller_thread.get_high_V())

    def __create_UI_elements(self):
        cv2.namedWindow(self.fwindow_capture_name)
        cv2.namedWindow(self.fwindow_detection_name)
        cv2.namedWindow(self.fwindow_processedimg_name)

        cv2.createTrackbar(
            self.flow_H_name, 
            self.fwindow_detection_name, 
            self.fHSV_controller_thread.get_low_H(), 
            self.fHSV_controller_thread.get_max_value_H(), 
            self.__on_low_H_thresh_trackbar)

        cv2.createTrackbar(
            self.fhigh_H_name, 
            self.fwindow_detection_name, 
            self.fHSV_controller_thread.get_high_H(), 
            self.fHSV_controller_thread.get_max_value_H(), 
            self.__on_high_H_thresh_trackbar)

        cv2.createTrackbar(
            self.flow_S_name, 
            self.fwindow_detection_name, 
            self.fHSV_controller_thread.get_low_S(), 
            self.fHSV_controller_thread.get_max_value(), 
            self.__on_low_S_thresh_trackbar)

        cv2.createTrackbar(
            self.fhigh_S_name, 
            self.fwindow_detection_name, 
            self.fHSV_controller_thread.get_high_S(), 
            self.fHSV_controller_thread.get_max_value(), 
            self.__on_high_S_thresh_trackbar)

        cv2.createTrackbar(
            self.flow_V_name, 
            self.fwindow_detection_name, 
            self.fHSV_controller_thread.get_low_V(), 
            self.fHSV_controller_thread.get_max_value(), 
            self.__on_low_V_thresh_trackbar)

        cv2.createTrackbar(
            self.fhigh_V_name, 
            self.fwindow_detection_name, 
            self.fHSV_controller_thread.get_high_V(), 
            self.fHSV_controller_thread.get_max_value(), 
            self.__on_high_V_thresh_trackbar)

    def render_window_frames(self):

        cv2.imshow(self.fwindow_depth_name, self.fvideo_feed_thread.get_depth_frame())    
        cv2.imshow(self.fwindow_capture_name, self.fvideo_feed_thread.get_RGB_frame())        
        cv2.imshow(self.fwindow_detection_name, self.fHSV_processor_thread.get_frame_threshold())
        cv2.imshow(self.fwindow_processedimg_name, self.fcone_detector_thread.get_detected_cone_frame())        
        
