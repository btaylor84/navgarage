import time
import json

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
#                    print ("Garage is Closed")
                    return "closed"
                else:
#                    print ("Garage is Open")
                    return "open"

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", door_status=Door())

@app.route("/open", methods=["POST"])
def opendoor():
    if Door() == "closed":
        Garage()
    return Door()

@app.route("/close", methods=["POST"])
def closedoor():
    if Door() == "open":
        Garage()
    return Door()

@app.route("/status", methods=["GET"])
def doorstatus():
    status = Door()
    last_time = '00:00:00 on yy-mm-dd'
    return { "door":Door(), "changed":last_time}

if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=5000)
