import time
import RPi.GPIO as GPIO

# GPIO_forward = 17
# GPIO_backward = 27
GPIO_forward2 = 23
GPIO_backward2 = 24
t = 3

while True:
#     inp = input()
    GPIO.setmode(GPIO.BCM)
#     GPIO.setup(GPIO_forward,GPIO.OUT)
#     GPIO.setup(GPIO_backward, GPIO.OUT)
    GPIO.setup(GPIO_forward2, GPIO.OUT)
    GPIO.setup(GPIO_backward2, GPIO.OUT)


#     if inp == 'u':
        
#         GPIO.output(GPIO_forward, GPIO.LOW)
#         GPIO.output(GPIO_backward, GPIO.HIGH)#Activate the relay one direction, to move the motor
    GPIO.output(GPIO_forward2, GPIO.LOW)
    GPIO.output(GPIO_backward2, GPIO.HIGH)
    time.sleep(t) #wait for t seconds
#     elif inp == 'q' :
#         GPIO.output(GPIO_forward,GPIO.HIGH)
#         GPIO.output(GPIO_backward,GPIO.HIGH) #Deactivate both relays to brake the motor
    GPIO.output(GPIO_forward2, GPIO.HIGH)
    GPIO.output(GPIO_backward2, GPIO.HIGH)
    time.sleep(t)
#         GPIO.cleanup()
#     elif inp == 'd':
#         GPIO.output(GPIO_forward,GPIO.HIGH) 
#         GPIO.output(GPIO_backward,GPIO.LOW) #activate the relay one direction to move the motor
    GPIO.output(GPIO_forward2, GPIO.HIGH)
    GPIO.output(GPIO_backward2, GPIO.LOW)
    time.sleep(t)

#     GPIO.output(GPIO_forward,GPIO.HIGH)
#     GPIO.output(GPIO_backward, GPIO.HIGH) #Deactivate the relay to brake the motor
#     GPIO.output(GPIO_forward2, GPIO.HIGH)
#     GPIO.output(GPIO_backward2, GPIO.HIGH)
#     time.sleep(t)
#     
    GPIO.cleanup()
