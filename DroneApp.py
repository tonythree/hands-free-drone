from DroneApi import DroneApi
from flask import Flask, Response
import time
import cv2
import numpy as np

app = Flask(__name__)
droneapi = DroneApi(is_fake=True)

@app.route('/')
def hello():
    return "Hello World!"            

@app.route('/connect')
def connect():
    return "OK" if droneapi.connect() else "KO"

def generateVideStream():
	while True:
		frame = droneapi.frame_read.frame

		# check if the output frame is available, otherwise skip
		# the iteration of the loop
		if frame is None:
			continue

		# encode the frame in JPEG format
		(flag, encodedImage) = cv2.imencode(".jpg", frame)
		# ensure the frame was successfully encoded
		if not flag:
			continue

		yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n\r\n')

@app.route('/videostream')
def video_feed():
    return Response(generateVideStream(), mimetype='multipart/x-mixed-replace; boundary=frame')

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

@app.route('/up')
def up():
    droneapi.up()
    return "OK"

@app.route('/down')
def down():
    droneapi.down()
    return "OK"

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5001)