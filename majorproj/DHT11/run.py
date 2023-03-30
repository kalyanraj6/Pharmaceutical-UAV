import sys
import Adafruit_DHT
import time
import RPi.GPIO as GPIO
from flask import Flask, render_template
 
app = Flask(__name__)
 
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
@app.route("/")
def index():
    # Check the humidity and temperature 
    humidity, temperature = Adafruit_DHT.read_retry(11, 21)
     
 
    templateData = {
            'humidity': humidity
            'temperature' : temperature
        }
    return render_template('index.html', **templateData)
     
@app.route("/<deviceName>/<action>")
def action(deviceName, action):
    templateData = {
            'humidity': humidity
                'temperature'    : temperature
    }
    return render_template('index.html', **templateData)
 
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000, debug=True)