from AlphaBot2 import AlphaBot2
import sys
import time
import traceback
import cv2
import zmq
import pickle
import argparse


ap = argparse.ArgumentParser()
ap.add_argument("-ip", required=True,
	help="IP address of the server is required")
args = vars(ap.parse_args())

maximum = 13
Ab = AlphaBot2()

rawCapture = cv2.VideoCapture(0)
time.sleep(2)
rawCapture.set(3, 160)
rawCapture.set(4, 120)

deviation_list = []
command_recv_time_list = []
data_processing_time_list = []
transmission_time_list = []
loop_time_list = []

def cal_average(time_list):
    if len(time_list) != 0:
        return sum(time_list) / len(time_list)
    else:
        return 0

context = zmq.Context()
print("Connecting to server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://{}:5554".format(args['ip']))

#socket.connect("tcp://192.168.108.153:5554")

try:
    while True:
        t = time.time()
        t2 = time.process_time()

        ret, image = rawCapture.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)
        contours, hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            serialized_dict = pickle.dumps(M)
            processing_time = time.time() - t
            data_processing_time_list.append(processing_time)

            socket.send(serialized_dict)
            reply_from_server = socket.recv()

            command_recv_time = time.time() - t
            outsidetime = time.process_time() - t2
            transmission_time = command_recv_time - outsidetime
            transmission_time_list.append(transmission_time)
            command_recv_time_list.append(command_recv_time)

            reply_as_string = reply_from_server.decode('utf-8')
            power_difference = float(reply_as_string)

            Ab.forward()
            power_difference = max(min(power_difference, maximum), -maximum)

            if power_difference < 0:
                Ab.setPWMA(maximum + power_difference)
                Ab.setPWMB(maximum)
            else:
                Ab.setPWMA(maximum)
                Ab.setPWMB(maximum - power_difference)
        else:
            d = 80
            deviation_list.append(abs(d))

        loop_time = time.time() - t
        loop_time_list.append(loop_time)

except (KeyboardInterrupt, SystemExit):
    Ab.stop()
    pass
except Exception as ex:
    print('Python error with no Exception handler:')
    print('Traceback error:', ex)
    traceback.print_exc()
finally:
    Ab.stop()
    print("Total number of images processed:", len(command_recv_time_list))
    print("The average loop processing time is:", cal_average(command_recv_time_list))
    print("Total number of images processed:", len(data_processing_time_list))
    print("The average processing time is:", cal_average(data_processing_time_list))
    input()

    with open("edgelv2_3G.txt", 'a') as f:
        f.write("image: " + str(len(transmission_time_list)) + " looptime: " + str(cal_average(loop_time_list)) + " command_recv_time: " + str(cal_average(command_recv_time_list)) + " data_processing_time: " + str(cal_average(data_processing_time_list)) + " transmission_time: " + str(cal_average(transmission_time_list)) + "\n")

    sys.exit()
