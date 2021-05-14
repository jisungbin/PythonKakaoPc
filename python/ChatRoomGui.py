from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import json
import pyrebase

config = {
    'apiKey': 'AIzaSyCJCjo-Gwpy_yFBu18x3Ng1tt0_ElLyi30',
    "authDomain": 'pythonkakaopcwrapper.firebaseapp.com',
    'databaseURL': 'https://pythonkakaopcwrapper-default-rtdb.firebaseio.com',
    'storageBucket': 'pythonkakaopcwrapper.appspot.com'
}

firebase = pyrebase.initialize_app(config)


class ChatRoomGui(QWidget):
    def __init__(self, _room, _messages, _device_number):
        self.device_number = _device_number
        self.room = _room
        self.messages = _messages
        super().__init__()

        self.listview = QListView(self)
        self.edittext = QTextEdit(self)
        self.button = QPushButton('메시지 전송', self)
        self.init()

        self.db = firebase.database().child(_device_number).child('receive').stream(self.stream_handler)

    def stream_handler(self, message):
        data_string = message['data']
        if str(data_string).count(',') == 1:
            data_json = json.loads(data_string, strict=False)
            self.messages.append(data_json)
            model = QStandardItemModel()
            for message in self.messages:
                model.appendRow(QStandardItem(f'[{message.get("sender")}] - {message.get("message")}'))
            self.listview.setModel(model)

    def init(self):
        self.setFixedSize(500, 500)
        self.setWindowTitle(f'{self.room} 채팅방')

        self.listview.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.listview.resize(500, 400)

        self.edittext.setPlaceholderText('메시지 입력...')
        self.edittext.setAcceptRichText(False)
        self.edittext.resize(300, 50)
        self.edittext.move(30, 425)

        self.button.clicked.connect(self.message_send)
        self.button.move(370, 435)

        self.show()

    def message_send(self):
        message = self.edittext.toPlainText()
        json_string = "{" + f'"sender": "나", "message": "{message}", "room": "{self.room}"' + "}"
        json_value = json.loads(json_string, strict=False)
        if len(message) != 0:
            self.messages.append(json_value)
            model = QStandardItemModel()
            for message in self.messages:
                model.appendRow(QStandardItem(f'[{message.get("sender")}] - {message.get("message")}'))
            self.listview.setModel(model)
            self.edittext.clear()
            firebase.database().child(self.device_number).child('send').push(json_string)
        else:
            dialog = QMessageBox(self)
            dialog.setWindowTitle('경고')
            dialog.setText('메시지를 입력하세요.')
            dialog.show()
