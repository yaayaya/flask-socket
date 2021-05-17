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
# import qwiic

# print("VL53L1X Qwiic Test\n")
# ToF = qwiic.QwiicVL53L1X()
# if (ToF.sensor_init() == None): # Begin returns 0 on a good init
#     print("Sensor online!\n")
# distance = 0
# def get_distance():
#     global distance
#     try:
#         ToF.start_ranging() # Write configuration bytes to initiate measurement
#         time.sleep(.03)
#         distance = ToF.get_distance()# Get the result of the measurement from the sensor
#         time.sleep(.03)
#         ToF.stop_ranging()
#         return distance
#         # print("Distance(mm): %s" % (distance))
#     except Exception as e:
#         print(e)
#         return distance

# 取得資料
_number = 0
isPlus = True

# 假資料取得
def getNumber():
    global isPlus
    global _number
    if (isPlus and _number <= 2000):
        _number += 50
        if (_number >= 2000):
            isPlus = False
    elif (not isPlus and _number > 0):
        _number -= 50
        if (_number <= 0):
            isPlus = True
    time.sleep(.5)
    return _number

# 把網頁叫出來  CORS防止圖片爆炸
@app.route('/')
def index():
    return render_template('Project1.html')

# 當前端呼叫 emit('getValue') 時執行
# 回傳資料至前端socket.io方法setValue
@socketio.event
def getValue():
    emit('setValue', {'data':getNumber()})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)

if __name__ == "__main__":
	socketio.run(app)