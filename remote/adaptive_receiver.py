import sys
from PID import PID
import time
import zmq


context = zmq.Context()
socket = context.socket(zmq.REP)


Feature_count = 0
pid = PID()


time_list = []


def cal_average(time_list):
    sum_num = 0
    for t in time_list:
        sum_num = sum_num + t
    avg = sum_num / len(time_list)
    return avg

try:
    with socket.bind("tcp://*:5554"):
        while True:
            message = socket.recv()
            t = time.time()
            cntrv = len(message)
            #print('size of the receiver feature is: {:,g} bytes'.format(cntrv))
            
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
            
            socket.send(bytes_val)
            elapsed_time = time.time()-t
            time_list.append(elapsed_time)


            
except (KeyboardInterrupt, SystemExit):
    print ("Total number of loops the experiment runs (time.time()): ", len(time_list))
    print ("The average time (time.time()) for a single loop execution is: ",cal_average(time_list))
    print ("Number of features received: ", Feature_count)
    pass
except Exception as ex:
    print('Python error with no Exception handler:')
    print('Traceback error:', ex)
    #traceback.print_exc()
finally:
    print()
    input()
    with open("serve_ad_pro_3G.txt", 'a') as f:
        f.write(str(Feature_count)+ " " +str(cal_average(time_list))+ "\n")
        f.close()
    sys.exit()
