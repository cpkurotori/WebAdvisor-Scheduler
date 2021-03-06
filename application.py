from flask import Flask, request
import flask
from flaskext.mysql import MySQL
from HTML import createHTML
from HTML import testcase
from HTML import addEntry
from HTML import getSchedule
import predtest
from prediction.scheduleGenerator import scheduleGenerator
import os


#Initialized the Database using Flask
# YOU MUST HAVE A DATABASE FOR INFORMATION TO BE STORED IN
# CHANGE THESE VALUES IF YOUR SET UP IS DIFFERENT
application = Flask(__name__)
mysql = MySQL()
application.config['MYSQL_DATABASE_DB'] = "Schedule"
application.config['MYSQL_DATABASE_HOST'] = "localhost"
application.config['MYSQL_DATABASE_USER'] = "root"
application.config['MYSQL_DATABASE_PASSWORD'] = "password"
mysql.init_app(application)


# this is the first route that will be called when the website is accessed
@application.route("/")
def index():
    createHTML.createHome()
    return application.send_static_file("home.html")

#this is the route that will be called when the "Generate" button is clicked
@application.route("/calendar", methods=["post"])
def calendar():
    #tempTest = testcase.testcase
    tempTest = scheduleGenerator(predtest.testcase) #this is merely a test case of a lists of schedules with lists of courses
    index = addEntry.addEntry(tempTest,mysql)  
    createHTML.createCalendar(len(tempTest),index)
    return application.send_static_file("calendar.html")

#When the calendar performs an AJAX request to /selectSchedule, this will run
@application.route("/selectSchedule", methods=["get"])
def selectSchedule():    
    index = int(request.args['i'])
    schedule = int(request.args['s'])
    selected = getSchedule.convertToJSON(schedule, index, mysql)
    print (selected)
    return selected

@application.route("/deleteEntry",methods=["get"])
def deleteEntry():
    db_id = int(request.args['i'])
    print("going to delete..."+str(db_id))
    addEntry.removeEntry(db_id,mysql)
    return "DELETED"

# run the application.
if __name__ == "__main__":
	# Setting debug to True enables debug output. This line should be
	# removed before deploying a production application.
	application.debug = True
	application.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
