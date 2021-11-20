import sys
import configparser
import json
from time import sleep
import datetime
from sense_hat import SenseHat


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
temperatureThreshold = int(config.get('raspberry-pi', 'temperatureThreshold'))
temperaturePollInterval = int(config.get('raspberry-pi', 'temperaturePollInterval'))
print ("Temperature pin: ", pin)

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
    if tempF < 50:
        #turn on heater
        print("Heat ON")
    else:
        print ("Heat OFF")
        
    sleep(temperaturePollInterval)

        