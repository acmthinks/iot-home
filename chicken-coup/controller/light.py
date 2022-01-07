"""
DEPRECATED: Module to use the Raspberry Pi Sense HAT to determine dusk to turn on Sense HAT light
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


sys.path.append('/home/pi/dev/iot-home/')

import defs

#set localPath and accommodate invocation by systemd or by local
LOCAL_PATH=defs.set_local_path(sys.argv[0])

# read configuration file
config = defs.get_config(LOCAL_PATH, 'controller.ini')

# read configuration parms
region = config.get('location-config', 'region')
timezone = config.get('location-config', 'timezone')
latitude = config.get('location-config', 'latitude')
longitude = config.get('location-config', 'longitude')
night_light_duration = config.get('raspberry-pi', 'night_light_duration')
sense_hat_led = config.get('raspberry-pi', 'sense_hat_led')
PIN = int(config.get('raspberry-pi', 'gpio_light_pin'))

#get today's date
tz = pytz.timezone(timezone)
now = datetime.datetime.now(tz=tz)
d = now.day
m = now.month
y = now.year

print ("Today's Date: " + str(y) + "-" + str(m) + "-"+ str(d))

location_info = LocationInfo('Chicken Coup', region, timezone, float(latitude), float(longitude))
location = Location(location_info)
print (location_info)
print (location_info.observer)
s = sun(location_info.observer, date=datetime.date(y,m,d), tzinfo=location_info.timezone)
for key in ['dawn', 'dusk', 'noon', 'sunrise', 'sunset']:
    print (f'{key:10s}: ', s[key])

today_dusk = location.dusk(None, True, 0)

print ("Today's Dusk: " + str(today_dusk))

# initialize Sense Hat
if sense_hat_led is True:
    print ("Sense Hat is the light source")
    sense_hat = SenseHat()

    O = [255, 255, 255] # white, on
    X = [0, 0, 0] # off

    all_on = [
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    ]

    all_off = [
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    ]
    sense_hat.clear()
    sense_hat.low_light = False
    sense_hat.set_pixels(all_on)
    sleep(10)
    sense_hat.clear()
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
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN, GPIO.OUT)

while True:
    if now > today_dusk:
        print ("It's dark!!!")
        #turn the light on
        print ("Light on")
        if sense_hat_led is True:
            sense_hat.low_light = False
            sense_hat.set_pixels(all_on)
        else:
            GPIO.output(PIN, True)

        #leave the light on for 2 hours
        sleep(int(night_light_duration))

        #turn the light off
        print ("Turn the light off")
        # stop signal to light
        if sense_hat_led is True:
            sense_hat.low_light = True
            sleep(10)
            sense_hat.clear()
        else:
            GPIO.output(PIN, False)
            GPIO.cleanup()

        #break out of the loop and quit
        sys.exit()
