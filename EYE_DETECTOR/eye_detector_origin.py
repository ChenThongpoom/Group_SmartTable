'Credit : Mohit Singh'
#Import necessary libraries
from scipy.spatial import distance
from imutils import face_utils
import threading
import numpy as np
import time
import dlib
import cv2
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
def camera():
    while True:
        #Read each frame and flip it, and convert to grayscale
        ret, frame = video_capture.read()
        frame = cv2.flip(frame,1)
        frame = cv2.resize(frame,(320,200))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #Detect facial points through detector function
        faces = detector(gray, 0)

        # #making reference lines
        frame = cv2.line(frame, (0,50),(1279,50),(0,0,255),2)
        frame = cv2.line(frame, (0,70),(1279,70),(0,0,255),2)
        

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

        
            print (leftEye[0][1]) #focus on y coordinate
        
            
            if leftEye[0][1] >= 50 and leftEye[0][1] <= 70:
                print ("good position")
            elif leftEye[0][1] < 50:
                print ("Moving up")
            elif leftEye[0][1] > 70:
                print ("Moving down")

        #show video feed
        cv2.imshow('EYE_DETECTION',frame )
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

a1 = threading.Thread(target=camera())
a1.start()




#Finally when video capture is over, release the video capture and destroyAllWindows
video_capture.release()
cv2.destroyAllWindows()


