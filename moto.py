import RPi.GPIO as GPIO
import time
import sys
from array import *

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

steps = int(sys.argv[1]);
clockwise = int(sys.argv[2]);

arr = [0, 1, 2, 3];
if clockwise != 1:
    arr = [3, 2, 1, 0];

ports = [24, 25, 8, 7]

for p in ports:
    GPIO.setup(p, GPIO.OUT)

for x in range(0, steps):
    for j in arr:
        time.sleep(0.01)
        for i in range(0, 4):
            if i == j:
                GPIO.output(ports[i], True)
            else:
                GPIO.output(ports[i], False)
