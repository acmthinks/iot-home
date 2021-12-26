"""
Module to use the Raspberry Pi Sense HAT to sense outside temperature and turn on coup heater
"""

from time import sleep
import datetime
from sense_hat import SenseHat
import defs

#set localPath and accommodate invocation by systemd or by local
LOCAL_PATH=defs.setLocalPath

# read configuration file
config = defs.getConfig(LOCAL_PATH, 'controller.ini')

# read configuration parms
TEMPERATURE_THRESHOLD = int(config.get('raspberry-pi', 'temperatureThreshold'))
TEMPERATURE_POLL_INTERVAL = int(config.get('raspberry-pi', 'temperaturePollInterval'))

# initialize Sense Hat
senseHat = SenseHat()

while True:
    # read temp
    temp = senseHat.get_temperature()
    humidity = senseHat.get_humidity()
    print("Last valid input: " + str(datetime.datetime.now()))
    tempF = ((temp * 9/5) + 32)
    print("Temperature: %-3.1f F" % tempF)
    print("Humidity: %-3.1f %%" % humidity)
    if tempF < TEMPERATURE_THRESHOLD:
        #turn on heater
        print("Heat ON")
    else:
        print ("Heat OFF")
    sleep(TEMPERATURE_POLL_INTERVAL)
        