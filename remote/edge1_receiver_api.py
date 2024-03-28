from bottle import Bottle, request
from imgProcessing import imgProcessing
from PID import PID
import pickle
import numpy as np
import cv2

app = Bottle()

pid = PID()
img = imgProcessing()



@app.route('/recv_image', method='POST')
def receive_image():
    try:
        # Deserialize image data
        image_data = pickle.loads(request.body.read())
        # Decode image

        M = cv2.moments(image_data)
        if M["m00"] != 0:
            cx  = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
        else:
            # set values as what you need in the situation
            cx, cy = 160, 120
   
        ##### PID #########
        pid.update(cx)
        output = pid.output
        output = format(output, '.4f')
        print ("result to send back:", output)
        #serialized_dict = pickle.dumps(c)

        #cv2.imshow("Received Image", frame)
        #cv2.waitKey(1)
        # Return any response (optional)
        return output
    except Exception as e:
        print("Error occurred while processing image:", str(e))
        return "Error processing image"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


