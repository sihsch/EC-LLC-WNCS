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
rawCapture.set(4, 128)
deviation = 0
last_feature = 0
deviation_list = []

command_recv_time_list = []
data_processing_time_list = []
transmition_time_list = []
looptime_list = []

data_size = []

def cal_average(time_list):
    sum_num = 0
    for t in time_list:
        sum_num = sum_num + t
    if len(time_list) != 0:
        avg = sum_num / len(time_list)
        return avg
    else:
        return 0

def summ (data_size):
    sum_data = 0
    for t in data_size:
        sum_data = sum_data + t
    return sum_data
context = zmq.Context()
print("Connecting to hello world server…")
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
        contours, hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            serialized_dict = pickle.dumps(c)
            dataprocessingtime = time.time()-t2
            data_processing_time_list.append(dataprocessingtime)

            socket.send(serialized_dict)
            reply_from_server = socket.recv()

            command_recv_time = time.time()-t2
            outsidetime = time.process_time() - t3
            transmition_time = command_recv_time - outsidetime
            transmition_time_list.append(transmition_time)
            command_recv_time_list.append(command_recv_time)


            reply_as_string = reply_from_server.decode('utf-8')
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
            d = 80
            deviation_list.append(abs(d))
            
        looptime = time.time() - t
        looptime_list.append(looptime)


except (KeyboardInterrupt, SystemExit):
    Ab.stop()
    print ("Total number image capture and processed: ", len(deviation_list))
    print ("The average deviation value is : ",cal_average(deviation_list))
    print ("Total number of loops the experiment runs (time.time()): ", len(command_recv_time_list))
    print ("The average time (time.time()) for a single loop execution is: ",cal_average(command_recv_time_list))
    print ("Total number of loops the experiment runs (time.time()): ", len(data_processing_time_list))
    print ("The average time (time.time()) for processing image is: ",cal_average(data_processing_time_list))
    #print ("The average data size  value is : ",cal_average(data_size))
    input ()
    #with open("edgelv1_dev.txt", 'a') as f:
        #f.write(str(len(deviation_list)) +"  "+str(cal_average(deviation_list))+ "\n")
        #f.close()
    with open("edgelv1_3G.txt", 'a') as f:
        f.write("image: "+ str(len(data_processing_time_list))+" looptime: " + str(cal_average(looptime_list)) +  " command_recv_time: " + str(cal_average(command_recv_time_list)) + " data_processing_time: " +str(cal_average(data_processing_time_list)) + " transmition_time: " +str(cal_average(transmition_time_list))+ " deviation: " +str(cal_average(deviation_list))+ "\n")
        f.close()
    #with open("edge_lv1_dev_data_size.txt", 'a') as f:
        #f.write(str(summ (data_size)) +"  "+str(cal_average(data_size))+ "\n")
        #f.close()
    pass
except Exception as ex:
    print('Python error with no Exception handler:')
    print('Traceback error:', ex)
    traceback.print_exc()
finally:
    Ab.stop()