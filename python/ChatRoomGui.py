from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

messages = []


class ChatRoomGui(QWidget):
    def __init__(self, _room):
        self.room = _room
        super().__init__()

        self.listview = QListView(self)
        self.edittext = QTextEdit(self)
        self.button = QPushButton("메시지 전송", self)
        self.init()

    def init(self):
        self.setFixedSize(500, 500)
        self.setWindowTitle(f'{self.room} 채팅방')

        self.listview.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.listview.resize(500, 400)

        self.edittext.setPlaceholderText("메시지 입력...")
        self.edittext.setAcceptRichText(False)
        self.edittext.resize(300, 50)
        self.edittext.move(30, 425)

        self.button.clicked.connect(self.message_send)
        self.button.move(370, 435)

        self.show()

    def message_send(self):
        message = self.edittext.toPlainText()
        if len(message) != 0:
            messages.append(message)
            model = QStandardItemModel()
            for message in messages:
                model.appendRow(QStandardItem(message))
            self.listview.setModel(model)
            self.edittext.clear()
        else:
            dialog = QMessageBox(self)
            dialog.setWindowTitle("경고")
            dialog.setText("메시지를 입력하세요.")
            dialog.show()
