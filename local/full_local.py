from AlphaBot2 import AlphaBot2
import time
import cv2

Ab = AlphaBot2()
maximum = 13
integral = 0
last_proportional = 0

rawCapture = cv2.VideoCapture(0)
time.sleep(2)
rawCapture.set(3, 160)
rawCapture.set(4, 120)

time_list = []
dataprocessing_time = []
deviation_list = []
singleloop_time =[]


def cal_average(time_list):
    return sum(time_list) / len(time_list)
    
try:
    while True:
        t = time.time()
        
        ret, frame = rawCapture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)
        # Find the contours of the frame
        contours, hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)
        # Check to see if any contours is capchaded
        if len(contours) > 0:
            # Getting the center
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            if M["m00"] != 0:
                cx  = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            else:
                cx = 160
            setpoint = 80
            ##### PID #########
            proportional = cx - setpoint
            pro = abs(proportional)
            deviation_list.append(pro)
            
            derivative = proportional - last_proportional
            integral += proportional
            last_proportional = proportional
            
            power_difference = proportional / 10 + integral / 100000 + derivative * 0.65
            dataprocessingtime= time.time()-t
            dataprocessing_time.append(dataprocessingtime)
            
            Ab.forward()

            power_difference = max(min(power_difference, maximum), -maximum)

            # Manoeuvring the alphabot
            if (power_difference < 0):
                #print ("turn left")
                Ab.setPWMA(maximum + power_difference)
                Ab.setPWMB(maximum)
            else:
                #print ("turn right")
                Ab.setPWMA(maximum)
                Ab.setPWMB(maximum - power_difference)
        else:
            deviation_list.append(80)
            #cx, pro= 00 ,80

        singlelooptime= time.time()-t
        singleloop_time.append(singlelooptime)

except (KeyboardInterrupt, SystemExit):
    Ab.stop()
    print("Total number of image captures and processed:", len(deviation_list))
    print("The average deviation value is:", cal_average(deviation_list))
    print("Total number of loops the experiment runs (time.time()):", len(singleloop_time))
    print("The average time (time.time()) for a single loop execution is:", cal_average(singleloop_time))
    print("Total number of loops the experiment runs (time.time()):", len(dataprocessing_time))
    print("The average time (time.time()) for processing time is:", cal_average(dataprocessing_time))
    input()
    
    with open("pi3_Floc_singleloop.txt", 'a') as f:
        f.write("Singleloop_time " + str(len(singleloop_time)) + " " + str(cal_average(singleloop_time)) + "\n")
    
    with open("pi3_Floc_pro.txt", 'a') as f:
        f.write("Data_Processing_time " + str(len(dataprocessing_time)) + " " + str(cal_average(dataprocessing_time)) + "\n")
    
    with open("pi3_Floc_deviation.txt", 'a') as f:
        f.write("Data_Processing_time " + str(len(deviation_list)) + " " + str(cal_average(deviation_list)) + "\n")
        
    pass

finally:
    Ab.stop()
