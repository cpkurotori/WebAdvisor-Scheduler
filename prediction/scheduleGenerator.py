from prediction.classes import Course, Meeting, Section
import datetime

class SectionList:
    def __init__(self,section,course): #Secion object, Course object
        self.section = section
        self.children = []
        self.course = course

    def compareSections(self,compare): #section object, section object
        firstList = splitMeetings(self.section)
        secondList = splitMeetings(compare)
        for meeting in firstList:
            for smeeting in secondList:
                if not compareMeetings(meeting,smeeting):
                    return False
        return True

    def addNonConflict(self,section): #SectionList object, SectionList object
        if self.course == section.course:
            return
        if self.compareSections(section.section):
            if self.children == [] or self.children[0].course == section.course:
                    self.children.append(section)
            else:
                for child in self.children:
                    child.addNonConflict(section)

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
                if duration(first)+duration(second)+allotted>totalSeconds(second.endTime)-totalSeconds(first.startTime):
                    return False
    return True


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
            for section in course.sections:
                sectionNode = SectionList(section,course)
                node.addNonConflict(sectionNode)
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