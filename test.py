import cv2

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()

    cv2.imshow("Webcam Video Output", frame)
    k = cv2.waitKey(100)
    if k == 27:
        break
    cv2.destroyAllWindows()