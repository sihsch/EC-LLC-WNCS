from AlphaBot2 import AlphaBot2
import time
import cv2


def lineTracker():
    Ab = AlphaBot2()

    maximum = 11
    integral = 0
    last_proportional = 0

    rawCapture = cv2.VideoCapture(0)
    time.sleep(2)
    rawCapture.set(3, 160)
    rawCapture.set(4, 128)

    try:
        while True:
            ret, frame = rawCapture.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)

            contours, hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

            if len(contours) > 0:
                c = max(contours, key=cv2.contourArea)
                M = cv2.moments(c)
                cx = int(M["m10"] / M["m00"]) if M["m00"] != 0 else 160
                cy = int(M["m01"] / M["m00"]) if M["m00"] != 0 else 80
                setpoint = 80

                proportional = cx - setpoint
                derivative = proportional - last_proportional
                integral += proportional
                last_proportional = proportional
                power_difference = proportional / 10 + integral / 100000 + derivative * 0.65

                power_difference = max(min(power_difference, maximum), -maximum)
                Ab.forward()

                if power_difference == 0:
                    Ab.setPWMA(maximum)
                    Ab.setPWMB(maximum)
                elif power_difference < 0:
                    Ab.setPWMA(maximum + power_difference)
                    Ab.setPWMB(maximum)
                else:
                    Ab.setPWMA(maximum)
                    Ab.setPWMB(maximum - power_difference)

                cv2.line(frame, (cx, 0), (cx, 720), (255, 0, 0), 1)
                cv2.line(frame, (0, cy), (1280, cy), (255, 0, 0), 1)
                cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)
            else:
                print("Out of Sight")
                cx = 160

            cv2.putText(frame, str(proportional), (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.imshow("path", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print('exit...')
                Ab.stop()
                rawCapture.release()
                cv2.destroyAllWindows()
                break

    except Exception as err:
        print("An error occurred:", err)
    finally:
        Ab.stop()


if __name__ == "__main__":
    lineTracker()
