import sys
import configparser
import json
from time import sleep
import datetime
import pytz
from astral import LocationInfo
from astral.sun import sun
from astral.location import Location
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
region = config.get('location-config', 'region')
timezone = config.get('location-config', 'timezone')
latitude = config.get('location-config', 'latitude')
longitude = config.get('location-config', 'longitude')
nightLightDuration = config.get('raspberry-pi', 'nightLightDuration')
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

while True:
    if now > todayDusk: 
        print ("It's dark!!!")
        #turn the light on
        print ("Light on")
        senseHat.low_light = False
        senseHat.set_pixels(allOn)
    
        #leave the light on for 2 hours
        sleep(int(nightLightDuration))
        
        senseHat.low_light = True

        sleep(10)

        #turn the light off
        print ("Turn the light off")
        # stop signal to gate controller
        senseHat.clear()

        #break out of the loop and quit
        quit()