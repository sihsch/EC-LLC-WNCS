from AlphaBot2 import AlphaBot2
import sys
import time
import traceback
import cv2
import zmq
import pickle
import argparse


ap = argparse.ArgumentParser()
ap.add_argument("-ip", "--InternetProtocol", required=True,
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
            serialized_dict1 = pickle.dumps(c)
            processing_time_lv1 = time.time() - t
            data_processing_time_lv1.append(processing_time_lv1)
            
            serialized_dict2 = pickle.dumps(M)
            processing_time_lv2 = time.time() - t
            data_processing_time_lv2.append(processing_time_lv2)
            
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            else:
                cx, cy = 160, 120

            setpoint = 80
            deviation = cx - setpoint
            deviation_list.append(abs(deviation))

            cx_str = str(cx)
            cx_bytes = cx_str.encode('utf-8')

            processing_time_lv3 = time.time() - t
            data_processing_time_lv3.append(processing_time_lv3)

            socket.send(cx_bytes)
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
    print("Total number of images captured and processed:", len(deviation_list))
    print("The average deviation value is:", cal_average(deviation_list))
    print("The average time for command receive is:", cal_average(command_recv_time_list))
    print("The average time for data processing (level 1) is:", cal_average(data_processing_time_lv1))
    print("The average time for data processing (level 2) is:", cal_average(data_processing_time_lv2))
    print("The average time for data processing (level 3) is:", cal_average(data_processing_time_lv3))
    print("Total number of loops the experiment runs:", len(transmission_time_list))
    print("The average time for transmission is:", cal_average(transmission_time_list))
    input()

    with open("processing_time_5G.txt", 'a') as f:
        f.write("processing_time_lv1: " + str(cal_average(data_processing_time_lv1)) + " processing_time_lv2: " + str(cal_average(data_processing_time_lv2)) + " processing_time_lv3: " + str(cal_average(data_processing_time_lv3)) + "\n")

    with open("edgelv3_5G.txt", 'a') as f:
        f.write("looptime: " + str(cal_average(loop_time_list)) + " command_recv_time: " + str(cal_average(command_recv_time_list)) + " data_processing_time: " + str(cal_average(data_processing_time_lv3)) + " transmission_time: " + str(cal_average(transmission_time_list)) + " deviation: " + str(cal_average(deviation_list)) + "\n")

    sys.exit()
