import time
from datetime import datetime

DOOR_RELAY = 4
REED_SWITCH = 14

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)  
GPIO.setwarnings(False)
GPIO.setup(REED_SWITCH, GPIO.IN, GPIO.PUD_UP) 
GPIO.setup(DOOR_RELAY, GPIO.OUT)
GPIO.output(DOOR_RELAY, GPIO.HIGH)


def Garage():
                print ("Pressing button")
                GPIO.output(DOOR_RELAY, GPIO.LOW)
                time.sleep(1)
                GPIO.output(DOOR_RELAY, GPIO.HIGH)
                time.sleep(8)

                if GPIO.input(REED_SWITCH) == GPIO.LOW:
                      print ("Garage is Closed")
                else:
                      print ("Garage is Open")

if __name__ == '__main__':
	Garage()
