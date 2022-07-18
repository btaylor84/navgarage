import time
from datetime import datetime
from flask import Flask, render_template

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
                time.sleep(15)

                if GPIO.input(REED_SWITCH) == GPIO.LOW:
                      print ("Garage is Closed")
                else:
                      print ("Garage is Open")


def Door():
                if GPIO.input(REED_SWITCH) == GPIO.LOW:
                    print ("Garage is Closed")
                    return "open"
                else:
                    print ("Garage is Open")
                    return "closed"

app = Flask(__name__)
door_status = Door() 

@app.route("/")
def index():
    return render_template("index.html", door_status=door_status)

@app.route("/open", methods=["POST"])
def opendoor():
    global door_status
    if door_status == "closed"
        Garage()
        door_status = "open"

@app.route("/close", methods=["POST"])
def closedoor():
    global door_status
    if door_status == "open"
        Garage()
        door_status = "closed"

