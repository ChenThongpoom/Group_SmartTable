import serial
import time
import math
# import pyttsx
import sys
from multiprocessing import Process , Pipe
# from voiceCommandStates import mainVoice

ser = serial.Serial(
                port='/dev/ttyACM0',
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)


# def distanceUs():
#     count = 1
#     avg = 0
#     while count <= 3:
#         ser.write(str.encode('a'))
#         #if ser.in_waiting > 0:
#         line = ser.readline()
#         #print("calculating...")
#         #print(line.decode())
#         if line.decode() != '':
#             avg += int(line.decode())
#             count += 1 pipeEye.send(self.leftEye[0][1])
#             print(avg)
#     avg = avg // 3
#     return int(avg)

def moveLinear(cond):
    if cond == 'up':
        ser.write(str.encode('u'))
        time.sleep(0.05)
#         con = ser.readline()
#         txt = 'The table is moving up'
#         mainVoice(txt)
        return
    elif cond == 'down':
        ser.write(str.encode('d'))
        time.sleep(0.05)
#         con = ser.readline()
#         txt = 'The table is moving down'
#         mainVoice(txt)
        return
    elif cond == 'stop':
        ser.write(str.encode('q'))
        time.sleep(0.05)
#         con = ser.readline()
#         txt = 'Table done moving'
#         mainVoice(txt)
    return "done"

# def linearDown(cond):
#     ser.write(str.encode('d'))
#     txt = ser.readline()
#     return txt.decode()
#     
# def linearStop():
#     ser.write(str.encode('q'))
#     txt = ser.readline()
#     return txt.decode()

def distanceUs1():

    x = 0
    Sum = 0
    count = 1
    countDis = 1
#     engine = pyttsx.init()
    print('Distance Detecting...')
    
    while count <= 3:
        ser.write(str.encode('a'))
        #if ser.in_waiting > 0:
        line = ser.readline()
#         print(line.decode())
        if line.decode() != '':
            if int(line.decode()) > 40 and int(line.decode()) < 70:
                Sum += (math.tan(20))* int(line.decode())
                count += 1
            elif int(line.decode()) < 40:
                countDis += 1
                if countDis % 5 == 0:
                    print("close")
#                     mainVoice('Too close')
#                     engine.say("You are sitting too close to the camera") #tooClose
#                     engine.runAndWait()
            elif int(line.decode()) > 70:
                countDis += 1
                if countDis % 5==0:
                    print("Far")
                    
#                     mainVoice('Too far')
#                     engine.say("You are sitting too far to the camera")  #tooFar
#                     engine.runAndWait()
    x = Sum // 3
    return(int(x))
        
        

