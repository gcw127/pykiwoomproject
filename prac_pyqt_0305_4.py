import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *



class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #로그인
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.dynamicCall("CommConnect()")


        self.setWindowTitle("종목코드")
        self.setGeometry(300,300,300,150)

        btn1 = QPushButton("종목코드 얻기",self)
        btn1.move(190,20)
        btn1.clicked.connect(self.btn1_clicked)

        self.listWidget = QListWidget(self)
        self.listWidget.setGeometry(10,10,170,130)

    def btn1_clicked(self): #종목코드 가져오는 메서드 호출
        ret = self.kiwoom.dynamicCall("GetCodeListByMarket(QString)",
                                    ["0"])
        kospi_code_list = ret.split(';')
        kospi_code_name_list = []

        for x in kospi_code_list: #종목코드로 종목명 가져오기
            name = self.kiwoom.dynamicCall("GetMasterCodeName(QString)",[x])
            kospi_code_name_list.append(x + " : " + name)

        self.listWidget.addItems(kospi_code_name_list)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()
