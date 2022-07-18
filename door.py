import time
from datetime import datetime

DOOR_RELAY = 4
REED_SWITCH = 14

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)  # the pin numbers refer to the board connector not the chip
GPIO.setwarnings(False)
GPIO.setup(REED_SWITCH, GPIO.IN, GPIO.PUD_UP) 
GPIO.setup(DOOR_RELAY, GPIO.OUT)
GPIO.output(DOOR_RELAY, GPIO.HIGH)


def Door():
                if GPIO.input(REED_SWITCH) == GPIO.LOW:
                      print ("Garage is Closed")
                else:
                      print ("Garage is Open")

if __name__ == '__main__':
	Door()
