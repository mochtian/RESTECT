import RPi.GPIO as GPIO  
import time
from time import sleep

GPIO.setmode(GPIO.BCM)  
GPIO.setwarnings(False)  

GPIO.setup(26, GPIO.IN)  
GPIO.setup(23, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)

pwm=GPIO.PWM(3, 50)
pwm.start(0)

def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(3, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(3,False)
    pwm.ChangeDutyCycle(0)

while True:  
            i=GPIO.input(26)  
            if i==0:                 #When output from LPG sensor is LOW  
                print("No Gas Leakage Detected",i)
                time.sleep(0.5)
            elif i==1:               #When output from LPG sensor is HIGH  
                #print("Intruder detected",i)
                SetAngle(90)
                time.sleep(0.5)
                print("LPG Detect",i)
                time.sleep(0.5)
                GPIO.output(23, GPIO.HIGH)
                time.sleep(0.3)
                GPIO.output(23, GPIO.LOW)
                time.sleep(0.1)
