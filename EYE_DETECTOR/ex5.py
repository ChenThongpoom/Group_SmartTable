'Credit : Mohit Singh'

#Import necessary libraries
from scipy.spatial import distance
from imutils import face_utils
import numpy as np
import time
import dlib
import cv2
import threading
from mosSerial import distanceUs1, moveLinear
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

            cv2.imshow('EYE_DETECTION',frame )
            
            if len(list(list(faces))) == 0:
                print("Faceless")
                     
                if count == 10:
                    print('count>>10')
#                     call(["aplay /home/pi/Desktop/Group4_SMART_TABLE-master/soundForSOT/noPeople.wav 2>/dev/null"], shell=True)
                    leftEyeSend.close()
                    p1.terminate()
                    time.sleep(1)
#                     p1.join()
#                     video_capture.release()
#                     cv2.destroyWindow("EYE_DETECTION")
                    return ''
                else:
                    count +=1
                    time.sleep(1)
                    continue

            elif len(list(list(faces))) > 1:
                print('there are more than one person in the camera')
#                 call(["aplay /home/pi/Desktop/Group4_SMART_TABLE-master/soundForSOT/morePeople.wav 2>/dev/null"], shell=True)
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
                
                
            #Show video feed
            
            
            
            if cv2.waitKey(1) & 0xFF == ord("q"):
                p1.terminate()
                time.sleep(0.1)
                return
            
            
            
    except KeyboardInterrupt:
        p1.terminate()
        time.sleep(0.1)
        return
    
    
def condEye(yVal,left):
    
#     leftEyeQueue = queue.Queue()
#     
#     t1 = threading.Thread(target=camera, args=(yVal,leftEyeQueue,))
#     t1.start()
    try:
        cond = ''
        count = 0
        while True:
            test = left.recv()
#             check = pipeCondRecv3.recv()  # pipe receive the condition from camera function to loop the process
#             print(yVal,' is y val')
#             print("Test is ", test)
            if test >= yVal-40 and test <= yVal:
                cond = 'stop'
                moveLinear(cond)
                print("Good position")
#                 call(["aplay /home/pi/Desktop/Group4_SMART_TABLE-master/soundForSOT/DoneMove.wav 2>/dev/null"], shell=True)
#                 count += 1
#                 if count == 5:
#                     print("do nothing")
#                     return  # pipe stop the p2 process
                
            elif test < yVal-40:
                cond = 'up'
                moveLinear(cond)
                print("Table is moving up")
#                 call(["aplay /home/pi/Desktop/Group4_SMART_TABLE-master/soundForSOT/Up.wav 2>/dev/null"], shell=True)
            elif test > yVal:
                cond = 'down'
                moveLinear(cond)
                print("Table is moving down")
#                 call(["aplay /home/pi/Desktop/Group4_SMART_TABLE-master/soundForSOT/Down.wav 2>/dev/null"], shell=True)

    except KeyboardInterrupt:
        return 
    
            
            
if __name__ == '__main__':
    y = distanceUs1()
    x = camera(y)
    while x == '':
        time.sleep(1)
        x = camera(distanceUs1())
