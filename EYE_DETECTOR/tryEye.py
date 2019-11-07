'Credit : Mohit Singh'

#Import necessary libraries
from scipy.spatial import distance
from imutils import face_utils
import numpy as np
import time
import dlib
import cv2
import multiprocessing as Process, pipes

#Load face cascade which will be used to draw a rectangle around detected faces.
#face_cascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml")

#This function calculates and return eye aspect ratio



#Load face detector and predictor, uses dlib shape predictor file
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

#Extract indexes of facial landmarks for the left and right eye
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS['left_eye']
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']

#Start webcam video capture
video_capture = cv2.VideoCapture(0)

#Give some time for camera to initialize(not required)
time.sleep(2)
def camera(yVal):

    leftEyeSend, leftEyeRecv = pipes()

    p2 = Process(target= condEye, args=(130,leftEyeRecv))
    p2.start()

    while(True):
        #Read each frame and flip it, and convert to grayscale
        ret, frame = video_capture.read()
        frame = cv2.flip(frame,1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #Detect facial points through detector function
        faces = detector(gray, 0)

        #making reference lines
        frame = cv2.line(frame, (0,yVal-80),(1279,yVal-80),(0,0,255),2)
        frame = cv2.line(frame, (0,yVal),(1279,yVal),(0,0,255),2)

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

            
            print(leftEye[0][1]) #focus on y coordinate
            leftEyeSend.send(leftEye[0][1])

            
        #Show video feed
        cv2.imshow('EYE_DETECTION',frame )
        if(cv2.waitKey(1) & 0xFF == ord('q')):
            return
        if len(list(list(faces)))==0:
            leftEyeSend.close()
            p2.terminate



def condEye(yVal,pipeRecv):

    while True:
        leftEye = pipeRecv.recv()
        if (leftEye) >= Yval-80 and (leftEye) <= yVal:
            print("Good position")
        else:
            print("Your position is not appropiate")
            


if __name__=='__main__':

    camera(130)
#Finally when video capture is over, release the video capture and destroyAllWindows
video_capture.release()
cv2.destroyAllWindows()
