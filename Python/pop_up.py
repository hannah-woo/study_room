import sys   #시스템 라이브러리
from PyQt5.QtWidgets import *   #위젯
from PyQt5.QtCore import *   #이벤트 처리

class Mywindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("윈도우")
        self.setGeometry(500, 500, 300, 300)
        
        btn1 = QPushButton("클릭", self)
        btn1.move(100, 100)
        btn1.clicked.connect(self.btn1_clicked)

    def btn1_clicked(self):
        QMessageBox.about(self, "팝업", "안녕하세요!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = Mywindow()
    myWindow.show()
    app.exec_()