from AlphaBot2 import AlphaBot2
import sys
import socket
import time
import cv2
from imutils.video import VideoStream
import zmq


maximum = 13
Ab = AlphaBot2()

skip =  0
last_feature = 0

deviation_list = []
time_list = []

def cal_average(time_list):
    sum_num = 0
    for t in time_list:
        sum_num = sum_num + t
    avg = sum_num / len(time_list)
    return avg


rawCapture = cv2.VideoCapture(0)
time.sleep(2)
rawCapture.set(3, 160)
rawCapture.set(4, 128)


context = zmq.Context()
#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://192.168.108.153:5554")

image_captured = 0
image_sent = 0
image_skipped = 0
threshold = 5

try:
    while True:  # send images as stream until Ctrl-C

        t = time.time()
        #image = picam.read()
        ret, image = rawCapture.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)
        # Find the contours of the frame
        contours, hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

        # Check to see if any contours is capchaded
        if len(contours) > 0:
            # Getting the center
            image_captured +=1
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            #print (M)
            #input()
            if M["m00"] != 0:
                cx  = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            else:
                # set values as what you need in the situation
                cx = 160

            setpoint = 80
            deviation = abs(cx - setpoint)
            feature_deviation = abs(cx - last_feature)
            last_feature = cx

            deviation_list.append(deviation)


            if feature_deviation >= threshold:
                image_sent +=1
                cxxx= str(cx)
                cxx =cxxx.encode('utf-8')
                #siz = sys.getsizeof(cxx)
                #print ("send size using getsizeoff: ", siz)
                socket.send(cxx)
                reply_from_server = socket.recv()
                #size3 = sys.getsizeof(reply_from_server)
                #print ("size using getsizeoff: ", size3)
                reply_as_string = reply_from_server.decode('utf-8')  # decode from bytes to Python 3 string
                power_difference = float(reply_as_string)
                Ab.forward()

                if (power_difference > maximum):
                    power_difference = maximum
                if (power_difference < - maximum):
                    power_difference = - maximum

                # Manoeuvring the alphabot
                if (power_difference < 0):
                    #print("turn left")
                    Ab.setPWMA(maximum + power_difference )
                    Ab.setPWMB(maximum)
                else:
                    #print("turn right")
                    Ab.setPWMA(maximum)
                    Ab.setPWMB(maximum - power_difference )

            else:
                image_skipped +=1
                continue

        deviation_list.append(80)
        elapsed_time = time.time()-t
        time_list.append(elapsed_time)

except (KeyboardInterrupt, SystemExit):
    Ab.stop()
    print ("threshold: " + str(threshold) + "  image_captured: "+ str(image_captured)+ "  image_sent: "+ str(image_sent)+ "  image_skipped: "+ str(image_skipped)+ "  deviation: " + str(cal_average(deviation_list)))
    input ()
    with open("ad2_5G_Pro_tm.txt", 'a') as f:
        f.write(str(threshold) +"  image_captured: "+ str(image_captured)+ "  image_sent: "+ str(image_sent)+ "  image_skipped: "+ str(image_skipped)+ "  deviation: " + str(cal_average(deviation_list))+"\n")
        f.close()
    pass
except Exception as ex:
    print('Python error with no Exception handler:')
    print('Traceback error:', ex)
    traceback.print_exc()
finally:
    Ab.stop()
    sys.exit()