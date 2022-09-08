import RPi.GPIO as GPIO  
import time
import requests
from time import sleep
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
from datetime import datetime

TOKEN = "BBFF-GVmjrx5Im4qO2gtC2WUQ9fQRR0ckbE"
DEVICE_LABEL = "RESTECT" 
VARIABLE_LABEL_1 = "gas"
VARIABLE_LABEL_2 = "flame"
VARIABLE_LABEL_3 = "buzzer"

GPIO.setmode(GPIO.BCM)  
GPIO.setwarnings(False)
 
#set GPIO direction (IN / OUT)
GPIO.setup(25, GPIO.IN)  #gas
GPIO.setup(21, GPIO.IN)  #flame
GPIO.setup(16,GPIO.IN,pull_up_down=GPIO.PUD_UP) #button
GPIO.setup(23, GPIO.OUT) #buzzer
GPIO.setup(17, GPIO.OUT) #servo

pwm=GPIO.PWM(17, 50)
pwm.start(0)
lcd = LCD()

def build_payload(variable_1, variable_2, variable_3):

    def SetAngle(angle):
        duty = angle / 18 + 2
        GPIO.output(17, True)
        pwm.ChangeDutyCycle(duty)
        sleep(1)
        GPIO.output(17, False)
        pwm.ChangeDutyCycle(0)
        
    def safe_exit(signum, frame):
        exit(1)

    gas = GPIO.input(25)
    button = GPIO.input(16)
    flame = GPIO.input(21)
    
    buzzer = 0
    #print(button)
    if gas == 0:                 #When output from LPG sensor is LOW  
        print("Gas Aman",gas)
        time.sleep(0.5)
        try:
            lcd.text("    Gas Aman", 1)
            #lcd.text(time.strftime('  %I:%M:%S %p'), 2)
        except KeyboardInterrupt:
            pass
        if button == 0:
            buzzer = 0
            GPIO.output(23, GPIO.LOW)
    elif gas == 1:               #When output from LPG sensor is HIGH  
    #print("Intruder detected",i)
        SetAngle(90)
        time.sleep(0.3)
        print("Gas Bocor",gas)
        buzzer = 1
        try:
            lcd.text("    Gas Bocor", 1)
            #lcd.text(time.strftime('  %I:%M:%S %p'), 2)
        except KeyboardInterrupt:
            pass
        if button == 1 :
            GPIO.output(23, GPIO.HIGH)
        else :
            buzzer = 0
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
            lcd.text(time.strftime('  %I:%M:%S %p'), 2)
            time.sleep(3)
            lcd.text("    Api Padam", 2)
            time.sleep(0.5)
        except KeyboardInterrupt:
            pass
        print("Api Padam")
    sleep(1)
     
    payload = {variable_1:gas, variable_2:flame, variable_3:buzzer}
    return payload

def post_request(payload):
   # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True

def main():
    payload = build_payload(VARIABLE_LABEL_1, VARIABLE_LABEL_2, VARIABLE_LABEL_3)

    print("[INFO] Attemping to send data")
    post_request(payload)
    print("[INFO] finished")


if __name__ == '__main__':
    while (True):
        main()
        time.sleep(1)
