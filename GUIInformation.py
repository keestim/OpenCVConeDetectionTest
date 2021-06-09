#https://docs.opencv.org/3.4/da/d97/tutorial_threshold_inRange.html
#UI Stuff

from ConeDetector import *
from HSVController import *
from time import sleep
import PySimpleGUI as sg

class GUIInformation:
    __PREVIOUS_IMG_BTN_TXT = "Previous Image"
    __WRITE_XML_BTN_TXT = "Write XML"
    __NEXT_IMG_BTN_TXT = "Next Image"

    def __init__(self, video_feed, generate_frame_lock, render_frame_lock):
        self.fvideo_feed_thread = video_feed
        self.frender_frame_lock = render_frame_lock

        self.fHSV_controller_thread = HSVController(video_feed)
        self.fHSV_controller_thread.start()

        sleep(0.5)

        self.fcone_detector_thread = ConeDetector(self.fvideo_feed_thread, self.fHSV_controller_thread, render_frame_lock)
        self.fcone_detector_thread.start()

        sleep(0.2)

        #UI Window names
        self.fwindow_frame_output = 'Visual Output'
        self.fwindow_UI_components = 'UI Components'
        
        self.flow_V_name = 'Low V'

        self.fhigh_V_name = 'High V'

        self.flayout = None
        self.fwindow = None

        self.__createUIElements()

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
        '''
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
        '''

        # create the window and show it without the plot
        self.flayout = [[sg.Image(filename='', key='image')], 
                        [sg.Button(self.__PREVIOUS_IMG_BTN_TXT), 
                        sg.Button(self.__WRITE_XML_BTN_TXT), 
                        sg.Button(self.__NEXT_IMG_BTN_TXT)]]
        
        self.fwindow = sg.Window('Output Window', self.flayout)
    
    def __windowListener(self, event, values):
        if (event == self.__PREVIOUS_IMG_BTN_TXT):
            print(event)
        elif (event == self.__NEXT_IMG_BTN_TXT):
            print(event)
        elif (event == self.__WRITE_XML_BTN_TXT):
            print(event)

    def renderWindowFrames(self):  
        while self.fwindow(timeout = 0.01)[0] is not None:
            stacked_frames = np.concatenate((self.fvideo_feed_thread.getRGBFrame(), 
                                            self.fcone_detector_thread.getDetectedConeFrame()),
                                            axis = 0)

            stacked_frames = self.__resizeWithAspectRatio(stacked_frames, width = 720)
            self.fwindow['image'](data=cv2.imencode('.png', stacked_frames)[1].tobytes())

            event, values = self.fwindow._ReadNonBlocking()
            self.__windowListener(event, values)

        
