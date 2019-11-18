'Credit : Mohit Singh'

#Import necessary libraries
from scipy.spatial import distance
from imutils import face_utils
import numpy as np
import time
import dlib
import cv2
import threading
from SerialFinal import distanceUs1, moveLinear
from multiprocessing import Process , Pipe
import threading
import queue
from num2words import num2words
from subprocess import call
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

def camera(yVal):
    count = 1
    leftEyeSend,leftEyeRecv = Pipe()
    
    p1 = Process(target = condEye, args=(yVal, leftEyeRecv))
    p1.start()
    try:
        while True:
            
            #Read each frame and flip it, and convert to grayscale
            ret, frame = video_capture.read()
            frame = cv2.flip(frame,1)
            frame = cv2.resize(frame, (300, 240))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
            
            faces = detector(gray, 0)
    


            #making reference lines
            frame = cv2.line(frame, (0,yVal-40),(1279,yVal-40),(0,0,255),2)
            frame = cv2.line(frame, (0,yVal),(1279,yVal),(0,0,255),2)
            
            #Show video feed
            cv2.imshow('EYE_DETECTION',frame )
            
            if len(list(list(faces))) == 0:
                print("Faceless")
                     
                if count == 50:
                    print('count>>50')
#                     call(["aplay /home/pi/Documents/Group4_SMART_TABLE/soundForSOT/soundForSOT/noPeople.wav 2>/dev/null"], shell=True)
                    leftEyeSend.close()
                    p1.terminate()
                    time.sleep(0.1)
#                     p1.join()
#                     video_capture.release()
#                     cv2.destroyWindow("EYE_DETECTION")
                    return ''
                else:
                    count +=1
                    continue
                    

            elif len(list(list(faces))) > 1:
                print('there are more than one person in the camera')
#                 call(["aplay /home/pi/Documents/Group4_SMART_TABLE/soundForSOT/soundForSOT/morePeople.wav 2>/dev/null"], shell=True)
                time.sleep(2)
                continue

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
                
                
                
                time.sleep(0.05)
                
                leftEyeSend.send(leftEye[0][1])
                count = 1
                
                
            
            if cv2.waitKey(1) & 0xFF == ord("q"):
                p1.terminate()
                time.sleep(0.1)
                return
            
            
            
    except KeyboardInterrupt:
        leftEyeSend.close()
        p1.terminate()
        time.sleep(0.1)
        video_capture.release()
        cv2.destroyAllWindows()
        return
    
    
def condEye(yVal,left):
    
    
    cond = ''
    countDone = 0
    countUp = 0
    countDown = 0
    while True:
        test = left.recv()

        if test >= yVal-40 and test <= yVal:
            cond = 'stop'
            moveLinear(cond)
            print("Good position")
            if countDone == 0: 
#                     call(["aplay /home/pi/Documents/Group4_SMART_TABLE/soundForSOT/soundForSOT/DoneMove.wav 2>/dev/null"], shell=True)
                countDone += 1    
            
        elif test < yVal-40:
            cond = 'up'
            moveLinear(cond)
            print("Table is moving up")
            countUp += 1
            if countUp == 5:
#                     call(["aplay /home/pi/Documents/Group4_SMART_TABLE/soundForSOT/soundForSOT/Up.wav 2>/dev/null"], shell=True)
                countUp = 0
        elif test > yVal:
            cond = 'down'
            moveLinear(cond)
            print("Table is moving down")
            countDown += 1
            if countDown == 5:
#                     call(["aplay /home/pi/Documents/Group4_SMART_TABLE/soundForSOT/soundForSOT/Down.wav 2>/dev/null"], shell=True)
                countDown = 0
                
                    
    
    
            
            
if __name__ == '__main__':
    y = distanceUs1()
    x = camera(y)
    while x == '':
        time.sleep(1)
        x = camera(distanceUs1())
    
