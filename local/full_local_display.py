from AlphaBot2 import AlphaBot2
import time
import cv2
import os
import csv


def lineTracker():
# def lineTracker(moveFunc):
    Ab = AlphaBot2()
    x_value = 0
    try:
        maximum = 11
        integral = 0
        last_proportional = 0
        #print("start recording...")
        rawCapture = cv2.VideoCapture(-1)
        time.sleep(2)
        rawCapture.set(3, 160)
        rawCapture.set(4, 128)
        while (True):
            x_value +=1
            #print("start getting frame...")
            ret, frame = rawCapture.read()
            #print ("the frame looks like this: ", frame)
            #print (frame.shape)
            # Convert the image to grayscale and apply a Gaussian
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0) #blur is to reduce noise in received image
            ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)
            # Show captured frame, draw conture line
            #print("start conture...")
            # Find the contours of the frame
            # contours is green line around the detected object
            contours, hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)
            # Check to see if any contours is capchaded
            if len(contours) > 0:
                # Getting the center
                c = max(contours, key=cv2.contourArea)
                M = cv2.moments(c)
                if M["m00"] != 0:
                    cx  = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                else:
                    # set values as what you need in the situation
                    cx , cy = 160, 80
                #cx = int(M['m10'] / M['m00'])
                #cy = int(M['m01'] / M['m00'])
                setpoint = 80
                ##### PID #########
                proportional = cx - setpoint
                derivative = proportional - last_proportional
                integral += proportional
                last_proportional = proportional
                power_difference = proportional /10 + integral/100000 + derivative * 0.65                 
                ######

                if (power_difference > maximum):
                    power_difference = maximum
                if (power_difference < - maximum):
                    power_difference = - maximum

                #print (cx , power_difference)
                #print("moving control ...")
                Ab.forward()
                # moveFunc()
                if (power_difference == 0):
                    #print ("go straight")
                    Ab.setPWMA(maximum)
                    Ab.setPWMB(maximum)
                    
                if (power_difference < 0):
                    #print ("turn left")
                    Ab.setPWMA(maximum + power_difference)
                    Ab.setPWMB(maximum)
                else:
                    #print ("turn right")
                    Ab.setPWMA(maximum)
                    Ab.setPWMB(maximum - power_difference)

                #print('showing contoure ...')
                cv2.line(frame, (cx, 0), (cx, 720), (255, 0, 0), 1)
                cv2.line(frame, (0, cy), (1280, cy), (255, 0, 0), 1)
                cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)
            else:
                print ("Out of Sight")
                cx = 160   
            ##########
              
            # put text top on image
            cv2.putText(frame, str(proportional), (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.imshow("path", frame)
                
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print('exit...')
                Ab.stop()
                rawCapture.release()
                cv2.destroyAllWindows()
                break
            
    except Exception as err:
        print("there is an err ", err)
    finally:
        Ab.stop()


if __name__ == "__main__":
    # main()
    lineTracker()
