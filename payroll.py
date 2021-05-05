import psycopg2 as pg2 
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import sys
import PyQt5
from signIn import *



password = 'admin'
conn = pg2.connect(database='payroll',user='postgres',password=password)

class MyWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setGeometry(50,50,500,200)
        self.setWindowTitle("Payroll")
        self.setStyleSheet("background-color:rgb(215,214,213);")
        self.initUI()
        self.secondW = SignIn()

    def initUI(self):
        
        
        admin_button = QtWidgets.QPushButton('Admin',self)
        admin_button.move(50,100)
        admin_button.clicked.connect(self.passing)

        manager_button = QtWidgets.QPushButton('Manager', self)
        manager_button.move(200,100)
        manager_button.clicked.connect(self.passing)

        employee_button = QtWidgets.QPushButton('Employee',self)
        employee_button.move(350,100)
        employee_button.clicked.connect(self.passing)

        
    
    def passing(self):
       self.secondW.show()




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())