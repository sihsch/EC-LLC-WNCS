import cv2
import time
import numpy as np 

class imgProcessing:

    def __init__(self):

        self.clear()

    def clear(self):

        self.cx = 0.0
        self.cy = 0.0
        self.d = 0

    def img_processing(self,frame):


        #lowbound_img = frame[0:120, 0:160]
        
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)
        ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)
        # Find the contours of the frame
        contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

        #Check to see if any contours is capchaded
        if len(contours) > 0:
        	
            print ("on site")
            self.d = 0

            # Getting the center
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            if M["m00"] != 0:
                self.cx  = int(M["m10"] / M["m00"])
                self.cy = int(M["m01"] / M["m00"])
            else:
                # set values as what you need in the situation
                self.cx , self.cy = 160, 80

        else:
            self.d = 80
            print ("Out of site:")
