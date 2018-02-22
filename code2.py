import cv2
import numpy as np
import RPi.GPIO as GPIO
red = 8
yellow = 9

GPIO.setup(GPIO.BOARD)
GPIO.Setup(red, GPIO.OUT,initial=0)
GPIO.Setup(yellow, GPIO.OUT,initial=0)
# avvailable digital pins on the pi 4 7 8 9 10 11 14 15 17 18 22 23 24
cap = cv2.VideoCapture(0)

lower_red = np.array([160,140,50])
upper_red = np.array([180,255,255])

lower_yellow = np.array([20,100,100])
upper_yellow = np.array([30,255,255])

countRed = 0
countYellow = 0
redFound = False

def ballSearch():

	while(True):
		global countRed
		global countYellow	
	
		success,frame = cap.read()
		hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
		hsv = cv2.medianBlur(hsv,5)
		imgThreshHighRed = cv2.inRange(hsv, lower_red, upper_red)
		imgThreshHighYellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
		circlesRed = cv2.HoughCircles(imgThreshHighRed, cv2.cv.CV_HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=10,maxRadius=0)
		circlesYellow = cv2.HoughCircles(imgThreshHighYellow,cv2.cv.CV_HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=10,maxRadius=0)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			break
		if circlesRed is not None:
			countRed+=1
			if countRed>2:
				countRed=0
				print "Red ball found"
				GPIO.output(red,GPIO.HIGH)
				redFound = True
		if circlesYellow is not None and redFound:
			countYellow+=1
			if countYellow>2:
				countYellow=0 
				print "yellow ball found"
				GPIO.output(yellow,GPIO.HIGH)
		else:
			print "no ball"
		if cv2.waitKey(1) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			break
ballSearch()
cv2.destroyAllWindows()
