import sys
from PyQt5.QAxContainer import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MyWindow(QMainWindow): #pyqt가 제공하는 Qmainwindow클래스 상속
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyStock")
        self.setGeometry(300,300,300,150)

        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.dynamicCall("CommConnect()") #로그인창실행

        self.text_edit = QTextEdit(self) #텍스트 객체 self.text_edit로 바인딩
        #self.text_edit가 클래스 다른 메서드 내에서도 호출 필요하기 때문에 self.붙여서바인딩
        #필요없으면 그냥 text_deit로 해도 됨

        self.text_edit.setGeometry(10,60,280,80)
        self.text_edit.setEnabled(False)

        self.kiwoom.OnEventConnect.connect(self.event_connect)

    def event_connect(self,err_code): #OnEventConnect 함수에 필요한 errcode 인자로 받기
        if err_code ==0: #0이면 로그인성공
            self.text_edit.append("로그인 성공")


if __name__ == "__main__":
    app = QApplication(sys.argv) #Qapp 인스턴스 생성
    myWindow = MyWindow() #위에 만든 MyWindow() 클래서 인스턴스생성
    myWindow.show()
    app.exec_() #이벤트루프