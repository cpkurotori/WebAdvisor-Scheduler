import sys
import pullCourses
import time

if len(sys.argv) == 2:
    #pullCourses.updateDepartments(sys.argv[1])
    #time.sleep(3)
    pullCourses.updateDepartments(sys.argv[1],skips='courselists/'+sys.argv[1]+'/good.txt')
    time.sleep(3)
    pullCourses.updateDepartments(sys.argv[1],skips='courselists/'+sys.argv[1]+'/good.txt')
    time.sleep(3)
    pullCourses.updateDepartments(sys.argv[1],skips='courselists/'+sys.argv[1]+'/good.txt')
    time.sleep(3)
    pullCourses.updateDepartments(sys.argv[1],skips='courselists/'+sys.argv[1]+'/good.txt')
    time.sleep(3)
else:
    print("Invalid number of arguments. 2 needed ("+str(len(sys.argv)),"given).")