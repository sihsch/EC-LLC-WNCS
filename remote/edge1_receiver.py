import sys
from PID import PID
import zmq
import traceback
import pickle
import cv2
import time
import numpy as np 

context = zmq.Context()
socket = context.socket(zmq.REP)


Feature_count = 0
pid = PID()
deviation_list = []
processing_time_list = []
looptime_list =[]

def cal_average(time_list):
    if len(time_list) == 0:
        return 0  
    else:
        return sum(time_list) / len(time_list)
        
        
try:
    with socket.bind("tcp://*:5554"):
        while True:
            t = time.time()
            message = socket.recv()
            t2 = time.time()
            #cntrv = len(message)
            #print('size of the receiver feature is: {:,g} bytes'.format(cntrv))
            Feature_count += 1  # count all images received            
            c = pickle.loads(message)
            M = cv2.moments(c)
            if M["m00"] != 0:
                cx  = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            else:
                # set values as what you need in the situation
                cx, cy = 160, 120
            #print("recevd value: ", cx)
            spoint = 80
            deviation = cx - spoint
            deviation_list.append(abs(deviation))


            ##### PID #########
            pid.update(cx)
            output = pid.output
            output = format(output, '.4f')

            ########## convert to bytes #################
            # convert the number to a string
            # convert the string to bytes and send it to mobile robot
            num_as_string = str(output)  
            bytes_val = num_as_string.encode()  
            cntrv2 = len(bytes_val)
            #print('size of sent control value is: {:,g} bytes'.format(cntrv2))
            processing_time = time.time()-t2
            processing_time_list.append(processing_time)
           
            socket.send(bytes_val)
            looptime = time.time()-t
            looptime_list.append(looptime)            


except (KeyboardInterrupt, SystemExit):
    print ("Total number of loops the experiment runs (time.time()): ", len(time_list))
    print ("The average time (time.time()) for a single processing is: ",cal_average(time_list))
    print ("Total number of loops the experiment runs (time.time()): ", len(timeloop_list))
    print ("The average time (time.time()) for a single loop execution is: ",cal_average(timeloop_list))
    print ("Total number of deviation points: ", len(deviation_list))
    print ("The average deviation offset is :  ",cal_average(deviation_list))
    print ("Number of features received: ", Feature_count)

    pass
except Exception as ex:
    print('Python error with no Exception handler:')
    print('Traceback error:', ex)
    #traceback.print_exc()
finally:
    print()
    print('Test Program: ', __file__)
    print('Total Number of Images received: {:,g}'.format(Feature_count))
    print ("Total number of loops the experiment runs (time.time()): ", len(processing_time_list))
    print ("The average time (time.time()) for a single loop execution is: ",cal_average(processing_time_list))
    input()
    with open("Edge_lv1_3G.txt", 'a') as f:
        f.write("received_img:  " + str(Feature_count) + " deviation:  " + str(cal_average(deviation_list)) + " processing_time:  " + str(cal_average(processing_time_list))+ " looptime_time:  " + str(cal_average(looptime_list))+ "\n")
        f.close()
    sys.exit()
