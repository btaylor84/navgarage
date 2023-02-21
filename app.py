# test framework to develop the web frontend
# useful for local tests with simulated door control



import time
import json

from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from webpush_handler import trigger_push_notifications_for_subscriptions
from flask_mqtt import Mqtt


DOOR_RELAY = 4
REED_SWITCH = 14

# import RPi.GPIO as GPIO
# GPIO.setmode(GPIO.BCM)  
# GPIO.setwarnings(False)
# GPIO.setup(REED_SWITCH, GPIO.IN, GPIO.PUD_UP) 
# GPIO.setup(DOOR_RELAY, GPIO.OUT)
# GPIO.output(DOOR_RELAY, GPIO.HIGH)

garageClosed = True     # true = closed

def Notify(state):

    # MQTT update
    mqtt.publish("nav/garage",state)

    # web push 
    subscriptions = PushSubscription.query.all()
    print(subscriptions)
    trigger_push_notifications_for_subscriptions(subscriptions,"Nav Garage",state)

def Garage():
    global garageClosed
    print ("Pressing button")
    # GPIO.output(DOOR_RELAY, GPIO.LOW)
    # time.sleep(1)
    # GPIO.output(DOOR_RELAY, GPIO.HIGH)
    # time.sleep(15)
    garageClosed = not garageClosed

    if garageClosed:
            print ("Garage is Closed")
            Notify("closed")
    else:
            print ("Garage is Open")
            Notify("opened")


def Door():
    if garageClosed:
#                    print ("Garage is Closed")
        return "closed"
    else:
#                    print ("Garage is Open")
        return "open"


app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('application.cfg.py')

mqtt = Mqtt(app)

# establish in-memory db of subscriptions for web-push
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"

db = SQLAlchemy(app)

class PushSubscription(db.Model):    
  id = db.Column(db.Integer, primary_key=True, unique=True)
  subscription_json = db.Column(db.Text, nullable=False)

db.create_all()

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

@app.route("/api/push-subscriptions", methods=["POST"])
def create_push_subscription():
    json_data = request.get_json()
    print(json.dumps( json_data)) #DEBUG
    subscription = PushSubscription.query.filter_by(
        subscription_json=json_data['subscription_json']
    ).first()
    if subscription is None:
        subscription = PushSubscription(
            subscription_json=json_data['subscription_json']
        )
        db.session.add(subscription)
        db.session.commit()
        print("sub added") #DEBUG
    return jsonify({
        "status": "success"
    })

if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=5000)
