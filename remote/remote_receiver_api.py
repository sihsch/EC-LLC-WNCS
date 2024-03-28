from bottle import Bottle, request
from imgProcessing import imgProcessing
from PID import PID
import numpy as np
import pickle
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
        frame = cv2.imdecode(np.frombuffer(image_data, dtype=np.uint8), cv2.IMREAD_COLOR)
        # Process the received image here (e.g., perform image processing, etc.)
        # You can send back a response to the client if needed
        # For now, let's just print the received image

        ###########imageprocessing#####################
        img.img_processing(frame)
        cx = img.cx
        
        ############## deviation calculation##############
        d = img.d

        ##### PID #########
        pid.update(cx)
        output = pid.output
        output = format(output, '.4f')
        print ("result to send back:", output)
        #serialized_dict = pickle.dumps(c)

        cv2.imshow("Received Image", frame)
        cv2.waitKey(1)
        # Return any response (optional)
        return output
    except Exception as e:
        print("Error occurred while processing image:", str(e))
        return "Error processing image"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


