#theory from: 
#https://raw.githubusercontent.com/MicrocontrollersAndMore/Traffic_Cone_Detection_Visual_Basic/master/presentation/Steps%20With%20Images.pdf

from ExternalImageReader import *
from GUIInformation import *

from abc import ABC, abstractmethod

import cv2
import numpy as np
import time
from time import sleep
from enum import Enum 
import threading
    
if __name__ == "__main__":
    image_thread = ExternalImageReader("./RGB_Source.png")
    image_thread.start()
    
    sleep(0.5)

    GUI_info = GUIInformation(image_thread)

    while True:     
        GUI_info.render_window_frames()

        k = cv2.waitKey(5) & 0xFF

        if k == 27:
            break
    cv2.destroyAllWindows()
