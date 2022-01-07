"""
Module to determine dusk for the current day, at the chicken coup
"""
# (crontab -u pi -l ; echo "0 7 * * * python3 ~/dev/iot-home/chicken-coup/controller/dusk.py") | crontab -u pi -

import sys
import subprocess
from time import sleep
import datetime
import pytz
from astral import LocationInfo
from astral.sun import sun
from astral.location import Location

sys.path.append('/home/pi/dev/iot-home/commons')

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
absolutePath = config.get('raspberry-pi', 'absolutePath')
lightScript = absolutePath + config.get('raspberry-pi', 'lightScript')
duskScript = absolutePath + config.get('raspberry-pi', 'duskScript')
cronScript = absolutePath + config.get('raspberry-pi', 'cronScript')
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

#let's turn the light on a lil' earlier than official dusk, about 30 minutes earlier
early = datetime.timedelta(minutes=30)
beforeDusk = todayDusk - early

print ("\n\nToday's Dusk: " + str(todayDusk))
#Today's Dusk: 2022-01-06 18:14:38.298481-05:00
min=str(todayDusk.minute)
hour=str(todayDusk.hour)
day_of_month="*"
month="*"
day_of_week="*"

light_sched = min + " " + hour + " * * * python3 " + lightScript
dusk_sched = "0 7 * * * python3 " + duskScript

cron = open(cronScript, "w")
cron.write(light_sched)
cron.write("\n")
cron.write(dusk_sched)
cron.write("\n")
cron.close()

# set crontab entry
cmd='crontab'

#remove all entries from the crontab for pi
subprocess.run([cmd,"-u", "pi", "-r"])

#set new crontab entries
subprocess.run([cmd, '-u', 'pi', cronScript])
