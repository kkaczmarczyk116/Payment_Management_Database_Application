import psycopg2 as pg2 
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import sys
import PyQt5

password = 'password'
conn = pg2.connect(database='payroll',user='managerrole',password=password)

class managerSignin(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(50,50,1024,1024)
        self.setWindowTitle("Manager")
        self.initUI()

    def initUI(self):
        self.list_widget = QtWidgets.QTableWidget(self)
        self.list_widget.setGeometry(50,50,800,200)
        self.list_widget.setColumnCount(10)
        self.list_widget.setHorizontalHeaderLabels(["SSN", "Gross","State Deduction","Federal Deduction","SS Deduction","Medicare","401k Deduction","Insurance Premuim","All Deduction","NetIncome"])
        self.list_widget.setVisible(False)
        self.r1 = QtWidgets.QPushButton(self)
        self.r1.setText("Report One")
        self.r1.move(30, 20)
        self.r1.clicked.connect(self.reportOne)


        self.r2 = QtWidgets.QPushButton(self)
        self.r2.setText("Report Two")
        self.r2.move(30, 260)
        self.r2.clicked.connect(self.reportTwo)

        self.list_widget2 = QtWidgets.QTableWidget(self)
        self.list_widget2.setGeometry(50,300,420,150)
        self.list_widget2.setColumnCount(4)
        self.list_widget2.setHorizontalHeaderLabels(["SSN","2021 Annual Income","All Deductions","Extra Earnings"])
        self.list_widget2.setVisible(False)
        
        self.r3 = QtWidgets.QPushButton(self)
        self.r3.setText("Report Three")
        self.r3.move(30,470)
        self.r3.clicked.connect(self.reportThree)

        self.list_widget3 = QtWidgets.QTableWidget(self)
        self.list_widget3.setGeometry(50,520,220,100)
        self.list_widget3.setColumnCount(2)
        self.list_widget3.setHorizontalHeaderLabels(["SSN","Total Costs"])
        self.list_widget3.setVisible(False)
   
    def callSQL(self):
        with conn.cursor() as cur:
            cur.execute("""
            SELECT checkk.check_id,checkk.soc_security,checkk.gross,receives.employee_id,((checkk.state_tax)*(checkk.gross)/100),((checkk.federal_tax)*(checkk.gross)/100),
            CAST((checkk.gross*.025)AS INTEGER),employee.employee_id,employee.salary_type,employee.benefits_id,benefits._401k_cont,(checkk.gross*(CAST(benefits._401k_cont AS INTEGER)/100)),insuranceplan.premium_individual,insuranceplan.premium_family
            ,CASE employee.salary_type
		    WHEN 'hourly' THEN CAST((checkk.gross*.075)AS INTEGER)
	        ELSE CAST((checkk.gross*.15)AS INTEGER)
	        END social_sec
            FROM checkk JOIN receives ON receives.check_id=CAST(checkk.check_id AS INTEGER)
            JOIN employee ON employee.employee_id=receives.employee_id
            JOIN benefits ON benefits.benefits_id=employee.benefits_id
            JOIN insuranceplan ON insuranceplan.insurance_id=employee.insurance_id
            ORDER BY checkk.soc_security ASC;
            """)
            self.rows = cur.fetchall()

    def callSQL2(self):
        with conn.cursor() as cur:
            cur.execute("""
            SELECT checkk.check_id,checkk.soc_security,checkk.gross,receives.employee_id,((checkk.state_tax)*(checkk.gross)/100),((checkk.federal_tax)*(checkk.gross)/100),(checkk.gross*.025),employee.employee_id,employee.salary_type,employee.benefits_id,benefits._401k_cont,(checkk.gross*(CAST(benefits._401k_cont AS INTEGER)/100)),insuranceplan.premium_individual,insuranceplan.premium_family
            ,CASE employee.salary_type
		    WHEN 'hourly' THEN (checkk.gross*.075)
	        ELSE (checkk.gross*.15)
	        END social_sec
            FROM checkk JOIN receives ON receives.check_id=CAST(checkk.check_id AS INTEGER)
            JOIN employee ON employee.employee_id=receives.employee_id
            JOIN benefits ON benefits.benefits_id=employee.benefits_id
            JOIN insuranceplan ON insuranceplan.insurance_id=employee.insurance_id
            WHERE receives.year = 2021
            ORDER BY checkk.soc_security ASC;
            """)
            self.rows = cur.fetchall()


    def callSQL3(self):
        with conn.cursor() as cur:
            cur.execute("""
               CREATE TABLE deductions AS SELECT checkk.soc_security,checkk.gross,((checkk.state_tax)*(checkk.gross)/100) AS stateT,((checkk.federal_tax)*(checkk.gross)/100) AS fed,(checkk.gross*.025) AS medi,(checkk.gross*(CAST(benefits._401k_cont AS INTEGER)/100)) AS _401kC
                ,CASE employee.salary_type
		        WHEN 'hourly' THEN (checkk.gross*.075)
	            ELSE (checkk.gross*.15)
	            END social_sec
                FROM checkk JOIN receives ON receives.check_id=CAST(checkk.check_id AS INTEGER)
                JOIN employee ON employee.employee_id=receives.employee_id
                JOIN benefits ON benefits.benefits_id=employee.benefits_id
                JOIN insuranceplan ON insuranceplan.insurance_id=employee.insurance_id
                WHERE receives.year = 2021
                ORDER BY checkk.soc_security ASC;
                SELECT soc_security,SUM(statet+fed+medi+_401kc+social_sec)
                FROM deductions
                GROUP by soc_security
                ORDER BY soc_security ASC;
           """ )
            self.rows = cur.fetchall()


    def callSQL4(self):
        with conn.cursor() as cur:
            cur.execute("""
            SELECT soc_security,Sum(gross) FROM checkk
            WHERE year ='2021'
            GROUP By soc_security
            ORDER BY soc_security ASC;
            """  )
            self.rows = cur.fetchall()

    def callSQL5(self):
        with conn.cursor() as cur:
            cur.execute("""
            SELECT checkk.soc_security,SUm(receives.bonus) FROM receives
            JOIN checkk ON checkk.check_id=receives.check_id
            GROUP by checkk.soc_security
            ORDER BY soc_security ASC;
            """  )
            self.rows = cur.fetchall()
    
    def callSQL6(self):
        with conn.cursor() as cur:
            cur.execute("""
            SELECT checkk.soc_security,SUM(receives.bonus+checkk.gross)
 			,CASE employee.salary_type
			WHEN 'W2' THEN CAST((checkk.gross *.075)AS INTEGER)
			ELSE (checkk.gross *0)
			END company_w2_con
			,CASE benefits._401k_cont
			WHEN '1' THEN CAST(SUM(checkk.gross *.001)AS INTEGER)
			WHEN '2' THEN CAST(SUM(checkk.gross *.002)AS INTEGER)
			WHEN '3' THEN CAST(SUM(checkk.gross *.003)AS INTEGER)
			WHEN '4' THEN CAST(SUM(checkk.gross *.004)AS INTEGER)
			WHEN '5' THEN CAST(SUM(checkk.gross *.005)AS INTEGER)
			WHEN '6' THEN CAST(SUM(checkk.gross *.006)AS INTEGER)
			ELSE CAST(SUM(checkk.gross *.007)AS INTEGER)
			END company_401_cont
			FROM receives
            JOIN checkk ON checkk.check_id=receives.check_id
			JOIN employee ON employee.employee_id=receives.employee_id
			JOIN benefits ON benefits.benefits_id=employee.benefits_id
            GROUP by checkk.soc_security, employee.employee_id,checkk.gross,benefits._401k_cont
            ORDER BY soc_security ASC;

            """)
            self.rows = cur.fetchall()


    def reportOne(self):
            self.list_widget.setVisible(True)
            self.callSQL()
            count = 0
            self.list_widget.setRowCount(len(self.rows))
            for r in self.rows:
                item = QtWidgets.QTableWidgetItem(str(r[1]))
                self.list_widget.setItem(count, 0, item)
                count += 1

            self.callSQL()
            count = 0
            for r in self.rows:
                item = QtWidgets.QTableWidgetItem(str(r[2]))
                self.list_widget.setItem(count, 1, item)
                count += 1

            self.callSQL()
            count = 0
            for r in self.rows:
                item = QtWidgets.QTableWidgetItem(str(r[4]))
                self.list_widget.setItem(count, 2, item)
                count += 1

            self.callSQL()
            count = 0
            for r in self.rows:
                item = QtWidgets.QTableWidgetItem(str(r[5]))
                self.list_widget.setItem(count, 3, item)
                count += 1
            
            self.callSQL()
            count = 0
            for r in self.rows:
                item = QtWidgets.QTableWidgetItem(str(r[6]))
                self.list_widget.setItem(count, 5, item)
                count += 1

            self.callSQL()
            count = 0
            for r in self.rows:
                item = QtWidgets.QTableWidgetItem(str(r[14]))
                self.list_widget.setItem(count, 4, item)
                count += 1

            self.callSQL()
            count = 0
            for r in self.rows:
                item = QtWidgets.QTableWidgetItem(str(r[11]))
                self.list_widget.setItem(count, 6, item)
                count += 1

            self.callSQL()
            count = 0
            for r in self.rows:
                item = QtWidgets.QTableWidgetItem(str(r[12]))
                self.list_widget.setItem(count, 7, item)
                count += 1
            
            self.callSQL()
            count = 0
            for r in self.rows:
                total = int(r[4]) + int(r[5])+ int(r[6])+ int(r[4])+ int(r[11])+ int(r[12])+ int(r[14])
                item = QtWidgets.QTableWidgetItem(str(total))
                self.list_widget.setItem(count, 8, item)
                count += 1

            self.callSQL()
            count = 0
            for r in self.rows:
                total = int(r[4]) + int(r[5])+ int(r[6])+ int(r[4])+ int(r[11])+ int(r[12])+ int(r[14])
                net = (int(r[2] -total))
                item = QtWidgets.QTableWidgetItem(str(net))
                self.list_widget.setItem(count, 9, item)
                count += 1


    def getRow(self,i):
        self.callSQL2()
        self.a = []
        for r in self.rows:
                item = QtWidgets.QTableWidgetItem(str(r[i]))
                if item.text() not in self.a:
                    self.a.append(item.text())
        return len(self.a)



    def reportTwo(self):
        
        count = 0
        self.rowN = self.getRow(1)
        self.list_widget2.setRowCount(self.rowN)
        for r in self.a:
                item = QtWidgets.QTableWidgetItem(r)
                self.list_widget2.setItem(count, 0, item)
                count += 1
        
        self.callSQL4()
        count=0
        for r in self.rows:
            item = QtWidgets.QTableWidgetItem(str(r[1]))
            self.list_widget2.setItem(count, 1, item)
            count += 1

        self.callSQL3()
        count=0
        for r in self.rows:
            item = QtWidgets.QTableWidgetItem(str(r[1]))
            self.list_widget2.setItem(count, 2, item)
            count += 1
            

        self.callSQL5()
        count=0
        for r in self.rows:
            item = QtWidgets.QTableWidgetItem(str(r[1]))
            self.list_widget2.setItem(count, 3, item)
            count += 1
            

                
        self.list_widget2.setVisible(True)


    def reportThree(self):
        self.callSQL6()
        count=0
        self.list_widget3.setRowCount(len(self.rows))
        for r in self.rows:
            item = QtWidgets.QTableWidgetItem(str(r[0]))
            self.list_widget3.setItem(count, 0, item)
            count += 1
            
        count=0
        for r in self.rows:
            total_spent = int(r[1]) + int(r[2])+ int(r[3])
            item = QtWidgets.QTableWidgetItem(str(total_spent))
            self.list_widget3.setItem(count, 1, item)
            count += 1

        self.list_widget3.setVisible(True)