from prediction.classes import Course, Meeting, Section
import datetime

""" reference for objects:

class Course:
    def __init__(self,sections,credits,subject,course_number,title,desc):
        self.sections = sections # list of section objects #
        self.credits = credits # string #ex "" #
        self.subject = subject #string 
        self.course_number = course_number #string
        self.title = title
        self.desc = desc # string schedule description


class Section:
    def __init__(self,startDate,endDate,meetings,section_number):
        self.startDate = startDate # date(2017,3,5) == March 5th,2017
        self.endDate = endDate # date(2017,4,15) == April 15th, 2017
        self.meetings = meetings  #list of meeting objects
        self.section_number = section_number # string # "02" #

class Meeting:
    def __init__(self,meetingType,campus,startTime,endTime,professorName,room,recurrence):
        self.meetingType = meetingType # string # "Lecture"
        self.campus = campus # string # "Newark"
        self.startTime = startTime #Time object  datetime.time()
        self.endTime = endTime #Time object  datetime.time()
        self.professorName = professorName #name string
        self.room = room #string
        self.recurrence = recurrence #list of strings
"""



class SectionList:
    def __init__(self,section,course): #Secion object, Course object
        self.section = section
        self.children = []
        self.course = course

def splitMeetings(section): #section object
    meetingList = []
    for meeting in section.meetings:
            meetingList.append(meeting)
    return meetingList

def totalSeconds(time): # must be datetime.time object
    return 3600*time.hour+60*time.minute+time.second

def duration(meeting): # meeting object
    return totalSeconds(meeting.endTime)-totalSeconds(meeting.startTime)

def firstEarlier(first,second):
    return totalSeconds(second.startTime)-totalSeconds(first.startTime) > 0

def compareMeetings(meeting,comparison): #list of meeting objects, meeting object
    skips = ['TBA','TBADISTANCE LEARNING VIA WEB','TBD']
    if firstEarlier(meeting,comparison):
        first,second = meeting,comparison
    else:
        first,second = comparison,meeting    
    for recurrence in first.recurrence:
        if recurrence in second.recurrence:
            if (not first.campus in skips) and (not second.campus in skips):
                if first.campus != second.campus:
                    allotted = 900
                else:
                    allotted = 0
                print ("First: "+str(first.professorName)+':'+str(first.meetingType))
                print ("Second: "+str(second.professorName)+':'+str(second.meetingType))
                print ("Duration first: "+str(duration(first)))
                print ("Duration second: "+str(duration(second)))
                print ("Allotted Transfer: "+str(allotted))
                print ("Sum: "+str(duration(first)+duration(second)+allotted))
                print ("Actual time between start and end: "+str(totalSeconds(second.endTime)-totalSeconds(first.startTime)))
                if duration(first)+duration(second)+allotted>totalSeconds(second.endTime)-totalSeconds(first.startTime):
                    print ("Meeting Bad...")
                    return False
                else:
                    print ("Meeting Good...")
        else:
            print ("Different Days. Meeting Good...")
    return True

def compareSections(first,second): #section object, section object
    firstList = splitMeetings(first)
    secondList = splitMeetings(second)
    for meeting in firstList:
        for smeeting in secondList:
            if not compareMeetings(meeting,smeeting):
                return False
    return True

def addNonConflict(root,section): #SectionList object, SectionList object
    if root.course == section.course:
        return
    if compareSections(root.section,section.section):
        if root.children == [] or root.children[0].course == section.course:
                root.children.append(section)
                print ("Appending section...")
                print ("Course: "+section.course.title+"-"+section.course.course_number)
                print ("Section: "+section.section.section_number)
        else:
            for child in root.children:
                addNonConflict(child,section)

def sumSchedules (root):
    if root.children == []:
        return 1
    lsum = 0
    for child in root.children:
        lsum += sumSchedules(child)
    return lsum


def convertNode (scheduleList,root):
    if root.children==[]:
        scheduleList.append([root])
        return 1
    count = 0
    for child in root.children:
        count+=convertNode(scheduleList,child)
    for i in range(count):
        scheduleList[-1*(i+1)].append(root)
    return count

def scheduleGenerator(courseList):
    nodeList = []
    for section in courseList[0].sections:
        sectionNode = SectionList(section,courseList[0])
        nodeList.append(sectionNode)
    for node in nodeList:   
        for course in courseList[1:]:
            print (course.title)
            for section in course.sections:
                sectionNode = SectionList(section,course)
                addNonConflict(node,sectionNode)
    scheduleSectionList = []
    for node in nodeList:
        tempList = []
        convertNode (tempList,node)
        scheduleSectionList += tempList
    length = len(scheduleSectionList)
    for i in range(length):
        if len(scheduleSectionList[length-1-i])<len(courseList):
            scheduleSectionList.pop(length-1-i)
    scheduleList = []
    for schedule in scheduleSectionList:
        tempSchedule = []
        for section in schedule:
            section.course = Course(section.section,section.course.credits,section.course.subject,section.course.course_number,section.course.title,section.course.desc)
            tempSchedule.append(section.course)
        scheduleList.append(tempSchedule)
    return scheduleList

"""
from prediction.schedule_generator_datatype import compareSections,SectionList,addNonConflict
from predtest import C1S1,C1S2,C1S3,C1,C2,C3,C2S1,C2S2,C2S3,C3S1,C3S2,C3S3
compareSections (C1S1,C2S1) #FALSE
compareSections (C1S1,C3S1) #FALSE
compareSections (C1S1,C3S3) #TRUE
compareSections (C2S1,C2S1) #FALSE
compareSections (C2S1,C3S1) #FALSE
compareSections (C2S1,C3S3) #TRUE
compareSections (C1S1,C2S1) #FALSE
compareSections (C1S1,C2S2) #FALSE
compareSections (C1S1,C2S3) #FALSE
one = SectionList(C1S1,C1) 
two = SectionList(C1S2,C1)
three = SectionList(C3S3,C3)
addNonConflict(one,two)
addNonConflict(one,three)



import predtest
predtest.testcase
from prediction.schedule_generator_datatype import scheduleGenerator
sched = scheduleGenerator(predtest.testcase)

def printCourse (schedlist,schedule,course):
    return schedlist[schedule][course].subject+schedlist[schedule][course].course_number+'-'+schedlist[schedule][course].sections.section_number

def printSchedule (schedlist,schedule):
    print (printCourse(schedlist,schedule,0)+','+printCourse(schedlist,schedule,1)+','+printCourse(schedlist,schedule,2))

def printList (schedlist):
    for i in range (len(schedlist)):
        printSchedule(schedlist,i)

printList(sched)

"""