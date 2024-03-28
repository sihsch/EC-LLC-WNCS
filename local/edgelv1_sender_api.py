from AlphaBot2 import AlphaBot2
import threading
import requests
import pickle
import time
import cv2
import argparse


ap = argparse.ArgumentParser()
ap.add_argument("-ip", required=True,
	help="IP address of the server is required")
args = vars(ap.parse_args())



# Function to continuously capture and send images
def send_images(server_url):
    # Set up camera
    rawCapture = cv2.VideoCapture(0)
    time.sleep(2)
    rawCapture.set(3, 160)
    rawCapture.set(4, 128)
    maximum = 13
    Ab = AlphaBot2()

    try:
        while True:
            t = time.time()
            ret, image = rawCapture.read()
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)
            contours, hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

            if len(contours) > 0:
                c = max(contours, key=cv2.contourArea)
                serialized_dict = pickle.dumps(c)

                # Send image data to server
                response = requests.post(f"{server_url}/recv_image", data=serialized_dict)
                if response.status_code == 200:
                    print("Server response:", float(response.text) )
                else:
                    print("Error:", response.status_code)
                command_recv_time = time.time() - t
                print("Command receive time:", command_recv_time)
                
                power_difference = float(response.text)
        
                #Ab.forward()
                if (power_difference > maximum):
                    power_difference = maximum
        
                if (power_difference < - maximum):
                    power_difference = - maximum
        
                # Manoeuvring the alphabot
                if (power_difference < 0):
                    #print("turn left")
                    Ab.setPWMA(maximum + power_difference )
                    Ab.setPWMB(maximum)
                else:
                    #print("turn right")
                    Ab.setPWMA(maximum)
                    Ab.setPWMB(maximum - power_difference )            
            
            
    except KeyboardInterrupt:
        Ab.stop()
        print("KeyboardInterrupt detected. Exiting.")
    finally:
        Ab.stop()
        rawCapture.release()

if __name__ == '__main__':
    # URL of the server
    #server_url = "http://192.168.1.72:8080"  # Replace with the server's IP address # 114.71.220.145
    server_url = "http://{}:8080".format(args['ip'])

    # Create and start a thread for sending images
    image_thread = threading.Thread(target=send_images, args=(server_url,))
    image_thread.start()
