"""
Module to use the Raspberry Pi to turn on light
"""

import sys
from time import sleep
from sense_hat import SenseHat
from RPi import GPIO

sys.path.append('/home/pi/dev/iot-home/commons')

import defs

#set localPath and accommodate invocation by systemd or by local
LOCAL_PATH=defs.set_local_path(sys.argv[0])

# read configuration file
config = defs.get_config(LOCAL_PATH, 'controller.ini')

# read configuration parms
night_light_duration = config.get('raspberry-pi', 'night_light_duration')
sense_hat_led = config.get('raspberry-pi', 'sense_hat_led')
PIN = int(config.get('raspberry-pi', 'gpio_light_pin'))

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
else:
    print ("GPIO is the light source")
    # setup the mode in which to refer to the pins
    GPIO.setmode(GPIO.BCM)
    # initialize the pin light
    GPIO.setup(PIN, GPIO.OUT)
    GPIO.output(PIN, False)

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
