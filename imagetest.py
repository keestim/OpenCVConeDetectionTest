# importing cv2 
import cv2
from time import sleep
  
# path
path = r'./RGB_Source.png'
  
# Using cv2.imread() method
img = cv2.imread(path)

    # Displaying the image
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
