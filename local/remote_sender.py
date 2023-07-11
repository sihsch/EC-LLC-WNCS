from AlphaBot2 import AlphaBot2
import sys
import time
import traceback
import cv2
import pickle
import zmq

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
    if len(time_list) != 0:
        return sum(time_list) / len(time_list)
    else:
        return 0

context = zmq.Context()
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://192.168.108.153:5554")

try:
    while True:
        t = time.time()
        t2 = time.time()
        t3 = time.process_time()
        
        ret, image = rawCapture.read()
        i += 1
        serialized_dict = pickle.dumps([image,i])
        socket.send(serialized_dict)
        reply_from_server = socket.recv()
        command_recv_time = time.time()-t2
        
        c = pickle.loads(reply_from_server)
        index , command = c


        command_recv_time = time.time()-t
        outsidetime = time.process_time() - t3
        transmition_time = command_recv_time - outsidetime
        data_transmition_time_list.append(transmition_time)
        command_recv_time_list.append(command_recv_time)

        power_difference = float(command)

        Ab.forward()
        power_difference = max(min(power_difference, maximum), -maximum)

        # Manoeuvring the alphabot
        if (power_difference < 0):
            Ab.setPWMA(maximum + power_difference )
            Ab.setPWMB(maximum)
        else:
            Ab.setPWMA(maximum)
            Ab.setPWMB(maximum - power_difference )
            
            
        looptime = time.time()-t
        looptime_list.append(looptime)


except (KeyboardInterrupt, SystemExit):
    Ab.stop()
    pass
except Exception as ex:
    print('Python error with no Exception handler:')
    print('Traceback error:', ex)
    traceback.print_exc()
finally:
    Ab.stop()
    print("Total number of loops the experiment runs (time.process): ", i)
    print("The average time (time.process) for a single loop execution is: ", cal_average(loop_time_list))
    print("Total number of loops the experiment runs (time.time()): ", len(command_recv_time_list))
    print("The average time (time.time()) for command receive time is: ", cal_average(command_recv_time_list))
    print("The average time (time.time()) for data transmission time is: ", cal_average(data_transmission_time_list))
    input()
    
    with open("remote_3G.txt", 'a') as f:
        f.write("Number_of_image: " + str(i) + " looptime: " + str(cal_average(loop_time_list)) + " command_recv_time: " + str(cal_average(command_recv_time_list)) + " data_transmission_time: " + str(cal_average(data_transmission_time_list)) + "\n")
    
    sys.exit()
