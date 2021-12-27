"""
Module to use the Raspberry Pi Sense HAT to determine dusk to turn on Sense HAT light
"""

import sys
from time import sleep
import datetime
import pytz
from astral import LocationInfo
from astral.sun import sun
from astral.location import Location
from sense_hat import SenseHat
from RPi import GPIO


sys.path.append('../../commons')

import defs

#set localPath and accommodate invocation by systemd or by local
LOCAL_PATH=defs.setLocalPath(sys.argv[0])

# read configuration file
config = defs.getConfig(LOCAL_PATH, 'controller.ini')

# read configuration parms
region = config.get('location-config', 'region')
timezone = config.get('location-config', 'timezone')
latitude = config.get('location-config', 'latitude')
longitude = config.get('location-config', 'longitude')
nightLightDuration = config.get('raspberry-pi', 'nightLightDuration')
senseHatLED = bool(config.get('raspberry-pi', 'senseHatLED'))
PIN = int(config.get('raspberry-pi', 'GPIOLightPin'))
print ("latitude: ", latitude)
print ("longitude: ", longitude)

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

# initialize Sense Hat
if (senseHatLED):
    print ("Sense Hat is the light source")
    senseHat = SenseHat()

    O = [255, 255, 255] # white, on
    X = [0, 0, 0] # off
    
    allOn = [
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    ]

    allOff = [
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    ]
    senseHat.clear()
    senseHat.low_light = False
    senseHat.set_pixels(allOn)
    sleep(10)
    senseHat.clear()
else:
    print ("GPIO is the light source")
    # setup the mode in which to refer to the pins
    GPIO.setmode(GPIO.BCM)
    # initialize the pin light
    GPIO.setup(PIN, GPIO.OUT)
    GPIO.output(PIN, False)
    GPIO.output(PIN, True)
    sleep(10)
    GPIO.output(PIN, False)

while True:
    if now > todayDusk:
        print ("It's dark!!!")
        #turn the light on
        print ("Light on")
        if (senseHatLED): 
            senseHat.low_light = False
            senseHat.set_pixels(allOn)
        else:
            GPIO.output(PIN, True)

        #leave the light on for 2 hours
        sleep(int(nightLightDuration))

        senseHat.low_light = True

        sleep(10)

        #turn the light off
        print ("Turn the light off")
        # stop signal to light
        if (senseHatLED):
            senseHat.clear()
        else: 
            GPIO.output(PIN, False)
            GPIO.cleanup()

        #break out of the loop and quit
        sys.exit()
