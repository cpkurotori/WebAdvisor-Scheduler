from bs4 import BeautifulSoup
from HTML import getDept
import pymysql
from Templates import classes
import re, os


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
		elif dept=='':
			continue
		elif not os.path.exists('courselists/'+term+'/'+dept+'.txt'):
			continue
		elif not importDept(cur,term,dept):
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
	#print (coursesList)
	coursesInfoList = []
	for course in coursesList:
		if course == '':
			continue
		title,dept,courseNum,sectionNum,description,credits,startD,endD,meetings,faculty = parse(cur,course)
		coursesInfoList.append({
			'title':title,
			'dept':dept,
			'courseNum':courseNum,
			'sectionNum':sectionNum,
			'description':description,
			'credits':credits,
			'startD':startD,
			'endD':endD,
			'meetings':meetings,
			'faculty':faculty
		})
		# elif not parse(cur,course):
		# 	return False
	#print (coursesInfoList)
	return True
		
def parse(cur,course):
	i,faculty = 0,[]
	try:
		soup = BeautifulSoup(course,'html.parser')
		title = soup.find(id="VAR1").get_text()
		debug = soup.find(id="VAR2").get_text().split('-')
		#print (debug)
		dept,courseNum,sectionNum = map(str,debug)#soup.find(id="VAR2").get_text().split('-'))
		description = soup.find(id="VAR15").get_text()
		credits = float(soup.find(id="VAR4").get_text())
		startD = convertDate(soup.find(id="VAR6").get_text().split(' '))
		endD   = convertDate(soup.find(id="VAR7").get_text().split(' '))
		meetings = parseMeeting (startD,endD,soup.find(id="LIST_VAR12_1").get_text())
		while True:
			try:
				faculty.append(soup.find(id="LIST_VAR7_"+str(i+1)).get_text())
				i += 1
			except:
				print(i,"teacher(s) found.")
				break
		return title,dept,courseNum,sectionNum,description,credits,startD,endD,meetings,faculty	
	except:
		print("Unable to populate fields...")
		return 'Error','Error','Error','Error','Error','Error','Error','Error','Error','Error'

	
def parseMeeting(startD,endD,meetingInfo):
	meetingList = []
	meetings = re.split(r'\d\d/\d\d/\d\d\d\d-\d\d/\d\d/\d\d\d\d',meetingInfo)
	#meetings = meetingInfo.split(startD+'-'+endD)
	for meeting in meetings:
		if meeting == '':
			continue
		elif 'WEB' in meeting: # 06/19/2017-08/10/2017 Text One-Way (72) Days TBA, Times TBADISTANCE LEARNING VIA WEB, Room WEB
			meetingList.append({
				'type':'Text One-Way (72)',
				'recurr':'Days TBA',
				'time':'Times TBA',
				'campus':'DISTANCE LEARNING VIA WEB',
				'location':'Room WEB'})
			continue
		print (meeting)
		meetingTypeSpan = re.search(r'\w+(\s\w+)?\s\(\d.\)',meeting).span()
		meetingRecurrSpan = re.search(r'(\w+day,?\s)+',meeting).span()
		meetingTimeSpan = re.search(r'\d.:\d.\w.\s-\s\d.:\d.\w.',meeting).span()
		locP = re.compile(r',\s\w+((\s\w+)+)?,')
		meetingCampusSpan = locP.search(meeting,meetingTimeSpan[1]).span()
		meetingList.append({
			'type':meeting[meetingTypeSpan[0]:meetingTypeSpan[1]],
			'recurr':meeting[meetingRecurrSpan[0]:meetingRecurrSpan[1]-1],
			'time':meeting[meetingTimeSpan[0]:meetingTimeSpan[1]],
			'campus':meeting[meetingCampusSpan[0]+2:meetingCampusSpan[1]-1],
			'location':meeting[meetingCampusSpan[1]:len(meeting)]
		})
	return meetingList
	
def convertDate(dateList):
	day,month,year = map(str,dateList)
	months = {'January':'01','February':'01','March':'03','April':'04','May':'05','June':'06','July':'07','August':'08','September':'09','October':'10','November':'11','December':'12'}
	month = months[month]
	return month+'/'+day+'/'+year
	
	
# from parsing.parse import parseMeeting
# meetingInfo = '08/30/2017-06/13/2018 Lecture (02) Monday, Tuesday, Thursday, Friday 10:26AM - 11:20AM, Mission San Jose High School, Room MSJ-N4 08/30/2017-06/13/2018 Laboratory (04) Wednesday 10:52AM - 11:40AM, Mission San Jose High School, Room MSJ-N4'
# startD = '06/19/2017'
# endD = '08/10/2017'
# parseMeeting(startD,endD,meetingInfo)