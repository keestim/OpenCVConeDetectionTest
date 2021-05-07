#theory from: 
#https://raw.githubusercontent.com/MicrocontrollersAndMore/Traffic_Cone_Detection_Visual_Basic/master/presentation/Steps%20With%20Images.pdf

from KinectVideoReader import *
from GUIInformation import *

from abc import ABC, abstractmethod

import cv2
import numpy as np
from time import sleep
from enum import Enum 
import threading
    
if __name__ == "__main__":
    render_frame_lock = threading.Lock()
    generate_frame_lock = threading.Lock()
    
    kinect_video_thread = KinectVideoReader(generate_frame_lock)
    kinect_video_thread.start()

    sleep(0.1)

    GUI_info = GUIInformation(kinect_video_thread, generate_frame_lock, render_frame_lock)

    while True:     
        try:
            render_frame_lock.acquire()
        finally:
            GUI_info.render_window_frames()
            render_frame_lock.release()
            sleep(0.01)

        k = cv2.waitKey(5) & 0xFF

        if k == 27:
            break
    cv2.destroyAllWindows()
