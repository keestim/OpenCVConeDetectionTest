from WebcamReader import *
from GUIInformation import *

import cv2
import threading
    
if __name__ == "__main__":
    render_frame_lock = threading.Lock()
    generate_frame_lock = threading.Lock()

    image_thread = WebcamReader()
    image_thread.start()

    GUI_info = GUIInformation(image_thread, generate_frame_lock, render_frame_lock)

    while True:     
        GUI_info.renderWindowFrames()

        k = cv2.waitKey(5) & 0xFF

        if k == 27:
            break
    cv2.destroyAllWindows()
