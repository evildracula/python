import Rpi.GPIO as GPIO
import sys


GPIO.setmode(GPIO.BOARD)
GPIO.setup(14, GPIO.OUT)
GPIO.output(14, True)
