from AlphaBot2 import AlphaBot2
import sys
import time
import traceback
import cv2
from imutils.video import VideoStream
import zmq
import pickle


maximum = 13
Ab = AlphaBot2()

rawCapture = cv2.VideoCapture(0)
time.sleep(2)
rawCapture.set(3, 160)
rawCapture.set(4, 120)
deviation = 0
last_feature = 0

deviation_list = []
time_list = []
processing_time = []

command_recv_time_list = []
data_processing_time_list = []
transmition_time_list = []
looptime_list = []



def cal_average(time_list):
    sum_num = 0
    for t in time_list:
        sum_num = sum_num + t
    if len(time_list) != 0:
        avg = sum_num / len(time_list)
        return avg
    else:
        return 0


context = zmq.Context()
print("Connecting to server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://192.168.108.153:5554")


try:
    while True:  # send images as stream until Ctrl-C

        t = time.time()
        t2 = time.time()
        t3 = time.process_time()

        ret, image = rawCapture.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)
        # Find the contours of the frame
        contours, hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            serialized_dict = pickle.dumps(M)
            processingtime = time.time()-t
            data_processing_time_list.append(processingtime)

            socket.send(serialized_dict)
            reply_from_server = socket.recv()

            command_recv_time = time.time()-t2
            outsidetime = time.process_time() - t3
            transmition_time = command_recv_time - outsidetime
            transmition_time_list.append(transmition_time)
            command_recv_time_list.append(command_recv_time)


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
            #cv2.line(image, (cx, 0), (cx, 720), (255, 0, 0), 1)
            #cv2.line(image, (0, cy), (1280, cy), (255, 0, 0), 1)
            #cv2.drawContours(image, contours, -1, (0, 255, 0), 1)
        else:
            d = 80
            deviation_list.append(abs(d))
            
        looptime = time.time() - t
        looptime_list.append(looptime)            

        #cv2.putText(image, str(deviation), (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        #cv2.imshow("path", image)
        #if cv2.waitKey(1) & 0xFF == ord('q'):
            #break
except (KeyboardInterrupt, SystemExit):
    Ab.stop()
    print ("Total number image processed: ", len(command_recv_time_list))
    print ("The average loop processing time is : ",cal_average(command_recv_time_list))
    print ("Total number image  processed: ", len(data_processing_time_list))
    print ("The average processing time is : ",cal_average(data_processing_time_list))
    input ()

    #with open("edgelv2_dev.txt", 'a') as f:
        #f.write(str(len(data_processing_time_list)) +"  "+ str(cal_average(data_processing_time_list))+ "\n")
        #f.close()


    with open("edgelv2_3G.txt", 'a') as f:
        f.write("image: "+ str(len(transmition_time_list))+ " looptime: " + str(cal_average(looptime_list)) + " command_recv_time: " + str(cal_average(command_recv_time_list)) + " data_processing_time: " + str(cal_average(data_processing_time_list)) + " transmition_time: " + str(cal_average(transmition_time_list))+ "\n")
        f.close()        
    pass  # Ctrl-C was pressed to end program
except Exception as ex:
    print('Python error with no Exception handler:')
    print('Traceback error:', ex)
    traceback.print_exc()
finally:
    Ab.stop()

    #picam.stop()  # stop the camera thread
    #sys.exit()