'''
simple test to light up LEDs
'''

from time import sleep
from RPi import GPIO

PIN1=17

#setup the mode in which to refer to the pins
GPIO.setmode(GPIO.BOARD)

#initialize the pins
GPIO.setup(PIN1, GPIO.OUT)

GPIO.output(PIN1, True)

sleep(1)

GPIO.output(PIN1, False)
GPIO.cleanup()
