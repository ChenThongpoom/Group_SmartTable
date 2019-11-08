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
from multiprocessing import Process , Pipe
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

def camera(pipeCamRecv,pipeLinSend3,pipeMainSend4):
    try:
        yVal = 0
        while yVal == 0:
            yVal = pipeCamRecv.recv()  #pipe receive distance from main function to make the y coordinate
            print(yVal)
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



            if len(list(list(faces))) > 1:
                
                print('there are more than one person in the camera')
                pipeMainSend4.send('again')  # pipe send data to main function to check the condition
                
            elif len(list(list(faces))) == 0 :
                
                pipeMainSend4.send('again')  # pipe send data to main function to check the condition
                
                
                
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
                
                
                print(leftEye[0][1])
                time.sleep(0.05)
                
                pipeLinSend3.send(leftEye[0][1])  # send the lefteye position to main function to check the condition
                
            
                

                
            #Show video feed
            cv2.imshow('EYE_DETECTION',frame )
            if cv2.waitKey(1) & 0xFF == ord("q"):
    #             time.sleep(2)
    #             #mainVoice('There is nobody in the frame')
    #             print('New Distance detecting... ')
    #             #mainVoice('Start new distance detecting')
    #             dis = distanceUs1()
    #             return camera(dis)
                pipeMainSend4.send('kill') # pipe send data to main function to check the condition
                
            
    #         if len(list(list(faces))) == 0:
    #             time.sleep(2)
    #             mainVoice('There is nobody in the frame')
    #             print('New Distance detecting... ')
    #             mainVoice('Start new distance detecting')
    #             dis = distanceUs1()
    #             return camera(dis)

    #         elif len(list(list(faces))) > 1:
    #             print("there are more than one person")
    #             p1.is_alive()
    #             p2.is_alive()
    #             p1.stop()
    #             p2.stop()
    #             mainVoice('There are more than one person in the frame')
    except KeyboardInterrupt:
        return
    
    
def condEye(pipeCamRecv,pipeLinRecv5,pipeMainSend4):
    try:
        cond = ''
        count = 0
        yVal = pipeCamRecv.recv()  #pipe receive distance from main function to check the condition with the leftEye value
        while True:
            test = pipeLinRecv5.recv()  # pipe receive the leftEye value from the main function
            print(yVal,' is y val')
            print("Test is ", test)
            if test >= yVal-40 and test <= yVal:
                cond = 'stop'
                moveLinear(cond)
                print("Good position")
                count += 1
                if count == 5:
                    pipeMainSend4.send('Done')  # pipe send data to main function to check the condition
                
            elif test < yVal-40:
                cond = 'up'
                moveLinear(cond)
                print("Table is moving up")
            elif test > yVal:
                cond = 'down'
                moveLinear(cond)
                print("Table is moving down")

    except KeyboardInterrupt:
        return 
            
            
            
def main(pipeDisRecv2,pipeCamSend,pipeMainRecv4,pipeEyeRecv3,pipeEyeSend5,p1,p2,p3):
    try:
        while True:
            Dis = pipeDisRecv2.recv()  # pipe receive the data from the distanceUs1 function which is Ultrasonic
#             if type(Dis) == int:
                
#             time.sleep(0.05)
            pipeCamSend.send(Dis)  # pipe send the distance value to both camera and condEye
            print(Dis)
            Eye = pipeEyeRecv3.recv()  # pipe receive the leftEye data to check condition and send back to condEye function
            pipeEyeSend5.send(Eye)  # pipe send leftEye value to condEye function to move the linear actuator

#                 check = pipeMainRecv4.recv()  # pipe receive the data from both camera and condEye function to check the condition
                
#                 if check == 'Done':
#                     p2.terminate()
#                     
#             
#                 elif check == 'kill':
#                     p1.terminate()
#                     p2.terminate()
#                     p3.terminate()
#                     return
#                 
#                 elif check == 'again':
#                     continue
                
                
#             elif Dis == "close":
#     #             if check == "done":
#                 print('close')
#                 
#             elif Dis == "Far":
#     #             if check == "done":
#                 print('far')
                
    except KeyboardInterrupt:
        p1.stop()
        p2.stop()
        p3.stop()
        return 
#         while type(Dis) == int:
#             
#             pipeCamSend.send(Dis)  # pipe send the distance value to both camera and condEye
#             pipeEyeSend5.send(Eye)
#             check = pipeMainRecv4.recv()  # pipe receive the data from both camera and condEye function to check the condition
#             Eye = pipeEyeRecv3.recv()  # pipe receive the leftEye data to check condition and send back to condEye function
#             
#             if check == 'Done' and type(Dis) == int:
#                 # send stop
#         
#             elif check == 'kill':
#                 p1.terminate()
#                 p2.terminate()
#                 p3.terminate()
#                 return 
#             elif check == 'again':
#                 pipeCamSend.send(Dis)
#                 pipeEyeSend5.send(Eye)
                
            
            
            
if __name__ == '__main__':
    #mainVoice('Distance detecting')
        
    
    
    pipeEyeSend , pipeEyeRecv= Pipe()
    pipeEyeSend2 , pipeEyeRecv2= Pipe()
    pipeEyeSend3 , pipeEyeRecv3= Pipe()
    pipeEyeSend4 , pipeEyeRecv4= Pipe()
    pipeEyeSend5 , pipeEyeRecv5= Pipe()
#     y = distanceUs1(pipeEyeSend2)

    p1 = Process(target=camera,args=(pipeEyeRecv,pipeEyeSend3,pipeEyeSend4,))
    p2 = Process(target=condEye,args=(pipeEyeRecv,pipeEyeRecv5,pipeEyeSend4))
    p3 = Process(target=distanceUs1,args=(pipeEyeSend2,))
    p4 = Process(target=main,args=(pipeEyeRecv2,pipeEyeSend,pipeEyeRecv4,pipeEyeRecv3,pipeEyeSend5,p1,p2,p3))
    
    
    p3.start()
    p4.start()
    p1.start()
    p2.start()
    p3.join()
    p4.join()
    p1.join()
    p2.join()
    
video_capture.release()
cv2.destroyAllWindows()
