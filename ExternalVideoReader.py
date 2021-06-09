from VideoSource import *

import threading
import cv2
import time

class ExternalVideoReader(VideoSource, threading.Thread):
    def __init__(self, frame_thread_Lock, file_src):
        self.ffile_src = file_src

        self.fframe_counter = 0
        self.flast_frame_time = time.time()

        self.fvideo_capture = cv2.VideoCapture(self.ffile_src)
        self.fvideo_frame_rate = self.fvideo_capture.get(cv2.CAP_PROP_FPS)
        self.ftotal_frames = self.fvideo_capture.get(cv2.CAP_PROP_FRAME_COUNT)

        VideoSource.__init__(self, frame_thread_Lock)
        threading.Thread.__init__(self)

        self.fRGB_frame = self.getVideo()
        self.fdepth_frame = self.getDepth()

    def getFileSrc(self):
        return self.ffile_src
    
    def run(self):
        while self.fvideo_capture.isOpened():
            self.fRGB_frame = self.getVideo()

            self.fHSV_frame = ~cv2.cvtColor(self.fRGB_frame, cv2.COLOR_RGB2HSV)

            self.fdepth_frame = self.getDepth()

    #function to get RGB image from external video file
    def getVideo(self):
        if (((time.time() - self.flast_frame_time) >= (1/self.fvideo_frame_rate)) or 
            (self.fRGB_frame is None)):
            success, frame = self.fvideo_capture.read()

            self.flast_frame_time = time.time()

            if success:
                self.fframe_counter += 1
                return frame
            else:
                print("Can't receive frame (stream end?).")   

                if (self.fframe_counter >= (self.ftotal_frames - 1)):
                    print("Attempting to reset video")
                    self.fvideo_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    self.fframe_counter = 0

                    return self.fRGB_frame
        else:
            return self.fRGB_frame

    #function to get depth image from external video file
    def getDepth(self):
        return None
        
