import psycopg2 as pg2 
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import sys
import PyQt5
from employeeSignin import *
from managerSignin import *
from adminSignin import *



class SignIn(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(50,50,360,360)
        self.setWindowTitle("Sign In")
        self.initUI()
        self.employeeW = employeeSignin()
        self.managerW = managerSignin()
        self.adminW = adminSignin()

    def initUI(self):
        self.username = QtWidgets.QLineEdit(self)
        self.username.setPlaceholderText('Username')
        self.username.setGeometry(20,90,100,30)
        #employeerole,managerrole,adminrole

        self.password_ = QtWidgets.QLineEdit(self)
        self.password_.setPlaceholderText('Password')
        self.password_.setGeometry(20,180,100,30)
        #passord = 'password3', 'password2', 'password3'

        self.login = QtWidgets.QPushButton('Login',self)
        self.login.move(20,300)
        self.login.clicked.connect(self.getloginInfo)


    def getloginInfo(self):
        #make connection with potgres to refernece 'role' table for access
        #store logins in dictionary
        self.login
        access = {}
        password = 'admin'
        conn = pg2.connect(database='payroll',user='postgres',password=password)
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM roles")
            rows = cur.fetchall()
            for r in rows:
                access.update({str(r[0]) : str(r[1])})
        conn.close()
        #Correct username/password?
        employeeU = 'employeerole'
        employeeP = 'password3'
        managerU = 'managerrole'
        managerP = 'password2'
        adminU = 'adminrole'
        adminP = 'password1'
        #if (self.username.text() in access.keys() ) and (access[self.username.text()] == self.password_.text()):

        if(self.username.text() == employeeU and self.password_.text() == employeeP  ):
            self.employeeW.show()
            self.password_.clear()
            self.close()
        if(self.username.text() == managerU and self.password_.text() == managerP ):
            self.managerW.show()
            self.password_.clear()
            self.close()
        if(self.username.text() == adminU and self.password_.text() == adminP):
            self.adminW.show()
            self.password_.clear()
            self.close()
                
            
            
        else:
            print("Denied")
            

#sign in : check if employee id is in database
# sign up : have fields, check for != drop table 