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
    def __init__(self, _room, _messages, device_number):
        self.db = firebase.database().child(device_number).child('send')
        self.room = _room
        self.messages = _messages
        super().__init__()

        self.listview = QListView(self)
        self.edittext = QTextEdit(self)
        self.button = QPushButton('메시지 전송', self)
        self.init()

    def init(self):
        self.setFixedSize(500, 500)
        self.setWindowTitle(f'{self.room} 채팅방')

        model = QStandardItemModel()
        for message in self.messages:
            model.appendRow(QStandardItem(f'[{message.get("sender")}] - {message.get("message")}'))
        self.listview.setModel(model)
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
        json_string = "{" + f'"sender": "나", "message": "{message}"' + "}"
        json_value = json.loads(json_string)
        if len(message) != 0:
            self.messages.append(json_value)
            model = QStandardItemModel()
            for message in self.messages:
                model.appendRow(QStandardItem(f'[{message.get("sender")}] - {message.get("message")}'))
            self.listview.setModel(model)
            self.edittext.clear()

            self.db.push(json_string)
        else:
            dialog = QMessageBox(self)
            dialog.setWindowTitle('경고')
            dialog.setText('메시지를 입력하세요.')
            dialog.show()
