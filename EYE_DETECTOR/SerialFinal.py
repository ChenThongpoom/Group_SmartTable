import serial
import time
import math
import sys
import threading
import queue
from num2words import num2words
import subprocess as sp


ser = serial.Serial(
                port='/dev/ttyACM0',
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)



def moveLinear(cond):
    
    if cond == 'up':
        ser.write(str.encode('u'))
        time.sleep(0.05)
        
        return
    elif cond == 'down':
        ser.write(str.encode('d'))
        time.sleep(0.05)
        
        return
    elif cond == 'stop':
        ser.write(str.encode('q'))
        time.sleep(0.05)
        
        return 
    return "done"



def distanceUs1():
    x = 0
    Sum = 0
    count = 1
    countDis = 1

    
    print('Distance detecting...')
    sp.Popen(["aplay /home/pi/Documents/Group4_SMART_TABLE/soundForSOT/Disdetect.wav 2>/dev/null"], shell=True)

    while count <= 1:
        ser.write(str.encode('a'))
        line = ser.readline()
        if line.decode() != '':
            if int(line.decode()) > 40 and int(line.decode()) < 70:
                Sum += (math.tan(20))* int(line.decode())
                count += 1
            elif int(line.decode()) < 40:
                countDis += 1
                if countDis % 5 == 0:
                    print("close")
                    sp.Popen(["aplay /home/pi/Documents/Group4_SMART_TABLE/soundForSOT/Close.wav 2>/dev/null"], shell=True)
                    

            elif int(line.decode()) > 70:
                countDis += 1
                if countDis % 5==0:
                    print("Far")
                    sp.Popen(["aplay /home/pi/Documents/Group4_SMART_TABLE/soundForSOT/Far.wav 2>/dev/null"], shell=True)
                    
                                      
    x = Sum // 1
    return(int(x))
    
 