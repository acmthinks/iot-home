import sys
import configparser
import json
#import RPi.GPIO as GPIO
from time import sleep
import datetime
import pytz
from astral import LocationInfo
from astral.sun import sun
from astral.location import Location


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
region = config.get('location-config', 'region')
timezone = config.get('location-config', 'timezone')
latitude = config.get('location-config', 'latitude')
longitude = config.get('location-config', 'longitude')
pin = config.get('raspberry-pi', 'GPIOLightPin')
nightLightDuration = config.get('raspberry-pi', 'nightLightDuration')
print ("latitude: ", latitude)
print ("longitude: ", longitude)
print ("Pin: " + pin)

#get today's date
tz = pytz.timezone(timezone)
now = datetime.datetime.now(tz=tz)
d = now.day
m = now.month
y = now.year

print ("Today's Date: " + str(y) + "-" + str(m) + "-"+ str(d))

locationInfo = LocationInfo('Chicken Coup', region, timezone, float(latitude), float(longitude))
location = Location(locationInfo)
print (locationInfo)
print (locationInfo.observer)
s = sun(locationInfo.observer, date=datetime.date(y,m,d), tzinfo=locationInfo.timezone)
for key in ['dawn', 'dusk', 'noon', 'sunrise', 'sunset']:
    print (f'{key:10s}: ', s[key])

todayDusk = location.dusk(None, True, 0)

print ("Today's Dusk: " + str(todayDusk))


while True:
    if now > todayDusk: 
        print ("It's dark!!!")
        #turn the light on
        print ("Light on")
        #leave the light on for 2 hours
        sleep(int(nightLightDuration))
        
        #turn the light off
        print ("Turn the light off")

        #break out of the loop and quit
        quit()

  #get today's scheduled Dusk time HH:MM
  #get the time right now
  #sleep(1)
  #if now is after Dusk, turn on the light