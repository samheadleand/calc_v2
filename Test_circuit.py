import time, random, itertools, RPi.GPIO as GPIO

# Comment Added

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


LEDOFF = 0
LEDON = 1


class Light:
    def __init__(self, led):
        self.led = led
        GPIO.setup(led, GPIO.OUT)
        GPIO.output(led, LEDOFF)
        self.state = LEDOFF
    def led_on(self):
        GPIO.output(self.led, LEDON)
        self.state = LEDON
    def led_off(self):
        GPIO.output(self.led, LEDOFF)
        self.state = LEDOFF
    def led_switch(self):
        if self.state == LEDON:
            GPIO.output(self.led, LEDOFF)
            self.state = LEDOFF
        else:
            GPIO.output(self.led, LEDON)
            self.state = LEDON

class SetofLights:
    def __init__(self, list_of_led_places):
        self.leds = [Light(led) for led in list_of_led_places]
        self.rotation = itertools.cycle(range(len(self.leds)))
    def all_off(self):
        for led in self.leds:
            led.led_off()
    def all_on(self):
        for led in self.leds:
            led.led_on()
    def all_switch(self):
        for led in self.leds:
            led.led_switch()
    def how_many_are_on(self):
        count = 0
        for led in self.leds:
            if led.state == LEDON:
                count += 1
        return count
    def rotate_one_on(self):
        self.all_off()
        self.leds[next(self.rotation)].led_on()
        
        
         
#LEDS = [7, 8]


