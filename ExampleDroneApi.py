from DroneApi import DroneApi
from flask import Flask, Response
import time
import cv2

app = Flask(__name__)
droneapi = DroneApi(is_fake=True)

@app.route('/')
def hello():
    return "Hello World!"

def gen():
    while True:
        #get camera frame
        frame = cv2.cvtColor(droneapi.frame_read.frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = np.flipud(frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')            


#@app.route('/videostrem/run')
#def run_video_stream():
#    droneapi.run()
#    return "OK"

@app.route('/takeoff')
def takeoff():
    droneapi.takeoff()
    return "OK"

@app.route('/land')
def land():
    droneapi.land()
    return "OK"

@app.route('/right')
def right():
    droneapi.right()
    return "OK"

@app.route('/left')
def left():
    droneapi.left()
    return "OK"

if __name__ == '__main__':
    app.run()