#!/usr/bin/env python
# Traffic Lights Demo Sequence
# Runs until Ctrl/C is pressed

# Must be run as root - sudo python TrafficLights.py 

import time, random, RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

COLUMN = [23, 24, 25] # Inputs as below

ROW = [14, 15, 18] # Outputs - set to zero

MAPPING = {(0, 0): 'kill', (0, 1): '^', (0, 2): 'tau',
           (1, 0): 'e', (1, 1): '+', (1, 2): '-',
           (2, 0): '*', (2, 1): '/', (2, 2): '='
           }


def setupgpio():
    for c in COLUMN:
        GPIO.setup(c, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    for r in ROW:
        GPIO.setup(r, GPIO.OUT)
        GPIO.output(r, 1)


setupgpio()

def all_rows_on():
    for r in ROW:
        GPIO.output(r, 1)


def scan():
    #which key has been pressed
    #run loop over each column, set the one I'm on to zero and the other two to 1
    #check to see if row input is zero or one
    for r in ROW:
        all_rows_on()
        GPIO.output(r, 0)
        time.sleep(0.01)
        for c in COLUMN:
            if not GPIO.input(c):   
                return MAPPING[(ROW.index(r), COLUMN.index(c))]
    return False

time.sleep(1)
print(scan())
