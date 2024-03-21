import sys
from PID import PID
import time
import zmq
import traceback
import pickle
context = zmq.Context()
socket = context.socket(zmq.REP)


Feature_count = 0
pid = PID()

looptime_list = []
processing_time_list = []

deviation_list = []
time_list = []


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
            M = pickle.loads(message)
            
            if M["m00"] != 0:
                cx  = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            else:
                # set values as what you need in the situation
                cx, cy = 160, 120
                     
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
    print ("Total number of loops the experiment runs (time.time()): ", len(looptime_list))
    print ("The average time (time.time()) for a single loop execution is: ",cal_average(looptime_list))
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
    
    print ("Total number of loops the experiment runs (time.time()): ", len(looptime_list))
    print ("The average time (time.time()) for a single loop execution is: ",cal_average(looptime_list))
    print ("Total number of loops the experiment runs (time.time()): ", len(processing_time_list))
    print ("The average time (time.time()) for a single loop execution is: ",cal_average(processing_time_list))
    input()
       
    with open("Edge_lv2_3G.txt", 'a') as f:
        f.write("received_img:  " + str(Feature_count) + " deviation:  " + str(cal_average(deviation_list)) + " processing_time:  " + str(cal_average(processing_time_list))+ " looptime_time:  " + str(cal_average(looptime_list))+ "\n")
        f.close()        
    print('Test Program: ', __file__)
    sys.exit()
