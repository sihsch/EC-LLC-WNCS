from imgProcessing import imgProcessing
from PID import PID
import sys
import time
import zmq
import traceback
import pickle
import cv2
import numpy as np 
context = zmq.Context()
socket = context.socket(zmq.REP)


img = imgProcessing()
pid = PID()

image_count = 0
processing_time_list = []
deviation_list = []
looptime_list = []


def cal_average(processing_time):
    sum_num = 0
    for t in processing_time:
        sum_num = sum_num + t
    if len(processing_time) != 0:
        avg = sum_num / len(processing_time)
        return avg
    else:
        return 0

try:
    with socket.bind("tcp://*:5554"):
        while True:
            t = time.time()
            message = socket.recv()
            jibu = pickle.loads(message)
            image= jibu[0]
            index =jibu[1]

            image_count += 1  # count all images received
            t2 = time.time()

            ###########imageprocessing#####################
            
            img.img_processing(image)
            cx = img.cx
            
            ############## deviation calculation##############
            d = img.d
            if d == 0:
                dev = cx - 80
                dev_abs  = abs (dev)
                deviation_list.append(dev_abs)
            else:
                deviation_list.append(d)

            ##### PID #########
            pid.update(cx)
            output = pid.output
            output = format(output, '.4f')
            processing_time = time.time()-t2
            processing_time_list.append(processing_time)
            c = []
            c.append(index)
            c.append (output)
            serialized_dict = pickle.dumps(c)
            
            socket.send(serialized_dict)

            looptime = time.time()-t
            looptime_list.append(looptime) 
            
except (KeyboardInterrupt, SystemExit):
    print ("Total number image capture and processed: ", len(deviation_list))
    print ("The average deviation value is : ",cal_average(deviation_list))
    print ("Total number of loops the experiment runs (time.time()): ", len(processing_time_list))
    print ("The average time (time.time()) for a single loop execution is: ",cal_average(processing_time_list))

    
    pass
except Exception as ex:
    print('Python error with no Exception handler:')
    print('Traceback error:', ex)
    traceback.print_exc()
finally:

     print ("Total number image capture and processed: ", len(deviation_list))
     print ("The average deviation value is : ",cal_average(deviation_list))
     print ("Total number of loops the experiment runs (time.time()): ", len(processing_time_list))
     print ("The average time (time.time()) for a single loop execution is: ",cal_average(processing_time_list))
     input()
         
     with open("remote_3G.txt", 'a') as f:
         f.write("received_img:  " + str(image_count) + " deviation:  " + str(cal_average(deviation_list)) + " processing_time:  " + str(cal_average(processing_time_list))+ " looptime_time:  " + str(cal_average(looptime_list))+ "\n")
         f.close()         
     sys.exit()
