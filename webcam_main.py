#theory from: 
#https://raw.githubusercontent.com/MicrocontrollersAndMore/Traffic_Cone_Detection_Visual_Basic/master/presentation/Steps%20With%20Images.pdf

from WebcamReader import *
from GUIInformation import *

from abc import ABC, abstractmethod

import cv2
import sys
import numpy as np
import time
from time import sleep
from enum import Enum 
import threading
import os.path
    
if __name__ == "__main__":
    image_thread = WebcamReader()
    image_thread.start()
    while(True):
        # Capture frame-by-frame

        # Display the resulting frame
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        GUI_info = GUIInformation(image_thread)

        while True:     
            GUI_info.render_window_frames()

            k = cv2.waitKey(100) & 0xFF

            if k == 27:
                break
        cv2.destroyAllWindows()
