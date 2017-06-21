from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import os
import re
from datetime import date
from bs4 import BeautifulSoup
from HTML import getDept

# updateDepartments(term,depts=getDept.gatherFields().dept)
# term = YYYYTT i.e. 2017SU - string
# depts = ditionary of department codes : department - both are strings
# returns boolean - true for success
# in folder courselists, there is a course list for each department for a given term

def updateDepartments(term,depts=getDept.gatherFields().dept):
	print ("Initializing browser...")
	# browser = webdriver.Chrome() # use ChromeDriver
	browser = webdriver.PhantomJS('phantomjs') # use PhantomJS - GhostDriver
	browser.implicitly_wait(5)
	for dept in depts:
		print ("Working on dept:",dept+'|')
		if dept == '':
			continue
		tries = 0
		success = False
		while not success and tries < 2:
			success = gatherDept(term,dept,browser)
			tries += 1
			print("Try",tries)
		if not success and tries == 2:
			print("Failed to get dept",dept+'|')
			continue
	
# gatherDept(term, dept)
# term = YYYYTT i.e. 2017SU - string
# dept = department code - string
# returns boolean - true for success
# navegates to the page of all courses for a specified dept and term
def gatherDept(term,dept,browser):
	try:
		navegateSearch(browser)
	except:
		return False
	try:
		print("Selecting",term)
		Select(browser.find_element_by_id('VAR1')).select_by_value(term)
		print("Selecting",'|'+dept+'|')
		Select(browser.find_element_by_id('LIST_VAR1_1')).select_by_value(dept)
		print("Clicking submit")
		browser.find_element_by_name('SUBMIT2').click()
	except:
		return False
	return getCourseHTML(term,dept,browser)
	
	
	
# def navegateSearch(browser)
# browser = selenium.webdriver.phantomjs.webdriver.WebDriver session
# opens up to the Search for Sections page on webAdvisor
def navegateSearch(browser):
	print("Opening webadvisor...")
	browser.get('https://webadvisor.ohlone.edu')
	print("Navegating to Students...")
	browser.find_element_by_link_text("Students").click()
	print("Navegating to Search for Sections...")
	browser.find_element_by_link_text("Search for Sections").click()
	
# getCourseHTML(browser)
# term = YYYYTT i.e. 2017SU - string
# dept = department code - string
# browser = selenium.webdriver.phantomjs.webdriver.WebDriver session
# saves html for each course in that dept to a file called courselists/[TERM][DEPT].txt
def getCourseHTML(term,dept,browser):
	soup_html = BeautifulSoup(browser.page_source,'html.parser')
	try:
		end = int(re.findall(r'Page [\w?]+ of [\w?]+',str(soup_html))[0].split(' ')[-1])
	except:
		return False
	if not os.path.exists(os.path.dirname('courselists/'+term+'/')):
	    try:
	        os.makedirs(os.path.dirname('courselists/'+term+'/'))
	    except:
	    	return False
	f = open('courselists/'+term+'/'+dept+'.txt','w')
	f.write(dept+ " courses for "+term+' updated: '+str(date.today())+'\n----------------------------------\n\n-------\n')
	home = browser.window_handles[0]
	for page in range(end):
		done = False
		print("Working on page "+str(page+1))
		for i in range(20):
			print("Working on course "+str(i+1))
			try:
				browser.find_element_by_id('SEC_SHORT_TITLE_'+str(i+1)).click()
			except:
				done = True
				break
			getPage(browser,f)
			browser.switch_to_window(home)
			if not done:
				browser.find_element_by_xpath('//*[@id="GROUP_Grp_WSS_COURSE_SECTIONS"]/table[1]/tbody/tr/td[1]/input[3]').click()
	f.close()
	return True

# getPage(browser,file)
# browser = selenium.webdriver.phantomjs.webdriver.WebDriver session
# file = io opened file for writing
# writes the html to a file
def getPage(browser,file):
	try:
		browser.switch_to_window(browser.window_handles[-1])
		#print("Course recorded.")
		file.write(browser.page_source)
		file.write('\n-------\n')
		browser.close()
	except:
		return False
	return True
