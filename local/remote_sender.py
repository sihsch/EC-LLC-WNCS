from AlphaBot2 import AlphaBot2
import sys
import time
import traceback
import cv2
from imutils.video import VideoStream
import imagezmq
import numpy as np
import sys
import pickle
import zmq
import argparse


ap = argparse.ArgumentParser()
ap.add_argument("-ip", "--InternetProtocol", required=True,
	help="IP address of the server is required")
args = vars(ap.parse_args())

rawCapture = cv2.VideoCapture(0)
time.sleep(2)
rawCapture.set(3, 160)
rawCapture.set(4, 128)
maximum = 13
Ab = AlphaBot2()


command_recv_time_list = []
data_processing_time_list = []
data_transmition_time_list = []
looptime_list = []
image_serial = []
i = 0


def cal_average(time_list):
    if len(time_list) == 0:
        return 0  
    else:
        return sum(time_list) / len(time_list)



context = zmq.Context()
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
#socket.connect("tcp://192.168.108.153:5554")
socket.connect("tcp://{}:5554".format(args['ip']))

try:
    while True:
        t = time.time()
        t2 = time.process_time()
        ret, image = rawCapture.read()
        i += 1
        serialized_dict = pickle.dumps([image,i])
        socket.send(serialized_dict)
        reply_from_server = socket.recv()
        command_recv_time = time.time()-t

        c = pickle.loads(reply_from_server)
        index , command = c


        command_recv_time = time.time()-t
        outsidetime = time.process_time() - t2
        transmition_time = command_recv_time - outsidetime
        data_transmition_time_list.append(transmition_time)
        command_recv_time_list.append(command_recv_time)

        #reply_as_string = reply_from_server.decode('utf-8')  # decode from bytes to Python 3 string
        power_difference = float(command)

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


        looptime = time.time()-t
        looptime_list.append(looptime)


except (KeyboardInterrupt, SystemExit):
    Ab.stop()
    pass  # Ctrl-C was pressed to end program
except Exception as ex:
    print('Python error with no Exception handler:')
    print('Traceback error:', ex)
    traceback.print_exc()
finally:
    Ab.stop()
    print ("Total number of loops the experiment runs (time.process): ", i)
    print ("The average time (time.process) for a single loop execution is: ",cal_average(looptime_list))
    print ("Total number of loops the experiment runs (time.time()): ", len(command_recv_time_list))
    print ("The average time (time.time()) for command recv time is: ",cal_average(command_recv_time_list))
    print ("The average time (time.time()) for data transmition time is: ",cal_average(data_transmition_time_list))
    input ()
    with open("remote_3G.txt", 'a') as f:
        f.write("Number_of_image: " + str(i)+ " looptime: " + str(cal_average(looptime_list)) + " command_recv_time: " + str(cal_average(command_recv_time_list)) + " data_transmition_time: " + str(cal_average(data_transmition_time_list))+ "\n")
        f.close()
    sys.exit()