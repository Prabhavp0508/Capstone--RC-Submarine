from flask import Flask, render_template
from flask import request, jsonify
import random
 
# PI specific shit
import time
import board
import os
import glob
import redis
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685
 
i2c = board.I2C()  # uses board.SCL and board.SDA
pca = PCA9685(i2c)
pca.frequency = 50
 
servoTurn = servo.Servo(pca.channels[0])
servoRotate = servo.Servo(pca.channels[1])
currentTurn = 0
currentRotate = 0

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

 
app = Flask(__name__)
 
@app.route('/')
def index():
    return render_template('test.html')
 
@app.route('/data', methods=['POST'])
def data():
    global currentTurn, currentRotate
 
    if request.is_json:
        data = request.get_json()
        print(data)
 
        if "cam-up" in data['buttons']:
            if currentTurn < 150:
                currentTurn += 10
            else:
                currentTurn = 150
        elif "cam-down" in data['buttons']:
            if currentTurn > 0:
                currentTurn -= 10
            else:
                currentTurn = 0
                
        elif "cam-left" in data['buttons']:
            if currentRotate < 180:
                currentRotate += 10
            else:
                currentRotate = 180
        elif "cam-right" in data['buttons']:
            if currentRotate > 0:
                currentRotate -= 10
            else:
                currentRotate = 0
 
        servoTurn.angle = currentTurn
        servoRotate.angle = currentRotate

        if "motor-start" in data['navButtons']:
            r.set('motor', 'start')
        elif "motor-stop" in data['navButtons']:
            r.set('motor', 'stop')
        elif "ballast-up" in data['navButtons']:
            r.set('ballast', 'up')
        elif "ballast-down" in data['navButtons']:
            r.set('ballast', 'down')
        else:
            r.set('ballast', 'stop')
            r.set('motor', 'none')

        r.set('motorValue', data['sliderValue'])

        response = {
            "temperature": f"{r.get('temperature')}",
            "ballast": "Ballast: ????? 45%",
            "bottom_distance": f"{r.get('bottom_distance')}",
            "front_distance": f"{r.get('front_distance')}",
            "pressure": f"{r.get('depth')}",
        }
        return jsonify(response), 200
    else:
        return jsonify({"message": "Request must be JSON"}), 200
 
 
app.run(host='0.0.0.0', port=5000)
 
pca.deinit()
