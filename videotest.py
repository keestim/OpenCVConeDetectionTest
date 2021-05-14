import numpy as np
import cv2 as cv2

while True:
    cap = cv2.VideoCapture('Presentation.mp4')
    repeat=0
    while cap.isOpened():
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            break

        cv2.imshow('Video Playback', cv2.cvtColor(frame, cv2.COLOR_RGB2HSV))

        if cv2.waitKey(27) & 0xFF == ord('q'):
            repeat=1
            break
        
    if repeat:
        break

cap.release()
cv2.destroyAllWindows()