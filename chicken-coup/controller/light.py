"""
Module to use the Raspberry Pi to determine dusk and turn on light
"""

import sys
from time import sleep
import datetime
import pytz
from astral import LocationInfo
from astral.sun import sun
from astral.location import Location
from RPi import GPIO
import defs


#set localPath and accommodate invocation by systemd or by local
LOCAL_PATH=defs.setLocalPath

# read configuration file
config = defs.getConfig(LOCAL_PATH, 'controller.ini')


# read configuration parms
region = config.get('location-config', 'region')
timezone = config.get('location-config', 'timezone')
latitude = config.get('location-config', 'latitude')
longitude = config.get('location-config', 'longitude')
PIN = int(config.get('raspberry-pi', 'GPIOLightPin'))
nightLightDuration = config.get('raspberry-pi', 'nightLightDuration')
print ("latitude: ", latitude)
print ("longitude: ", longitude)
print ("Pin: " + str(PIN))

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

# setup the mode in which to refer to the pins
GPIO.setmode(GPIO.BCM)
# initialize the pin light
GPIO.setup(PIN, GPIO.OUT)

while True:
    if now > todayDusk:
        print ("It's dark!!!")
        #turn the light on
        print ("Light on")
        GPIO.output(PIN, True)

        #leave the light on for 2 hours
        sleep(int(nightLightDuration))

        #turn the light off
        print ("Turn the light off")
        # stop signal to gate controller
        GPIO.output(PIN, False)
        GPIO.cleanup()

        #break out of the loop and quit
        sys.exit()
