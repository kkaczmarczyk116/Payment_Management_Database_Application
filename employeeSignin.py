import psycopg2 as pg2 
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import sys
import PyQt5

password = 'password'
conn = pg2.connect(database='payroll',user='employeerole',password=password)

class employeeSignin(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(50,50,360,360)
        self.setWindowTitle("Employee")
        self.initUI()

    def initUI(self):

        ###############
        #Setup Fields for UPDATE/ADD FUNCTION
        ###############

        self.title = QtWidgets.QLabel(self)
        self.title.setText("Add New Employee")
        self.title.move(50,20)
        self.employee_id = QtWidgets.QLineEdit(self)
        self.employee_id.setPlaceholderText('Employee ID')
        self.employee_id.move(50,50)
        self.fname = QtWidgets.QLineEdit(self)
        self.fname.setPlaceholderText('First Name')
        self.fname.move(50,80)
        self.lname = QtWidgets.QLineEdit(self)
        self.lname.setPlaceholderText('Last Name')
        self.lname.move(50,110)
        self.job = QtWidgets.QLineEdit(self)
        self.job.setPlaceholderText('Job Title')
        self.job.move(50,140)
        self.salaryType = QtWidgets.QLineEdit(self)
        self.salaryType.setPlaceholderText('Salary Type')
        self.salaryType.move(50,170)
        self.contribution = QtWidgets.QLineEdit(self)
        self.contribution.setPlaceholderText('Contribution')
        self.contribution.move(50,200)
        self.insuranceid = QtWidgets.QLineEdit(self)
        self.insuranceid.setPlaceholderText('Insurance: 1 or 2')
        self.insuranceid.move(50,230)
        self.benefitsid = QtWidgets.QLineEdit(self)
        self.benefitsid.setPlaceholderText('Benefits: 1 or 2')
        self.benefitsid.move(50,260)
        self.update = QtWidgets.QPushButton('Add',self)
        self.update.move(50,290)
        self.update.clicked.connect(self.sendToDB)
        
        
        self.viewlable =QtWidgets.QLabel(self)
        self.viewlable.setText('View Employees By Id')
        self.viewlable.move(200,90)
        self.list_widget = QtWidgets.QListWidget(self)
        self.list_widget.setGeometry(200,110,100,80)

        with conn.cursor() as cur:
            cur.execute("SELECT * FROM employee ORDER BY employee_id ASC;")
            rows = cur.fetchall()
            for r in rows:
                self.item = QtWidgets.QListWidgetItem(str(r[0]))
                self.list_widget.addItem(self.item)

        self.list_widget.itemClicked.connect(self.list_clicked)

    
    
    def list_clicked(self,item):
        self.employee_id = item.text()
        self.emp = str(self.employee_id)
        
        with conn.cursor() as cur:
            
            cur.execute("SELECT * FROM employee WHERE employee_id = %s",(self.emp))
            rows = cur.fetchall()
            for r in rows:
                print(str(r[0]) +' '+ str(r[1])+' '+ str(r[2])+' '+ str(r[3])+' '+ str(r[4])+' '+ str(r[5])+' '+ str(r[6])+' '+ str(r[7]))
        #conn.close()

    def error_flag(self):
        self.error_dialog = QtWidgets.QMessageBox()
        self.error_dialog.setIcon(QtWidgets.QMessageBox.Critical)
        self.error_dialog.setWindowTitle("ERROR")
        self.error_dialog.setText("Employee ID allready taken\nTry another number And/Or\nCheck if all provided information is correct")
        self.error_dialog.setGeometry(50,50,200,200)
        self.error_dialog.exec_() 


    def sendToDB(self):
        try:
            sql ="INSERT INTO employee(employee_id,first_name,last_name,job_title,salary_type,contribution,insurance_id,benefits_id)VALUES(%s,%s,%s,%s,%s,%s,%s,%s);" 
            with conn.cursor() as cur:
                cur.execute(sql,(int(self.employee_id.text()),self.fname.text(),self.lname.text(),self.job.text(),self.salaryType.text(),self.contribution.text(),int(self.insuranceid.text()),int(self.benefitsid.text())))
            conn.commit()
            
        except:
            self.error_flag()