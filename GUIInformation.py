#https://docs.opencv.org/3.4/da/d97/tutorial_threshold_inRange.html
#UI Stuff

from ConeDetector import *
from HSVProcessor import *
from HSVController import *
from HSVController import * 
from time import sleep

class GUIInformation:
    def __init__(self, video_feed, generate_frame_lock, render_frame_lock):
        self.fvideo_feed_thread = video_feed
        self.frender_frame_lock = render_frame_lock

        self.fHSV_controller_thread = HSVController(video_feed)
        self.fHSV_controller_thread.start()

        self.fHSV_processor_thread = HSVProcessor(self.fHSV_controller_thread, 
                                                    self.fvideo_feed_thread, 
                                                    generate_frame_lock)

        self.fHSV_processor_thread.start()
        sleep(0.2)

        self.fcone_detector_thread = ConeDetector(self.fHSV_processor_thread,
                                                  render_frame_lock)

        self.fcone_detector_thread.start()

        sleep(0.2)

        #UI Window names
        self.fwindow_frame_output = 'Visual Output'
        self.fwindow_UI_components = 'UI Components'
        
        self.flow_H_name = 'Low H'
        self.flow_S_name = 'Low S'
        self.flow_V_name = 'Low V'
        self.fhigh_H_name = 'High H'
        self.fhigh_S_name = 'High S'
        self.fhigh_V_name = 'High V'

        self.fplay_video_button = "Play Video"
        self.fpause_video_button = "Pause Video"

        self.__createUIElements()

    def __onLowHThreshTrackbar(self, val):
        self.fHSV_controller_thread.getHSVValueContainer().low_H = val
        self.fHSV_controller_thread.getHSVValueContainer().low_H = min(self.fHSV_controller_thread.getHSVValueContainer().high_H - 1, 
                                                                        self.fHSV_controller_thread.getHSVValueContainer().low_H)
        
        cv2.setTrackbarPos(self.flow_H_name,
                            self.fwindow_UI_components,
                            self.fHSV_controller_thread.getHSVValueContainer().low_H)

    def __onHighHThreshTrackbar(self, val):
        self.fHSV_controller_thread.getHSVValueContainer().high_H = val
        self.fHSV_controller_thread.getHSVValueContainer().high_H = max(self.fHSV_controller_thread.getHSVValueContainer().high_H, 
                                                                        self.fHSV_controller_thread.getHSVValueContainer().low_H + 1)
        
        cv2.setTrackbarPos(self.fhigh_H_name,
                            self.fwindow_UI_components,
                            self.fHSV_controller_thread.getHSVValueContainer().high_H)

    def __onLowSThreshTrackbar(self, val):
        self.fHSV_controller_thread.getHSVValueContainer().low_S = val
        self.fHSV_controller_thread.getHSVValueContainer().low_S = min(self.fHSV_controller_thread.getHSVValueContainer().high_S - 1, 
                                                                        self.fHSV_controller_thread.getHSVValueContainer().low_S)
        
        cv2.setTrackbarPos(self.flow_S_name,
                            self.fwindow_UI_components,
                            self.fHSV_controller_thread.getHSVValueContainer().low_S)

    def __onHighSThreshTrackbar(self, val):
        self.fHSV_controller_thread.getHSVValueContainer().high_S = val
        self.fHSV_controller_thread.getHSVValueContainer().high_S = max(self.fHSV_controller_thread.getHSVValueContainer().high_S, 
                                                                        self.fHSV_controller_thread.getHSVValueContainer().low_S + 1)
        
        cv2.setTrackbarPos(self.fhigh_S_name,
                            self.fwindow_UI_components, 
                            self.fHSV_controller_thread.getHSVValueContainer().high_S)

    def __onLowVThreshTrackbar(self, val):
        self.fHSV_controller_thread.getHSVValueContainer().low_V = val
        self.fHSV_controller_thread.getHSVValueContainer().low_V = min(self.fHSV_controller_thread.getHSVValueContainer().high_V - 1, 
                                                                        self.fHSV_controller_thread.getHSVValueContainer().low_V)
        
        cv2.setTrackbarPos(self.flow_V_name, 
                            self.fwindow_UI_components,
                            self.fHSV_controller_thread.getHSVValueContainer().low_V)

    def __onHighVThreshTrackbar(self, val):
        self.fHSV_controller_thread.getHSVValueContainer().high_V = val
        self.fHSV_controller_thread.getHSVValueContainer().high_V = max(self.fHSV_controller_thread.getHSVValueContainer().high_V,
                                                                        self.fHSV_controller_thread.getHSVValueContainer().low_V + 1)
        
        cv2.setTrackbarPos(self.fhigh_V_name, 
                            self.fwindow_UI_components, 
                            self.fHSV_controller_thread.getHSVValueContainer().high_V)

    def __onPlayVideoButton(self, val, other):
        print("PLAYING VIDEO")
    
    def __onPauseVideoButton(self, val, other):
        print("PAUSING VIDEO")
    
    #https://stackoverflow.com/questions/35180764/opencv-python-image-too-big-to-display
    def __resizeWithAspectRatio(self, image, width = None, height = None, inter = cv2.INTER_AREA):
        dim = None
        (h, w) = image.shape[:2]

        if width is None and height is None:
            return image
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))

        return cv2.resize(image, dim, interpolation = inter)

    def __createUIElements(self):
        # Windows are created
        cv2.namedWindow(self.fwindow_frame_output)
        cv2.namedWindow(self.fwindow_UI_components)

        cv2.createTrackbar(
            self.flow_H_name, 
            self.fwindow_UI_components, 
            self.fHSV_controller_thread.getHSVValueContainer().low_H, 
            MAX_HUE_VALUE, 
            self.__onLowHThreshTrackbar)

        cv2.createTrackbar(
            self.fhigh_H_name, 
            self.fwindow_UI_components, 
            self.fHSV_controller_thread.getHSVValueContainer().high_H, 
            MAX_HUE_VALUE, 
            self.__onHighHThreshTrackbar)

        cv2.createTrackbar(
            self.flow_S_name, 
            self.fwindow_UI_components, 
            self.fHSV_controller_thread.getHSVValueContainer().low_S, 
            MAX_VALUE, 
            self.__onLowSThreshTrackbar)

        cv2.createTrackbar(
            self.fhigh_S_name, 
            self.fwindow_UI_components, 
            self.fHSV_controller_thread.getHSVValueContainer().high_S, 
            MAX_VALUE, 
            self.__onHighSThreshTrackbar)

        cv2.createTrackbar(
            self.flow_V_name, 
            self.fwindow_UI_components, 
            self.fHSV_controller_thread.getHSVValueContainer().low_V, 
            MAX_VALUE, 
            self.__onLowVThreshTrackbar)

        cv2.createTrackbar(
            self.fhigh_V_name, 
            self.fwindow_UI_components, 
            self.fHSV_controller_thread.getHSVValueContainer().high_V, 
            MAX_VALUE, 
            self.__onHighVThreshTrackbar)

        cv2.createButton(
            self.fplay_video_button,
            self.__onPlayVideoButton,
            self.fwindow_UI_components, 
            cv2.QT_PUSH_BUTTON,
            1
        )

        cv2.createButton(
            self.fpause_video_button,
            self.__onPauseVideoButton,
            self.fwindow_UI_components, 
            cv2.QT_PUSH_BUTTON,
            1
        )

    def renderWindowFrames(self):  
        stacked_frames = self.fvideo_feed_thread.getRGBFrame()

        stacked_frames = np.concatenate((self.fvideo_feed_thread.getRGBFrame(), 
                                        self.fcone_detector_thread.getDetectedConeFrame()),
                                        axis = 0)

        stacked_frames = self.__resizeWithAspectRatio(stacked_frames, width = 720)
        cv2.imshow(self.fwindow_frame_output, stacked_frames)
