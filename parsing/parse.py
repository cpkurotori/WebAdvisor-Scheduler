from bs4 import BeautifulSoup
from HTML import getDept
import pymysql
from Templates import classes


def parseHTML(term,depts=getDept.gatherFields().dept):
	try:
		cnx = pymysql.connect(user='root', password='password', host='localhost',database='Schedule')
	except:
		print ("Failed to open connection to database.")
		exit(1)
	cur = cnx.cursor()
	for dept in depts:
		if not checkTable (cur,term):
			continue
		if not importDept(cur,term,dept):
			print ("Failed to import",dept)
			continue
	cur.close()
	cnx.close()
	
	
def checkTable (cur,term):
	createIfNone = 'CREATE TABLE IF NOT EXISTS '+term+' (title VARCHAR(40), dept VARCHAR(6), courseNum VARCHAR(6), sectionNum VARCHAR(6), description VARCHAR(100), credits DECIMAL(3,2), startD DATE, endD DATE, meetingInfo VARCHAR(255), faculty VARCHAR(255), comments VARCHAR(255),section_id INT(11) NOT NULL AUTO_INCREMENT,PRIMARY KEY (section_id));'
	try:
		cur.execute(createIfNone)
	except:
		print ("Failed to create table.")
		return False
	return True

def importDept(cur,term,dept):
	with open('courselists/'+term+'/'+dept+'.txt','r') as file:
		coursesHTML = file.read()
	coursesList = coursesHTML[coursesHTML.find('\n-------\n'):].split('\n-------\n')
	for course in coursesList:
		if course == '':
			continue
		elif not parse(cur,course):
			return False
	return True
		
def parse(cur,course):
	soup = BeautifulSoup(course,'html.parser')
	title = soup.find(id="VAR1").get_text()
	dept,courseNum,sectionNum= map(str,soup.find(id="VAR2").get_text().split('-'))
	description = soup.find(id="VAR15").get_text()
	credits = float(soup.find(id="VAR4").get_text())
	startD = soup.find(id="VAR6").get_text()
	endD = soup.find(id="VAR7").get_text()
	meetings = None
	#meetings = parseMeeting (soup.find(id="LIST_VAR12_1").get_text()):
	i,faculty = 0,[]
	while True:
		try:
			faculty.append(soup.find(id="LIST_VAR7_"+str(i+1)).get_text())
			i += 1
		except:
			print(i,"teacher(s) found.")
			break
	return title,dept,courseNum,sectionNum,description,credits,startD,endD,meetings,faculty
	
def parseMeeting(meetingInfo):
	pass