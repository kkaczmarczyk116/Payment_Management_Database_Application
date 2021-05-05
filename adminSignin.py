import psycopg2 as pg2 
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import sys
import PyQt5

password = 'password'
conn = pg2.connect(database='payroll',user='adminrole',password=password)

class adminSignin(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(50,50,1024,1024)
        self.setWindowTitle("Admin")
        self.initUI()

    def initUI(self):
        self.updateE = QtWidgets.QLabel(self)
        self.updateE.setText("Update Employee")
        self.updateE.move(50,20)
        self.employee_id = QtWidgets.QLineEdit(self)
        self.employee_id.setPlaceholderText('Employee ID')
        self.employee_id.move(50,50)
        self.fname = QtWidgets.QLineEdit(self)
        self.fname.setPlaceholderText('First Name')
        self.fname.move(50,70)
        self.lname = QtWidgets.QLineEdit(self)
        self.lname.setPlaceholderText('Last Name')
        self.lname.move(50,90)
        self.job = QtWidgets.QLineEdit(self)
        self.job.setPlaceholderText('Job Title')
        self.job.move(50,110)
        self.salaryType = QtWidgets.QLineEdit(self)
        self.salaryType.setPlaceholderText('Salary Type')
        self.salaryType.move(50,130)
        self.contribution = QtWidgets.QLineEdit(self)
        self.contribution.setPlaceholderText('Contribution')
        self.contribution.move(50,150)
        self.insuranceid = QtWidgets.QLineEdit(self)
        self.insuranceid.setPlaceholderText('Insurance: 1 or 2')
        self.insuranceid.move(50,170)
        self.benefitsid = QtWidgets.QLineEdit(self)
        self.benefitsid.setPlaceholderText('Benefits: 1 or 2')
        self.benefitsid.move(50,190)
        self.updateC = QtWidgets.QPushButton('Update',self)
        self.updateC.move(50,220)
        self.updateC.clicked.connect(self.updateEmployeeC)

        self.updateB = QtWidgets.QLabel(self)
        self.updateB.setText("Update Benefits")
        self.updateB.move(50,320)
        self.benefit_id = QtWidgets.QLineEdit(self)
        self.benefit_id.setPlaceholderText('Benefit ID')
        self.benefit_id.move(50,340)
        self.health_plan = QtWidgets.QLineEdit(self)
        self.health_plan.setPlaceholderText('Health Plan')
        self.health_plan.move(50,360)
        self._401k_cont = QtWidgets.QLineEdit(self)
        self._401k_cont.setPlaceholderText('401k Contribution')
        self._401k_cont.move(50,380)
        self.attorney_plan = QtWidgets.QLineEdit(self)
        self.attorney_plan.setPlaceholderText('Attorney Plan')
        self.attorney_plan.move(50,400)
        self.life_insurance = QtWidgets.QLineEdit(self)
        self.life_insurance.setPlaceholderText('Life Insurance')
        self.life_insurance.move(50,420)
        self.match = QtWidgets.QLineEdit(self)
        self.match.setPlaceholderText('Match')
        self.match.move(50,440)
        self.dental = QtWidgets.QLineEdit(self)
        self.dental.setPlaceholderText('Dental')
        self.dental.move(50,460)
        self.vision = QtWidgets.QLineEdit(self)
        self.vision.setPlaceholderText('Vision')
        self.vision.move(50,480)
        self.updatebu = QtWidgets.QPushButton('Update',self)
        self.updatebu.move(50,510)
        self.updatebu.clicked.connect(self.updateBenefits)


        self.updateD = QtWidgets.QLabel(self)
        self.updateD.setText("Update Dependent")
        self.updateD.move(200,20)
        self.dId = QtWidgets.QLineEdit(self)
        self.dId.setPlaceholderText('Dependent Id')
        self.dId.move(200,50)
        self.dname = QtWidgets.QLineEdit(self)
        self.dname.setPlaceholderText('Dependent Name')
        self.dname.move(200,70)
        self.rel = QtWidgets.QLineEdit(self)
        self.rel.setPlaceholderText('relation')
        self.rel.move(200,90)
        self.dssn = QtWidgets.QLineEdit(self)
        self.dssn.setPlaceholderText('Dependent SSN')
        self.dssn.move(200,110)
        self.bId = QtWidgets.QLineEdit(self)
        self.bId.setPlaceholderText('Benefit Id')
        self.bId.move(200,130)
        self.eId = QtWidgets.QLineEdit(self)
        self.eId.setPlaceholderText('Employee Id')
        self.eId.move(200,150)
        self.updateD = QtWidgets.QPushButton('Update',self)
        self.updateD.move(200,180)
        self.updateD.clicked.connect(self.updateDependents)
       
        self.updateT = QtWidgets.QLabel(self)
        self.updateT.setText("Update Tax")
        self.updateT.move(200,320)
        self.cId = QtWidgets.QLineEdit(self)
        self.cId.setPlaceholderText('Check Id')
        self.cId.move(200,340)
        self.stateT = QtWidgets.QLineEdit(self)
        self.stateT.setPlaceholderText('State Tax')
        self.stateT.move(200,360)
        self.fedT = QtWidgets.QLineEdit(self)
        self.fedT.setPlaceholderText('Federal Tax')
        self.fedT.move(200,380)
        self.updateD = QtWidgets.QPushButton('Update',self)
        self.updateD.move(200,410)
        self.updateD.clicked.connect(self.updateTax)

        self.updatelabel = QtWidgets.QLabel(self)
        self.updatelabel.setText("Update Bonus")
        self.updatelabel.move(350,20)
        self.checkId = QtWidgets.QLineEdit(self)
        self.checkId.setPlaceholderText('Check ID')
        self.checkId.move(350,40)
        self.bonus = QtWidgets.QLineEdit(self)
        self.bonus.setPlaceholderText('Bonus')
        self.bonus.move(350,60)
        self.updateCB = QtWidgets.QPushButton('Update',self)
        self.updateCB.move(350,90)
        self.updateCB.clicked.connect(self.updateBonus)


        self.saveb = QtWidgets.QPushButton('Done', self)
        self.saveb.move(350,510)
        self.saveb.clicked.connect(self.save)

    def updateEmployeeC(self):
        with conn.cursor() as cur:
            cur.execute("UPDATE employee SET first_name = %s,last_name = %s, job_title = %s,salary_type = %s, contribution =%s, insurance_id =%s,benefits_id=%s WHERE employee_id =%s",(self.fname.text(),self.lname.text(),self.job.text(),self.salaryType.text(),self.contribution.text(),self.insuranceid.text(),self.benefitsid.text(),self.employee_id.text()))
        conn.commit()
        #conn.close()

    def updateBenefits(self):
        with conn.cursor() as cur:
            cur.execute("UPDATE benefits SET health_plan=%s,_401k_cont=%s,attorney_plan=%s,life_insurance=%s,matchamount=%s,dental=%s,vision=%s WHERE benefits_id = %s",(self.health_plan.text(),self._401k_cont.text(),self.attorney_plan.text(),self.life_insurance.text(),self.match.text(),self.dental.text(),self.vision.text(),self.benefit_id.text()))
        conn.commit()
        #conn.close()
    
    def updateDependents(self):
        with conn.cursor() as cur:
            cur.execute("UPDATE dependents SET dependentname=%s,relation=%s,dependednt_ssn=%s,benefits_id =%s,employee_id=%s WHERE dependent_id =%s",(self.dname.text(),self.rel.text(),self.dssn.text(),self.bId.text(),self.eId.text(),self.dId.text()))
        conn.commit()
        #conn.close()

    def updateTax(self):
        with conn.cursor() as cur:
            cur.execute("UPDATE checkk SET state_tax = %s,federal_tax =%s WHERE check_id = %s",(self.stateT.text(),self.fedT.text(),self.cId.text()))
        conn.commit()
        #conn.close()

    def updateBonus(self):
        with conn.cursor() as cur:
            cur.execute("UPDATE receives SET bonus =%s WHERE check_id =%s",(self.bonus.text(),self.checkId.text()))
            conn.commit()

    def save(self):
        conn.close()
        self.close()