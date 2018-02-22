# written by oreanroy  https://www.linkedin.com/in/rahul-kumar-roy-7b102512a/

import serial # you need to install the pySerial use pip`
import time
import cv2 
import numpy as np

#open cv variable initialization
cap = cv2.VideoCapture(0)

lower_green = np.array([45,140,50]) 
upper_green = np.array([75,255,255])

lower_red = np.array([160,140,50]) 
upper_red = np.array([180,255,255])

lower_blue = np.array([110,50,50]) # more tight range will be developed once balls are made
upper_blue = np.array([125,240,2])

countred = 0
countgreen = 0  # variables to only give output once ball count increaes 5
countblue = 0


# your Serial port should be different!
arduino = serial.Serial('/dev/ttyACM0', 9600)

def onOffFunction():
        #command = raw_input("Type something..: (on/ off / bye )");
	command = ballsearch()
	if command =="on":
		print "The LED is on... red ball found" # go to deafault position
		time.sleep(1) 
		arduino.write('H') 
		onOffFunction()
	elif command =="off":  # go to second position
		print "The LED is off... blue ball found"
		time.sleep(1) 
		arduino.write('L')
		onOffFunction()
	elif command =="bye": # go to golden ring
		print "See You!..."
		time.sleep(1) 
		arduino.close()
	else:
		print "Sorry..type another thing..!"
		onOffFunction()

time.sleep(2) #waiting the initialization...


def ballsearch():
	global countred 
	global countblue # making the variables global, python
	global countgreen 
	success,frame = cap.read()  
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	#hsv = cv2.medianBlur(hsv,5)
	imgThreshHighred = cv2.inRange(hsv, lower_red, upper_red) #masking other color
	imgThreshHighgreen = cv2.inRange(hsv, lower_green, upper_green)
	imgThreshHighblue = cv2.inRange(hsv, lower_blue, upper_blue)
	circlesred = cv2.HoughCircles(imgThreshHighred,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=10,maxRadius=0)
	circlesblue = cv2.HoughCircles(imgThreshHighblue,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=10,maxRadius=0)# finding circles
	circlesgreen = cv2.HoughCircles(imgThreshHighgreen,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=10,maxRadius=0)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		cv2.destroyAllWindows() 	# 1 or q pressed stop terminal
	if circlesred is not None:
        	#print "found red"
		countred+=1
		if countred>5:
			#print "circlesred"
			return("on")            # red ball found go to deault return from function to onOFff function
			countred = 0
		return(onOffFunction())
	if circlesgreen is not None:
	#	print "found green"
		countgreen+=1
		if countgreen>5:
			#print "circlesGreen"
			return("off")
			countgreen = 0
		return(onOffFunction())
	
	if circlesblue is not None:
		countblue+=1
		if countblue>5:		
			#print "found blue"
			return("bye")
			countblue = 0
		return(onOffFunction())
	#	print circlesblue
	else:
		print "no ball"
		return(ballsearch()) 


	if cv2.waitKey(1) & 0xFF == ord('q'):
		cv2.destroyAllWindows()

onOffFunction()
cv2.destroyAllwindows()

