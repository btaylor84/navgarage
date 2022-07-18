import time
from datetime import datetime
from flask import Flask, render_template, request

DOOR_RELAY = 8
REED_SWITCH = 7



import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)  # the pin numbers refer to the board connector not the chip
GPIO.setwarnings(False)
GPIO.setup(REED_SWITCH, GPIO.IN, GPIO.PUD_UP) # set up pin ?? (one of the above listed pins) as an input with a pull-up resistor
GPIO.setup(DOOR_RELAY, GPIO.OUT)
GPIO.output(DOOR_RELAY, GPIO.HIGH)



app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
             if GPIO.input(DOOR_RELAY) == GPIO.LOW:
                   print ("Garage is Closed")
                   return app.send_static_file('Closed.html')
             else:
                    print ("Garage is Open")
                    return app.send_static_file('Open.html')


@app.route('/Garage', methods=['GET', 'POST'])
def Garage():
        name = request.form['garagecode']
        if name == '12345678':  # 12345678 is the Password that Opens Garage Door (Code if Password is Correct)
                GPIO.output(DOOR_RELAY, GPIO.LOW)
                time.sleep(1)
                GPIO.output(DOOR_RELAY, GPIO.HIGH)
                time.sleep(2)

                if GPIO.input(REED_SWITCH) == GPIO.LOW:
                      print ("Garage is Closed")
                      return app.send_static_file('Closed.html')
                else:
                      print ("Garage is Open")
                      return app.send_static_file('Open.html')

        if name != '12345678':  # 12345678 is the Password that Opens Garage Door (Code if Password is Incorrect)
                if name == "":
                        name = "NULL"
                print("Garage Code Entered: " + name)

                if GPIO.input(REED_SWITCH) == GPIO.LOW:
                        print ("Garage is Closed")
                        return app.send_static_file('Closed.html')
                else:
                        print ("Garage is Open")
                        return app.send_static_file('Open.html')

@app.route('/stylesheet.css')
def stylesheet():
        return app.send_static_file('stylesheet.css')

@app.route('/Log')
def logfile():
        return app.send_static_file('log.txt')

@app.route('/images/<picture>')
def images(picture):
        return app.send_static_file('images/' + picture)

if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=5000)

