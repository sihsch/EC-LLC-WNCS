from AlphaBot2 import AlphaBot2
import sys
import time
import cv2
import zmq
import argparse


ap = argparse.ArgumentParser()
ap.add_argument("-ip", required=True,
	help="IP address of the server is required")
args = vars(ap.parse_args())


maximum = 13
Ab = AlphaBot2()

deviation_list = []
time_list = []


def cal_average(time_list):
    return sum(time_list) / len(time_list)



rawCapture = cv2.VideoCapture(0)
time.sleep(2)
rawCapture.set(3, 160)
rawCapture.set(4, 128)


context = zmq.Context()
print("Connecting to server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://{}:5554".format(args['ip']))
#socket.connect("tcp://192.168.108.153:5554")


image_captured = 0
image_sent = 0
image_skipped = 0
threshold = 5
last_feature = 0

try:
    while True:
        t = time.time()

        ret, image = rawCapture.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)
        contours, hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

        if len(contours) > 0:
            image_captured += 1
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)

            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
            else:
                cx = 160

            setpoint = 80
            deviation = abs(cx - setpoint)
            feature_deviation = abs(cx - last_feature)
            last_feature = cx

            deviation_list.append(deviation)

            if feature_deviation >= threshold:
                image_sent += 1
                cx_str = str(cx)
                cx_bytes = cx_str.encode('utf-8')

                socket.send(cx_bytes)
                reply_from_server = socket.recv()
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
                image_skipped += 1
                continue

        deviation_list.append(80)
        elapsed_time = time.time() - t
        time_list.append(elapsed_time)

except (KeyboardInterrupt, SystemExit):
    Ab.stop()
    print ("threshold: " + str(threshold) + "  image_captured: "+ str(image_captured)+ "  image_sent: "+ str(image_sent)+ "  image_skipped: "+ str(image_skipped)+ "  deviation: " + str(cal_average(deviation_list)))
    input ()
    with open("ad2_5G_Pro_tm.txt", 'a') as f:
        f.write(str(threshold) +"  image_captured: "+ str(image_captured)+ "  image_sent: "+ str(image_sent)+ "  image_skipped: "+ str(image_skipped)+ "  deviation: " + str(cal_average(deviation_list))+"\n")
        f.close()
    pass
except Exception as ex:
    print('Python error with no Exception handler:')
    print('Traceback error:', ex)
    traceback.print_exc()
finally:
    Ab.stop()
    sys.exit()
