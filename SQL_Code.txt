create table Employee (
employee_id SERIAL PRIMARY KEY,
first_name VARCHAR(20) NOT NULL,
last_name VARCHAR(20) NOT NULL,
job_title VARCHAR(20) NOT NULL,
salary_type VARCHAR(20) NOT NULL,
contribution VARCHAR(20),
insurance_id VARCHAR(20) REFERENCES InsurancePlan,
benefits_id VARCHAR(20) REFERENCES Benefits
)

CREATE table InsurancePlan (
Insurance_id SERIAL PRIMARY KEY,
premium_individual VARCHAR(50) NOT NULL,
premium_family VARCHAR(50) NOT NULL
)
create table Benefits (
benefits_id SERIAL PRIMARY KEY,
health_plan VARCHAR(20),
401k_cont INTEGER,
attorney_plan VARCHAR(20),
life_insurance VARCHAR(20),
matchamount VARCHAR(20),
dental VARCHAR(20),
vision VARCHAR(20)
)
create table Dependents (
dependent_id SERIAL PRIMARY KEY,
dependentname VARCHAR(20) NOT NULL,
relation VARCHAR(20) NOT NULL,
dependednt_ssn VARCHAR(20) UNIQUE NOT NULL,
benefits_id VARCHAR(20) REFERENCES Benefits,
employee_ID VARCHAR(20) REFERENCES Employee
)
create table Checkk (
check_id VARCHAR(20) UNIQUE NOT NULL PRIMARY KEY,
state_tax INTEGER NOT NULL,
federal_tax INTEGER NOT NULL,
soc_security VARCHAR(10) NOT NULL,
medicare INTEGER NOT NULL,

create table receives (
check_ID INTEGER UNIQUE PRIMARY KEY,
Bonus INTEGER,
Employee_id INTEGER REFERENCES Employee(employee_id) ON UPDATE CASCADE ON DELETE CASCADE;
)


INSERT INTO employee(employee_id,first_name,last_name,job_title,salary_type,contribution,insurance_id,benefits_id)
VALUES(1,'Kamil','Kaczmarczyk','student','salary','100','1','1')

CREATE ROLE employeerole with password 'password' LOGIN;
GRANT SELECT on "employee" to employeerole;
GRANT INSERT ON "employee" to employeerole;
GRANT SELECT ON "insuranceplan" to employeerole;
GRANT SELECT on "checkk" to employeerole;
GRANT SELECT ON "benefits" TO employeerole;
GRANT UPDATE ON "employee" to employeerole;


CREATE ROLE managerrole with password 'password' LOGIN;
GRANT SELECT on "employee" to managerrole;
GRANT SELECT ON "insuranceplan" to managerrole;
GRANT SELECT on "checkk" to managerrole;
GRANT SELECT ON "benefits" TO managerrole;
GRANT SELECT ON "dependents" TO managerrole;
GRANT SELECT ON "receives" TO managerrole;

create table roles(
username VARCHAR(50),
password VARCHAR(50)
)


CREATE ROLE adminrole with password 'password' LOGIN;
GRANT UPDATE on "employee" to adminrole;
GRANT UPDATE ON "insuranceplan" to adminrole;
GRANT UPDATE on "checkk" to adminrole;
GRANT UPDATE ON "benefits" TO adminrole;
GRANT UPDATE ON "dependents" TO adminrole;
GRANT UPDATE ON "receives" TO adminrole;

SELECT checkk.check_id,checkk.soc_security,checkk.week,checkk.gross,receives.employee_id,((checkk.state_tax)*(checkk.gross)/100),((checkk.federal_tax)*(checkk.gross)/100),(checkk.gross*.025),employee.employee_id,employee.salary_type,employee.benefits_id,benefits._401k_cont,(checkk.gross*benefits._401k_cont/100),insuranceplan.premium_individual,insuranceplan.premium_family
,CASE employee.salary_type
		WHEN 'hourly' THEN (checkk.gross*.075)
	ELSE (checkk.gross*.15)
	END social_sec
FROM checkk JOIN receives ON receives.check_id=CAST(checkk.check_id AS INTEGER)
JOIN employee ON employee.employee_id=receives.employee_id
JOIN benefits ON benefits.benefits_id=employee.benefits_id
JOIN insuranceplan ON insuranceplan.insurance_id=employee.insurance_id;


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

 SELECT soc_security,Sum(gross) FROM checkk
            WHERE year ='2021'
            GROUP By soc_security
            ORDER BY soc_security ASC;


SELECT checkk.soc_security,SUm(receives.bonus) FROM receives
            JOIN checkk ON checkk.check_id=receives.check_id
            GROUP by checkk.soc_security
            ORDER BY soc_security ASC;

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