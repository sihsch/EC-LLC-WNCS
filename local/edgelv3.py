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

command_recv_time_list = []
data_processing_time_lv1 = []
data_processing_time_lv2 = []
data_processing_time_lv3 = []
transmition_time_list = []
looptime_list = []


#image_serial = []
#i = 0

def cal_average(time_list):
    sum_num = 0
    for t in time_list:
        sum_num = sum_num + t
    avg = sum_num / len(time_list)
    return avg

context = zmq.Context()
print("Connecting to server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://192.168.108.153:5554")


try:
    while True:

        t = time.time()
        t2 = time.time()
        t3 = time.process_time()

        ret, image = rawCapture.read()
        #i  +=1
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)
        contours, hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

        # Check to see if any contours is capchaded
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            serialized_dict = pickle.dumps(c)
            processingtime1 = time.time()-t2
            data_processing_time_lv1.append(processingtime1)
            
            M = cv2.moments(c)
            serialized_dict2 = pickle.dumps(M)
            
            processingtime2 = time.time()-t2
            data_processing_time_lv2.append(processingtime2)             
            if M["m00"] != 0:
                cx  = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            else:
                # set values as what you need in the situation
                cx, cy = 160, 120

            setpoint = 80
            deviation = cx - setpoint
            deviation_list.append(abs(deviation))

            cxxx= str(cx)
            cxx =cxxx.encode('utf-8')

            #size = sys.getsizeof(cxx)
            #print (size)
            processingtime = time.time()-t2
            data_processing_time_lv3.append(processingtime)

            socket.send(cxx)
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
    print ("Total number image capture and processed: ", len(deviation_list))
    print ("The average deviation value is : ",cal_average(deviation_list))   
    print ("The average time (time.time()) for a single loop execution is: ",cal_average(command_recv_time_list))
    print ("The average time (time.time()) for command_recv_time is: ",cal_average(command_recv_time_list))
    print ("The average time (time.time()) for data_processing_time is: ",cal_average(data_processing_time_lv3))
    print ("Total number of loops the experiment runs (time.time()): ", len(transmition_time_list))
    print ("The average time (time.time()) for transmition_time is: ",cal_average(transmition_time_list))
    input ()
    with open("processing_time_5G.txt", 'a') as f:
        f.write(str(len(data_processing_time_lv1)) + " processing_time lv1: " +str(cal_average(data_processing_time_lv1))+ " processing_time lv2: " +str(cal_average(data_processing_time_lv2))+" processing_time lv3: " +str(cal_average(data_processing_time_lv3))+ "\n")
        f.close()
    with open("edgelv3_5G.txt", 'a') as f:
        f.write("looptime: " + str(cal_average(looptime_list)) + " command_recv_time: " + str(cal_average(command_recv_time_list)) + " data_processing_time: " +str(cal_average(data_processing_time_lv3)) + " transmition_time: " + str(cal_average(transmition_time_list))+ " deviation: " + str(cal_average(deviation_list))+ "\n")
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