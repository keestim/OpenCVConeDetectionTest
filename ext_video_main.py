#theory from: 
#https://raw.githubusercontent.com/MicrocontrollersAndMore/Traffic_Cone_Detection_Visual_Basic/master/presentation/Steps%20With%20Images.pdf

from ExternalVideoReader import *
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
    try:
        vid_path = sys.argv[1]
        if not os.path.isfile(vid_path):
            raise Exception("file doesn't exist or bad file name")
    except:
        print("Please specify file name. ")
        sys.exit(0)
    finally:
        while(True):
            video_thread = ExternalVideoReader(vid_path)
            video_thread.start()
            print("yeet")
            
            sleep(0.5)
            
            GUI_info = GUIInformation(video_thread)

            while True:     
                GUI_info.render_window_frames()

                k = cv2.waitKey(27)

                if k == 27 & 0xFF == ord('q'):
                    break

            video_thread.release()
            cv2.destroyAllWindows()
