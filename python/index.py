import json
import sys
from ChatRoomGui import ChatRoomGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pyrebase
import turtle
from plyer import notification

rooms = []
messages = {}

device_number = input('카카오톡이 설치된 기기 번호 입력: ')


def open_chat_room(room):
    global messages
    notification.notify(
        title='알림',
        message='새로운 창이 열리지 않으면 현재 창을 닫아주세요.',
        timeout=5,
    )
    app = QApplication(sys.argv)
    _ = ChatRoomGui(room, messages[room], device_number)
    sys.exit(app.exec_())


def window_click(x, y):
    print(y)
    if 200 <= y <= 250:
        open_chat_room(rooms[0])
    elif 150 <= y <= 199:
        open_chat_room(rooms[1])
    elif 100 <= y <= 149:
        open_chat_room(rooms[2])


def draw_rooms():
    for i in range(0, len(rooms)):
        room = rooms[i]
        y = 200 - (50 * i)
        print(y)
        turtle.penup()
        turtle.goto(0, y)
        turtle.pendown()
        turtle.write(room, font=('나눔고딕', 20))


def stream_handler(message):
    global messages
    global rooms
    room = message['path'].split('/')[1]
    data = message['data']
    if room == '' or data == 'None':
        return
    if room not in rooms:
        rooms.append(room)
        draw_rooms()
        print(rooms)
    json_value = json.loads(data)
    if room not in messages:
        messages[room] = [json_value]
    else:
        new_messages = messages[room]
        new_messages.append(json_value)
        messages[room] = new_messages


config = {
    'apiKey': 'AIzaSyCJCjo-Gwpy_yFBu18x3Ng1tt0_ElLyi30',
    "authDomain": 'pythonkakaopcwrapper.firebaseapp.com',
    'databaseURL': 'https://pythonkakaopcwrapper-default-rtdb.firebaseio.com',
    'storageBucket': 'pythonkakaopcwrapper.appspot.com'
}

firebase = pyrebase.initialize_app(config)

db = firebase.database().child(device_number)
db.child('status').push('connected')
db.child(device_number).child('receive').stream(stream_handler)

window = turtle.Screen()
window.title('카카오톡 PC버전 따라하기')
window.setup(500, 500)
window.onclick(window_click)

turtle.speed(10)
turtle.mainloop()
