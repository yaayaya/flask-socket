#!/usr/bin/env python
from threading import Event , Lock
from flask import Flask, render_template, session, request,  copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room,  close_room, rooms, disconnect
from flask_cors import cross_origin

import config
import random

app = Flask(__name__)
app.config.from_object(config)

socketio = SocketIO(app)
# Sensor
# Import required Python libraries
import time
import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO to use on Pi
GPIO_TRIGGER = 4
GPIO_ECHO = 17

print("Ultrasonic Measurement")

# Set pins as output and input
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo

# Set trigger to False (Low)
GPIO.output(GPIO_TRIGGER, False)
prev_distance = 0
def get_distance():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.1)
    GPIO.output(GPIO_TRIGGER, False)
    start = time.time()
    while GPIO.input(GPIO_ECHO)==0:
      start = time.time()
    while GPIO.input(GPIO_ECHO)==1:
      stop = time.time()
    # Calculate pulse length
    elapsed = stop-start
    # Distance pulse travelled in that time is time
    # multiplied by the speed of sound (cm/s)
    distance = elapsed * 34000
    # That was the distance there and back so halve the value
    distance = distance / 2
    global prev_distance
    if distance > 2500:
        return prev_distance
    else:
        prev_distance = distance
    return distance

# 取得資料
_number = 0
isPlus = True

# 假資料取得
def getNumber():
    global isPlus
    global _number
    if (isPlus and _number <= 300):
        _number += 10
        if (_number >= 300):
            isPlus = False
    elif (not isPlus and _number > 0):
        _number -= 10
        if (_number <= 0):
            isPlus = True
    return _number

# 把網頁叫出來  CORS防止圖片爆炸
@app.route('/')
@cross_origin()
def index():
    return render_template('Project1.html')

# 當前端呼叫 emit('getValue') 時執行
# 回傳資料至前端socket.io方法setValue
@socketio.event
def getValue():
    emit('setValue', {'data':get_distance()})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)

if __name__ == "__main__":
	socketio.run(app)
