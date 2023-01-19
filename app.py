from flask import Flask, render_template
import time
import Adafruit_DHT
import RPi.GPIO as GPIO
import csv

app = Flask(__name__)

# Set the sensor type (DHT22) and the GPIO pin number
sensor = Adafruit_DHT.DHT22
pin = 4

# Set the relay pin number
relay = 17

# Set the interval for logging data and turning on the relay (in seconds)
log_interval = 300 # 5 minutes
relay_interval = 14400 # 4 hours

# Initialize the GPIO pin for the relay
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay, GPIO.OUT)

# Open the CSV files for writing
temp_humidity_file = open('temp_humidity_data.csv', 'w', newline='')
temp_humidity_writer = csv.writer(temp_humidity_file)
temp_humidity_writer.writerow(['Time', 'Temperature(F)', 'Humidity(%)'])

relay_file = open('relay_data.csv', 'w', newline='')
relay_writer = csv.writer(relay_file)
relay_writer.writerow(['Time', 'Relay Status'])
# Store the time when the relay was last turned on
last_relay_on = time.time()

# Global variables to store the temperature and humidity values
global temperature
global humidity

def read_and_log_data():
    try:
        while True:
            temperature, humidity = read_sensor_data()
            log_data(temperature, humidity)
            check_relay()
            time.sleep(log_interval)
    except KeyboardInterrupt:
        pass
    finally:
        # Close the CSV files
        temp_humidity_file.close()
        relay_file.close()
        # Clean up the GPIO pins
        GPIO.cleanup()

@app.route("/")
def index():
    read_and_log_data()
    return render_template("index.html", temperature=temperature, humidity=humidity)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)