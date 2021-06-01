from ExternalImageReader import *
from GUIInformation import *

import cv2
import sys
from time import sleep
import threading
import os.path
    
if __name__ == "__main__":
    render_frame_lock = threading.Lock()
    generate_frame_lock = threading.Lock()

    try:
        input_image_path = sys.argv[1]
        if not os.path.isfile(input_image_path):
            raise Exception("file doesn't exist or bad file name")
    except:
        print("Please specify file name. ")
        sys.exit(0)
    finally:
        image_thread = ExternalImageReader(generate_frame_lock, input_image_path)
        image_thread.start()
    
    sleep(0.5)

    GUI_info = GUIInformation(image_thread, generate_frame_lock, render_frame_lock)

    while True:     
        GUI_info.renderWindowFrames()

        k = cv2.waitKey(5) & 0xFF

        if k == 27:
            break
    cv2.destroyAllWindows()
