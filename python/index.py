import json
import sys
from PyQt5.QtWidgets import QApplication
from ChatRoomGui import ChatRoomGui
import pyrebase


rooms = []
messages = {}


def stream_handler(message):
    room = message["path"].split('/')[1]
    data = message["data"]
    if room == '' or data == 'None':
        return
    if room not in rooms:
        rooms.append(room)
    json_value = json.loads(data)
    if room not in messages:
        messages[room] = [json_value]
    else:
        new_messages = messages[room]
        new_messages.append(json_value)
        messages[room] = new_messages
    print(messages[room])


config = {
    "apiKey": "AIzaSyCJCjo-Gwpy_yFBu18x3Ng1tt0_ElLyi30",
    "authDomain": "pythonkakaopcwrapper.firebaseapp.com",
    "databaseURL": "https://pythonkakaopcwrapper-default-rtdb.firebaseio.com",
    "storageBucket": "pythonkakaopcwrapper.appspot.com"
}

firebase = pyrebase.initialize_app(config)

device_number = input('카카오톡이 설치된 기기 번호 입력: ')

db = firebase.database().child(device_number)
db.child("status").push("connected")
db.child(device_number).child("receive").stream(stream_handler)


def open_chat_room():
    app = QApplication(sys.argv)
    ChatRoomGui("aaa")
    sys.exit(app.exec_())
