import RPi.GPIO as GPIO  
import time
from time import sleep
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
from datetime import datetime

GPIO.setmode(GPIO.BCM)  
GPIO.setwarnings(False)  

GPIO.setup(25, GPIO.IN)  #gas
GPIO.setup(21, GPIO.IN)  #flame
GPIO.setup(16,GPIO.IN,pull_up_down=GPIO.PUD_UP) #button
GPIO.setup(23, GPIO.OUT) #buzzer
GPIO.setup(17, GPIO.OUT) #servo
 
pwm=GPIO.PWM(17, 50)
pwm.start(0)
lcd = LCD()

def SetAngle(angle):
        duty = angle / 18 + 2
        GPIO.output(17, True)
        pwm.ChangeDutyCycle(duty)
        sleep(1)
        GPIO.output(17, False)
        pwm.ChangeDutyCycle(0)
        
def safe_exit(signum, frame):
    exit(1)

while True:
    gas = GPIO.input(25)
    button = GPIO.input(16)
    flame = GPIO.input(21)
    #print(button)
    if gas == 0:                 #When output from LPG sensor is LOW  
        print("Gas Aman",gas)
        time.sleep(0.5)
        try:
            lcd.text("    Gas Aman", 1)
        except KeyboardInterrupt:
            pass
        if button == 0:
            GPIO.output(23, GPIO.LOW)
    elif gas == 1:               #When output from LPG sensor is HIGH  
    #print("Intruder detected",i)
        SetAngle(90)
        time.sleep(0.3)
        print("Gas Bocor",gas)
        try:
            lcd.text(time.strftime('  %I:%M:%S %p'), 2)
            time.sleep(3)
            lcd.text("    Gas Bocor", 1)
            time.sleep(0.5)
        except KeyboardInterrupt:
            pass
        if button == 1 :
            GPIO.output(23, GPIO.HIGH)
        else :
            GPIO.output(23, GPIO.LOW)
    if flame == 0:
        try:
            lcd.text(time.strftime('  %I:%M:%S %p'), 2)
            time.sleep(3)
            lcd.text("   Api Menyala", 2)
            time.sleep(0.5)
        except KeyboardInterrupt:
            pass
        print("Api Menyala")
    elif flame == 1:
        try:
            lcd.text("    Api Mati", 2)
        except KeyboardInterrupt:
            pass
        print("Api Mati")
    sleep(1)

