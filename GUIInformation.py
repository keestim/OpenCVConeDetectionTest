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

        #UI Window names
        self.fwindow_capture_name = 'Video Capture'
        self.fwindow_detection_name = 'Object Detection'
        self.fwindow_processed_img_name = 'Processed Capture'
        self.fwindow_depth_name = 'Depth Capture'
        self.flow_H_name = 'Low H'
        self.flow_S_name = 'Low S'
        self.flow_V_name = 'Low V'
        self.fhigh_H_name = 'High H'
        self.fhigh_S_name = 'High S'
        self.fhigh_V_name = 'High V'

        self.__createUIElements()

    def __on_low_H_thresh_trackbar(self, val):
        self.fHSV_adjustor_thread.set_low_H(val)
        self.fHSV_adjustor_thread.low_H = min(self.fHSV_adjustor_thread.getHighH() - 1, self.fHSV_adjustor_thread.getLowH())
        cv2.setTrackbarPos(self.flow_H_name, self.fwindow_detection_name, self.fHSV_adjustor_thread.getLowH())

    def __onHighHThreshTrackbar(self, val):
        self.fHSV_adjustor_thread.set_high_H(val)
        self.fHSV_adjustor_thread.high_H = max(self.fHSV_adjustor_thread.getHighH(), self.fHSV_adjustor_thread.getLowH() + 1)
        cv2.setTrackbarPos(self.fhigh_H_name, self.fwindow_detection_name, self.fHSV_adjustor_thread.getHighH())

    def __onLowSThreshTrackbar(self, val):
        self.fHSV_adjustor_thread.set_low_S(val)
        self.fHSV_adjustor_thread.low_S = min(self.fHSV_adjustor_thread.getHighS() - 1, self.fHSV_adjustor_thread.getLowS())
        cv2.setTrackbarPos(self.flow_S_name, self.fwindow_detection_name, self.fHSV_adjustor_thread.getLowS())

    def __onHighSThreshTrackbar(self, val):
        self.fHSV_adjustor_thread.set_high_S(val)
        self.fHSV_adjustor_thread.high_S = max(self.fHSV_adjustor_thread.getHighS(), self.fHSV_adjustor_thread.getLowS() + 1)
        cv2.setTrackbarPos(self.fhigh_S_name, self.fwindow_detection_name, self.fHSV_adjustor_thread.getHighS())

    def __onLowVThreshTrackbar(self, val):
        self.fHSV_adjustor_thread.set_low_V(val)
        self.fHSV_adjustor_thread.low_V = min(self.fHSV_adjustor_thread.getHighV() - 1, self.fHSV_adjustor_thread.getLowV())
        cv2.setTrackbarPos(self.flow_V_name, self.fwindow_detection_name, self.fHSV_adjustor_thread.getLowV())

    def __onHighVThreshTrackbar(self, val):
        self.fHSV_adjustor_thread.set_high_V(val)
        self.fHSV_adjustor_thread.high_V = max(self.fHSV_adjustor_thread.getHighV(), self.fHSV_adjustor_thread.getLowV() + 1)
        cv2.setTrackbarPos(self.fhigh_V_name, self.fwindow_detection_name, self.fHSV_adjustor_thread.getHighV())

    def __createUIElements(self):
        cv2.namedWindow(self.fwindow_capture_name)
        cv2.namedWindow(self.fwindow_detection_name)
        cv2.namedWindow(self.fwindow_processed_img_name)

        cv2.createTrackbar(
            self.flow_H_name, 
            self.fwindow_detection_name, 
            self.fHSV_processor_thread.getLowH(), 
            self.fHSV_processor_thread.getMaxValueH(), 
            self.__onLowHThreshTrackbar)

        cv2.createTrackbar(
            self.fhigh_H_name, 
            self.fwindow_detection_name, 
            self.fHSV_processor_thread.getHighH(), 
            self.fHSV_processor_thread.getMaxValueH(), 
            self.__onHighHThreshTrackbar)

        cv2.createTrackbar(
            self.flow_S_name, 
            self.fwindow_detection_name, 
            self.fHSV_processor_thread.getLowS(), 
            self.fHSV_processor_thread.getMaxValue(), 
            self.__onLowSThreshTrackbar)

        cv2.createTrackbar(
            self.fhigh_S_name, 
            self.fwindow_detection_name, 
            self.fHSV_processor_thread.getHighS(), 
            self.fHSV_processor_thread.getMaxValue(), 
            self.__onHighSThreshTrackbar)

        cv2.createTrackbar(
            self.flow_V_name, 
            self.fwindow_detection_name, 
            self.fHSV_processor_thread.getLowV(), 
            self.fHSV_processor_thread.getMaxValue(), 
            self.__onLowVThreshTrackbar)

        cv2.createTrackbar(
            self.fhigh_V_name, 
            self.fwindow_detection_name, 
            self.fHSV_processor_thread.getHighV(), 
            self.fHSV_processor_thread.getMaxValue(), 
            self.__onHighVThreshTrackbar)

    def renderWindowFrames(self):  
        cv2.imshow(self.fwindow_capture_name, self.fvideo_feed_thread.getRGBFrame())        
        cv2.imshow(self.fwindow_detection_name, self.fHSV_processor_thread.getFrameThreshold())
        cv2.imshow(self.fwindow_processed_img_name, self.fcone_detector_thread.getDetectedConeFrame())       

        if (self.fvideo_feed_thread.getDepthFrame() is not None):
            cv2.imshow(self.fwindow_depth_name, self.fvideo_feed_thread.getDepthFrame())   

