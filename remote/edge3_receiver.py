import sys
from PID import PID
import time
import zmq
import traceback


context = zmq.Context()
socket = context.socket(zmq.REP)

Feature_count = 0
pid = PID()
processing_time_list = []
looptime_list = []


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
            Feature_count += 1  # count all images received            
            cx = int(message.decode('utf-8'))
            
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
            

            looptime_time = time.time()-t
            looptime_list.append(looptime_time)

except (KeyboardInterrupt, SystemExit):
    print ("Total number of loops the experiment runs (time.time()): ", len(looptime_list))
    print ("The average time (time.time()) for a single loop execution is: ",cal_average(looptime_list)) 
    print ("Total number of loops the experiment runs (time.time()): ", len(processing_time_list))
    print ("The average time (time.time()) for a single loop execution is: ",cal_average(processing_time_list)) 
    print ("Number of features received: ", Feature_count)
    #pass
    
except Exception as ex:
    print('Python error with no Exception handler:')
    print('Traceback error:', ex)
    traceback.print_exc()
    
finally:
    print()
    print ("Total number of loops the experiment runs (time.time()): ", len(looptime_list))
    print ("The average time (time.time()) for a single loop execution is: ",cal_average(looptime_list)) 
    print ("Total number of loops the experiment runs (time.time()): ", len(processing_time_list))
    print ("The average time (time.time()) for a single loop execution is: ",cal_average(processing_time_list)) 
    input()
    with open("Edge_lv3_5G.txt", 'a') as f:
        f.write("received_img:  " + str(Feature_count) + " processing_time:  " + str(cal_average(processing_time_list))+ " looptime_time:  " + str(cal_average(looptime_list))+ "\n")
    sys.exit()
