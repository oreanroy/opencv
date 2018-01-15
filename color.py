import cv2
import numpy as np
#import cv2.cv as cv
cap = cv2.VideoCapture(0)
while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV 
    lower_red = np.array([160,140,50]) 
    upper_red = np.array([180,255,255])
    
    lower_green = np.array([65,60,60])
    upper_green = np.array([80,255,255])

    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])
    

    imgThreshHighred = cv2.inRange(hsv, lower_red, upper_red)
    imgThreshHighgreen = cv2.inRange(hsv, lower_green, lower_green)
    imgThreshHighblue = cv2.inRange(hsv, lower_blue, lower_blue)

    #imgray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #thresh = 18
    #edges = cv2.Canny(imgray,thresh,thresh*3)

    #circles = cv2.HoughCircles(imgThreshHigh, cv.CV_HOUGH_GRADIENT, 1, 500, 25, 75, 5, 15)
    circlesred = cv2.HoughCircles(imgThreshHighred,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)
    circlesgreen = cv2.HoughCircles(imgThreshHighgreen,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)
    circlesblue = cv2.HoughCircles(imgThreshHighblue,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)
    maxRadius= 0
    xc = 0.00
    yc = 0.00
    foundred = False
    foundgreen = False
    foundblue = False
    print circlesred+"red circle"
    print circlesgreen+"green circle"
    print circlesblue+"blue circle" 
    if circlesred is not None:
        foundred = True
        #print circles
    
    if circlesblue is not None:
        foundblue = True
        #print circles
    if circlesgreen is not None:
        foundgreen = True
        #print circles
    
        
    if foundred: 
        print "ball detected is red"
    if foundgreen:
        print "green ball detected"
    if foundblue:
        print "blue ball detected"
    else: 
        print "no ball" 
    #cv2.imshow('frame',frame)
    #cv2.imshow('edges',edges)
    #cv2.imshow('circles',circlesred)
    #k = cv2.waitKey(5) & 0xFF
    #if k == 27:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
