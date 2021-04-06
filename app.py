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


# 取得資料
_number = 0
isPlus = True

def getNumber():
    global isPlus
    global _number
    if (isPlus and _number <= 1920):
        _number += 10
        if (_number >= 1920):
            isPlus = False
    elif (not isPlus and _number > 50):
        _number -= 10
        if (_number <= 300):
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
    emit('setValue', {'data':getNumber()})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)

if __name__ == "__main__":
	socketio.run(app,__debug__)
