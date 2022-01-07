"""
Module to determine dusk for the current day, at the chicken coup
"""

import sys
import subprocess
import datetime
import pytz
from astral import LocationInfo
from astral.sun import sun
from astral.location import Location

sys.path.append('/home/pi/dev/iot-home/commons')

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
absolute_path = config.get('raspberry-pi', 'absolute_path')
light_script = absolute_path + config.get('raspberry-pi', 'light_script')
dusk_script = absolute_path + config.get('raspberry-pi', 'dusk_script')
cron_script = absolute_path + config.get('raspberry-pi', 'cron_script')

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

today_dusk = location.dusk(None, True, 0)

#let's turn the light on a lil' earlier than official dusk, about 30 minutes earlier
early = datetime.timedelta(minutes=30)
beforeDusk = today_dusk - early

print ("\n\nToday's Dusk: " + str(today_dusk))
#Today's Dusk: 2022-01-06 18:14:38.298481-05:00
DUSK_MINUTE=str(today_dusk.minute)
DUSK_HOUR=str(today_dusk.hour)

light_sched = DUSK_MINUTE + " " + DUSK_HOUR + " * * * python3 " + light_script
dusk_sched = "0 7 * * * python3 " + dusk_script

with open(cron_script, "w", encoding="utf8") as cron:
    cron.write(light_sched)
    cron.write("\n")
    cron.write(dusk_sched)
    cron.write("\n")

# set crontab entry
CMD='crontab'

#remove all entries from the crontab for pi
subprocess.run([CMD,"-u", "pi", "-r"], check=True)

#set new crontab entries
subprocess.run([CMD, '-u', 'pi', cron_script], check=True)
