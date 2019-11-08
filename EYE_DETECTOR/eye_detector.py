'Credit : Mohit Singh'

#Import necessary libraries
from scipy.spatial import distance
from imutils import face_utils
import numpy as np
import time
import dlib
import cv2
import threading
from serialCommu import distanceUs1, moveLinear
#from voiceCommandStates import main


#mainVoice('The system start running')
#Load face detector and predictor, uses dlib shape predictor file
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

#Extract indexes of facial landmarks for the left and right eye
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS['left_eye']
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']

#Start webcam video capture
video_capture = cv2.VideoCapture(0)

#Give some time for camera to initialize(not required)
time.sleep(0)


# y = distanceUs1()
# 
# print(y)

def camera(yVal):
    cond = ''
    while(True):
        #Read each frame and flip it, and convert to grayscale
        ret, frame = video_capture.read()
        frame = cv2.flip(frame,1)
        frame = cv2.resize(frame, (300, 240))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #Detect facial points through detector function
        faces = detector(gray, 0)

        #making reference lines
        frame = cv2.line(frame, (0,yVal-40),(1279,yVal-40),(0,0,255),2)
        frame = cv2.line(frame, (0,yVal),(1279,yVal),(0,0,255),2)
        
#         cv2.imshow('EYE_DETECTION',frame )
            
            
        #Detect facial points
        for face in faces:

            shape = predictor(gray, face)
            shape = face_utils.shape_to_np(shape)

            #Get array of coordinates of leftEye and rightEye
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]


            #Use hull to remove convex contour discrepencies and draw eye shape around eyes
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

            print(leftEye)
#             print(leftEye[0][1]) #focus on y coordinate
            cv2.imshow('EYE_DETECTION',frame )
            
            if (leftEye[0][1]) >= yVal-40 and (leftEye[0][1]) <= yVal:
                cond = 'stop'
                print("Good position")
#                 print(moveLinear(cond))
            elif (leftEye[0][1]) < yVal-40:
                cond = 'up'
                print("Table is moving up")
#                 moveLinear(cond)
            elif (leftEye[0][1]) > yVal:
                cond = 'down'
                print("Table is moving down")
#                 moveLinear(cond)
                
            
            
        #Show video feed
#         cv2.imshow('EYE_DETECTION',frame )
        if cv2.waitKey(1) & 0xFF == ord("q"):
            time.sleep(2)

            print('New Distance detecting... ')
            return
    

        elif len(list(list(faces))) > 1:
            print("there are more than one person")
#             mainVoice('There are more than one person in the frame')
        elif len(list(list(faces))) == 0:
            print('faceless')


#Finally when video capture is over, release the video capture and destroyAllWindows

camera(distanceUs1())
video_capture.release()
cv2.destroyAllWindows()

