from bottle import Bottle, request
from PID import PID
import pickle
import numpy as np
import cv2

app = Bottle()

pid = PID()



@app.route('/recv_image', method='POST')
def receive_image():
    try:
        # Deserialize image data
        cx = pickle.loads(request.body.read())
        ##### PID #########
        pid.update(cx)
        output = pid.output
        output = format(output, '.4f')
        print ("result to send back:", output)
        # Return any response (optional)
        return output
    except Exception as e:
        print("Error occurred while processing image:", str(e))
        return "Error processing image"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


