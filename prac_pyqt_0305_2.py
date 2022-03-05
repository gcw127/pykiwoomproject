import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *


class MyWindow(QMainWindow): #QWindow 상속
    def __init__(self):
        super().__init__()

        #키움 로그인처리
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.dynamicCall("CommConnect()")

        #openAPI+ event
        self.kiwoom.OnEventConnect.connect(self.event_connect)
        self.kiwoom.OnReceiveTrData.connect(self.receive_trdata)
        #OnReceiveTrdata는 서버로부터 tr 데이터 받아왔을 때 발생


        self.setWindowTitle("Pystock")
        self.setGeometry(300,300,300,150)

        label = QLabel('종목코드 : ',self) #간단한 텍스트출력
        label.move(10,20)

        self.code_edit = QLineEdit(self) #사용자 입력처리
        self.code_edit.move(80,20) #위치만조정하는 move, 크기위치동시에 setGeometry
        self.code_edit.setText("039490")

        btn1 = QPushButton("조회",self)
        btn1.move(190,20)
        btn1.clicked.connect(self.btn1_clicked)

        self.text_edit = QTextEdit(self) #메세지출력 (실행결과)
        self.text_edit.setGeometry(10,60,280,80)
        self.text_edit.setEnabled(False)


    def event_connect(self, err_code):
        if err_code == 0:
            self.text_edit.append("로그인 성공")

    def btn1_clicked(self):
        code = self.code_edit.text() #사용자가 입력한 코드 가져옴
        self.text_edit.append("종목코드 : " + code)

        #input값으로 설정하기 / SetInputValue : TR입력값 설정
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)","종목코드",code)

        #CommRqData : 입력값 서버로 전송 , 첫 인자는 tr인지 확인하기위한 용도
        self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)",
                                "opt10001_req","opt10001",0,"0101")

    def receive_trdata(self, screen_no,rqname,trcode,recordname,
                       prev_next, data_len, err_code, msg1, msg2):
        if rqname == "opt10001_req":
            #서버로부터 종목명, 거래량 받아오기
            name = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString,"
                                           "int, QString)", trcode, "",rqname,0,"종목명")
            volume = self.kiwoom.dynamicCall("CommGetData(QString, QString,QString,int,"
                                             "QString)", trcode,"",rqname,0,"거래량")

            #CommGetData : 수신된 데이터 가져오기
            self.text_edit.append("종목명: " + name.strip())
            self.text_edit.append("거래량: " + volume.strip())



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
