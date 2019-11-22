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
import subprocess as sp






def camera(yVal):
    count = 1
    countsp = 0
    leftEyeSend,leftEyeRecv = Pipe()
    
    p1 = Process(target = condEye, args=(yVal, leftEyeRecv))
    p1.start()
    
    #Load face detector and predictor, uses dlib shape predictor file
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    #Extract indexes of facial landmarks for the left and right eye
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS['left_eye']
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']

    #Start webcam video capture
    video_capture = cv2.VideoCapture(0)
    
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
            
            if len(faces) == 0:
                print("Faceless")
                     
                if count == 20:
                    print('count>>20')
                    sp.Popen(["aplay /home/pi/Documents/Group4_SMART_TABLE/soundForSOT/noPeople.wav 2>/dev/null"], shell=True)
                    leftEyeSend.close()
                    p1.terminate()
                    time.sleep(0.1)
                    return ''
                else:
                    count +=1
                    moveLinear('stop')
                    continue
                    
                    

            if len(faces) > 1:
#                 print('there are more than one person in the camera')
                moveLinear('stop')
                if countsp == 0:
                    sp.Popen(["aplay /home/pi/Documents/Group4_SMART_TABLE/soundForSOT/morePeople.wav 2>/dev/null"], shell=True)
                    countsp +=1
                continue


            shape = predictor(gray, faces[0])
            shape = face_utils.shape_to_np(shape)

            #Get array of coordinates of leftEye and rightEye
            leftEye = shape[lStart:lEnd]
            
            leftEyeSend.send(leftEye[0][1])
            count = 1
            countsp = 0
            
                
            if cv2.waitKey(1) & 0xFF == ord("q"):
                p1.terminate()
                time.sleep(0.1)
                return
            
            
    except KeyboardInterrupt:
        moveLinear('stop')
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

        if test >= yVal-30 and test <= yVal-10:
            cond = 'stop'
            moveLinear(cond)
            print("Good position")
            countDone+=1
            countDown = 0
            countUp = 0
            if countDone == 10: 
                sp.Popen(["aplay /home/pi/Documents/Group4_SMART_TABLE/soundForSOT/DoneMove.wav 2>/dev/null"], shell=True)
                
                    
        elif test < yVal-40:
            cond = 'up'
            moveLinear(cond)
#             print("Table is moving up")
            countDone = 0
            countDown = 0
            countUp += 1

            if countUp==10:
                sp.Popen(["aplay /home/pi/Documents/Group4_SMART_TABLE/soundForSOT/Up.wav 2>/dev/null"], shell=True)
                
                
        elif test > yVal:
            cond = 'down'
            moveLinear(cond)
#             print("Table is moving down")
            countDone = 0
            countUp = 0
            countDown += 1
            if countDown == 10:
                sp.Popen(["aplay /home/pi/Documents/Group4_SMART_TABLE/soundForSOT/Down.wav 2>/dev/null"], shell=True)
                
                    
    
    
            
            
if __name__ == '__main__':
    start_time = time.time()
    y = distanceUs1()
    x = camera(y)
    
    while x == '':
        cv2.destroyAllWindows()
        time.sleep(3)
        
        x = camera(distanceUs1())
    