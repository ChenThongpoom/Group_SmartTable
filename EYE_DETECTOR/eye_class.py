from scipy.spatial import distance
from imutils import face_utils
import threading
from multiprocessing import Process , Pipe
import numpy as np
import time
import dlib
import cv2
from serialCommu import distanceUs1,moveLinear


print("Distance detecting...")
y = distanceUs1()

class opencv():
    def __init__(self, yVal):
        # threading.Thread.__init__(self)
        self.yVal = yVal
        #Load face detector and predictor, uses dlib shape predictor file
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

        #Extract indexes of facial landmarks for the left and right eye
        (self.lStart, self.lEnd) = face_utils.FACIAL_LANDMARKS_IDXS['left_eye']
        (self.rStart, self.rEnd) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']

        #Start webcam video capture
        self.video_capture = cv2.VideoCapture(0)
        self.leftEye = np.array([[0,0]])
        

    def run(self,pipeEye):
        while True:
            #Read each frame and flip it, and convert to grayscale
            self.ret, self.frame = self.video_capture.read()
            self.frame = cv2.flip(self.frame,1)
            self.frame = cv2.resize (self.frame,(300,240))
            self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            
            #Detect facial points through detector function
            self.faces = self.detector(self.gray, 0)

            #making reference lines
            self.frame = cv2.line(self.frame, (0,self.yVal-40),(1279,self.yVal-40),(0,0,255),2)
            self.frame = cv2.line(self.frame, (0,self.yVal),(1279,self.yVal),(0,0,255),2)

#             eye.eyeDetect()
            for face in self.faces:

                self.shape = self.predictor(self.gray, face)
                self.shape = face_utils.shape_to_np(self.shape)

                #Get array of coordinates of leftEye and rightEye
                self.leftEye = self.shape[self.lStart:self.lEnd]
                self.rightEye = self.shape[self.rStart:self.rEnd]

                #Use hull to remove convex contour discrepencies and draw eye shape around eyes
                leftEyeHull = cv2.convexHull(self.leftEye)
                rightEyeHull = cv2.convexHull(self.rightEye)
                cv2.drawContours(self.frame, [leftEyeHull], -1, (0, 255, 0), 1)
                cv2.drawContours(self.frame, [rightEyeHull], -1, (0, 255, 0), 1)
                
                print (self.leftEye[0][1])
                pipeEye.send(self.leftEye[0][1])
                
#             eye.sendToLinear()
            cv2.imshow('EYE_DETECTION',self.frame )

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

#     def eyeDetect(self,pipeEye):
#         for face in self.faces:
# 
#             self.shape = self.predictor(self.gray, face)
#             self.shape = face_utils.shape_to_np(self.shape)
# 
#             #Get array of coordinates of leftEye and rightEye
#             self.leftEye = self.shape[self.lStart:self.lEnd]
#             self.rightEye = self.shape[self.rStart:self.rEnd]
# 
#             #Use hull to remove convex contour discrepencies and draw eye shape around eyes
#             leftEyeHull = cv2.convexHull(self.leftEye)
#             rightEyeHull = cv2.convexHull(self.rightEye)
#             cv2.drawContours(self.frame, [leftEyeHull], -1, (0, 255, 0), 1)
#             cv2.drawContours(self.frame, [rightEyeHull], -1, (0, 255, 0), 1)
#             
#         print (self.leftEye[0][1])
#         pipeEye.send(self.leftEye[0][1])
#         pipeEye.close()
    
    def sendToLinear(self,pipeEye):
        while True:
            eye = (pipeEye.recv())
            if eye != 0:
                if (eye) >= (self.yVal-40) and (eye) <= (self.yVal):
                    con = 'stop'
                    print('Good position')
                    return moveLinear(con)
                elif (eye) < (self.yVal)-40:
                    con = 'up'
                    print('Table is moving up')
                    return moveLinear(con)
                elif (eye) > (self.yVal):
                    con = 'down'
                    print('Table is moving down')
                    return moveLinear(con)
#         if self.leftEye[0][1] != 0:
#             if (self.leftEye[0][1]) >= (self.yVal-40) and (self.leftEye[0][1]) <= (self.yVal):
#                 con = 'stop'
#                 print('Good position')
#                 return moveLinear(con)
#             elif (self.leftEye[0][1]) < (self.yVal)-40:
#                 con = 'up'
#                 print('Table is moving up')
#                 return moveLinear(con)
#             elif (self.leftEye[0][1]) > (self.yVal):
#                 con = 'down'
#                 print('Table is moving down')
#                 return moveLinear(con)



eye = opencv(y)

if __name__ == '__main__':
    pipeEyeSend , pipeEyeRecv= Pipe()
    p1 = Process(target=eye.run,args=(eye,pipeEyeSend))
    p2 = Process(target=eye.sendToLinear,args=(eye,pipeEyeRecv,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
      














