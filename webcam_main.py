#theory from: 
#https://raw.githubusercontent.com/MicrocontrollersAndMore/Traffic_Cone_Detection_Visual_Basic/master/presentation/Steps%20With%20Images.pdf

from ExternalImageReader import *
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
    cap = cv2.VideoCapture(0)
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        

        # Display the resulting frame
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        print("test3")
        GUI_info = GUIInformation(frame)

        while True:     
            GUI_info.render_window_frames()

            k = cv2.waitKey(5) & 0xFF

            if k == 27:
                break
        cv2.destroyAllWindows()
