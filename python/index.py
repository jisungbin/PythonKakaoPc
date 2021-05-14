import sys
from PyQt5.QtWidgets import QApplication
from ChatRoomGui import ChatRoomGui
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

device_number = int(input('카카오톡이 설치된 기기 번호 입력: '))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    test = ChatRoomGui("aaa")
    sys.exit(app.exec_())
