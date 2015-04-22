#!/usr/bin/env python
# Traffic Lights Demo Sequence
# Runs until Ctrl/C is pressed

# Must be run as root - sudo python TrafficLights.py 

import time, random, RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

BUTTON_PLUS = 14
BUTTON_MINUS = 15
BUTTON_MULTIPLY = 18
BUTTON_DIVIDE = 23
BUTTON_EQUALS = 24
BUTTON_KILL = 25


def setupgpio():
    GPIO.setup(BUTTON_PLUS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON_MINUS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON_MULTIPLY, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON_DIVIDE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON_EQUALS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON_KILL, GPIO.IN, pull_up_down=GPIO.PUD_UP)

BUTTON_LIST = [BUTTON_PLUS, BUTTON_MINUS, BUTTON_MULTIPLY, BUTTON_DIVIDE, BUTTON_EQUALS, BUTTON_KILL]

setupgpio()

def key():
    while True:
        for button_pin in BUTTON_LIST:
            if not GPIO.input(button_pin):
                if button_pin == BUTTON_PLUS:
                    return '+'
                elif button_pin == BUTTON_MINUS:
                    return '-'
                elif button_pin == BUTTON_MULTIPLY:
                    return '*'
                elif button_pin == BUTTON_DIVIDE:
                    return '/'
                elif button_pin == BUTTON_EQUALS:
                    return '='
                elif button_pin == BUTTON_KILL:
                    return 'kill'


