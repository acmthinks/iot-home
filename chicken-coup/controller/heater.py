import sys
import configparser
import json
import RPi.GPIO as GPIO
import dht11
from time import sleep
import datetime

#set localPath and accommodate invocation by systemd or by local
scriptName = sys.argv[0]
print ("Running: " + scriptName)
localPath = scriptName.rsplit('/', 1)[0]
if scriptName == localPath: 
    localPath = ""
else:
    localPath = localPath + "/"
print ("localPath: " + localPath)


# read configuration file
config = configparser.ConfigParser()
configFilePath = localPath + 'controller.ini'
config.read(configFilePath)

# read configuration parms
pin = int(config.get('raspberry-pi', 'GPIOTemperaturePin'))
temperatureThreshold = int(config.get('raspberry-pi', 'temperatureThreshold'))
print ("Temperature pin: ", pin)

# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

# read data using pin 14
instance = dht11.DHT11(pin = pin)

try:
    while True:
        result = instance.read()
        if result.is_valid():
            print("Last valid input: " + str(datetime.datetime.now()))
            print("Temperature: %-3.1f C" % result.temperature)
            print("Humidity: %-3.1f %%" % result.humidity)
            if result.temperature < 50:
                #turn on heater
                print("Heat ON")
            else:
                print ("Heat OFF")
        else:
            print("Error: %d" % result.error_code)

        sleep(10)
except KeyboardInterrupt:
    print("Cleanup")
    GPIO.cleanup()
        