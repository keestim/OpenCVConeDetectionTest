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

        self.fHSV_processor_thread = HSVProcessor(self.fHSV_controller_thread, 
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
        self.fwindow_frame_output = 'Visual Output'
        self.fwindow_UI_components = 'UI Components'

        '''
        self.fwindow_capture_name = 'Video Capture'
        self.fwindow_processed_img_name = 'Processed Capture'
        self.fwindow_depth_name = 'Depth Capture'
        '''
        
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
        self.fHSV_controller_thread.setLowH(val)
        self.fHSV_controller_thread.low_H = min(self.fHSV_controller_thread.getHighH() - 1, 
                                                self.fHSV_controller_thread.getLowH())
        
        cv2.setTrackbarPos(self.flow_H_name,
                            self.fwindow_UI_components,
                            self.fHSV_controller_thread.getLowH())

    def __onHighHThreshTrackbar(self, val):
        self.fHSV_controller_thread.setHighH(val)
        self.fHSV_controller_thread.high_H = max(self.fHSV_controller_thread.getHighH(), 
                                                self.fHSV_controller_thread.getLowH() + 1)
        
        cv2.setTrackbarPos(self.fhigh_H_name,
                            self.fwindow_UI_components,
                            self.fHSV_controller_thread.getHighH())

    def __onLowSThreshTrackbar(self, val):
        self.fHSV_controller_thread.setLowS(val)
        self.fHSV_controller_thread.low_S = min(self.fHSV_controller_thread.getHighS() - 1, 
                                                self.fHSV_controller_thread.getLowS())
        
        cv2.setTrackbarPos(self.flow_S_name,
                            self.fwindow_UI_components,
                            self.fHSV_controller_thread.getLowS())

    def __onHighSThreshTrackbar(self, val):
        self.fHSV_controller_thread.setHighS(val)
        self.fHSV_controller_thread.high_S = max(self.fHSV_controller_thread.getHighS(), 
                                                self.fHSV_controller_thread.getLowS() + 1)
        
        cv2.setTrackbarPos(self.fhigh_S_name,
                            self.fwindow_UI_components, 
                            self.fHSV_controller_thread.getHighS())

    def __onLowVThreshTrackbar(self, val):
        self.fHSV_controller_thread.setLowV(val)
        self.fHSV_controller_thread.low_V = min(self.fHSV_controller_thread.getHighV() - 1, 
                                                self.fHSV_controller_thread.getLowV())
        
        cv2.setTrackbarPos(self.flow_V_name, 
                            self.fwindow_UI_components,
                            self.fHSV_controller_thread.getLowV())

    def __onHighVThreshTrackbar(self, val):
        self.fHSV_controller_thread.setHighV(val)
        self.fHSV_controller_thread.high_V = max(self.fHSV_controller_thread.getHighV(),
                                                self.fHSV_controller_thread.getLowV() + 1)
        
        cv2.setTrackbarPos(self.fhigh_V_name, 
                            self.fwindow_UI_components, 
                            self.fHSV_controller_thread.getHighV())

    def __onPlayVideoButton(self, val, other):
        print("PLAYING VIDEO")
    
    def __onPauseVideoButton(self, val, other):
        print("PAUSING VIDEO")
    
    #https://stackoverflow.com/questions/35180764/opencv-python-image-too-big-to-display
    def __resizeWithAspectRatio(self, image, width=None, height=None, inter=cv2.INTER_AREA):
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

        return cv2.resize(image, dim, interpolation=inter)

    def __createUIElements(self):
        # Windows are created
        cv2.namedWindow(self.fwindow_frame_output)
        cv2.namedWindow(self.fwindow_UI_components)

        cv2.createTrackbar(
            self.flow_H_name, 
            self.fwindow_UI_components, 
            self.fHSV_controller_thread.getLowH(), 
            self.fHSV_controller_thread.getMaxValueH(), 
            self.__onLowHThreshTrackbar)

        cv2.createTrackbar(
            self.fhigh_H_name, 
            self.fwindow_UI_components, 
            self.fHSV_controller_thread.getHighH(), 
            self.fHSV_controller_thread.getMaxValueH(), 
            self.__onHighHThreshTrackbar)

        cv2.createTrackbar(
            self.flow_S_name, 
            self.fwindow_UI_components, 
            self.fHSV_controller_thread.getLowS(), 
            self.fHSV_controller_thread.getMaxValue(), 
            self.__onLowSThreshTrackbar)

        cv2.createTrackbar(
            self.fhigh_S_name, 
            self.fwindow_UI_components, 
            self.fHSV_controller_thread.getHighS(), 
            self.fHSV_controller_thread.getMaxValue(), 
            self.__onHighSThreshTrackbar)

        cv2.createTrackbar(
            self.flow_V_name, 
            self.fwindow_UI_components, 
            self.fHSV_controller_thread.getLowV(), 
            self.fHSV_controller_thread.getMaxValue(), 
            self.__onLowVThreshTrackbar)

        cv2.createTrackbar(
            self.fhigh_V_name, 
            self.fwindow_UI_components, 
            self.fHSV_controller_thread.getHighV(), 
            self.fHSV_controller_thread.getMaxValue(), 
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
        stacked_frames = np.concatenate((self.fvideo_feed_thread.getRGBFrame(), 
                                        self.fcone_detector_thread.getDetectedConeFrame()),
                                        axis = 0)

        stacked_frames = self.__resizeWithAspectRatio(stacked_frames, width = 720)
        cv2.imshow(self.fwindow_frame_output, stacked_frames)
        
        '''
        cv2.imshow(self.fwindow_capture_name, 
                    self.fvideo_feed_thread.getRGBFrame())        
        
        if (self.fcone_detector_thread.getDetectedConeFrame() is not None):
            cv2.imshow(self.fwindow_processed_img_name, 
                        self.fcone_detector_thread.getDetectedConeFrame())       

        cv2.imshow(self.fwindow_detection_name, 
                    self.fHSV_processor_thread.getFrameThreshold())

        if (self.fvideo_feed_thread.getDepthFrame() is not None):
            cv2.imshow(self.fwindow_depth_name, 
                        self.fvideo_feed_thread.getDepthFrame())   
        '''