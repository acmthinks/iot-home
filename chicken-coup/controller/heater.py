"""
Module to use the Raspberry Pi Sense HAT to sense outside temperature and turn on coup heater
"""

from time import sleep
import datetime
from RPi import GPIO
import dht11
import defs

#set localPath and accommodate invocation by systemd or by local
LOCAL_PATH=defs.setLocalPath

# read configuration file
config = defs.getConfig(LOCAL_PATH, 'controller.ini')

# read configuration parms
PIN = int(config.get('raspberry-pi', 'GPIOTemperaturePin'))
TEMPERATURE_THRESHOLD = int(config.get('raspberry-pi', 'temperatureThreshold'))
TEMPERATURE_POLL_INTERVAL = int(config.get('raspberry-pi', 'temperaturePollInterval'))
print ("Temperature pin: ", PIN)

# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

# read data using pin 14
instance = dht11.DHT11(pin = PIN)

try:
    while True:
        result = instance.read()
        if result.is_valid():
            print("Last valid input: " + str(datetime.datetime.now()))
            tempF = ((result.temperature * 9/5) + 32)
            "Temperature: {} F ".format(tempF)
            "Humidity: {}%".format(result.humidity)
            if tempF < TEMPERATURE_THRESHOLD:
                #turn on heater
                print("Heat ON")
            else:
                print("Heat OFF")
        else:
            "Error: {}".format(result.error_code)

        sleep(TEMPERATURE_POLL_INTERVAL)
except KeyboardInterrupt:
    print("Cleanup")
    GPIO.cleanup()
        