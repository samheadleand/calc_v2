import time, random, itertools, RPi.GPIO as GPIO

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

#multiple_leds = SetofLights(LEDS)
#multiple_leds.all_off()
#multiple_leds.all_on()
#time.sleep(1)
#multiple_leds.all_off()
#multiple_leds.rotate_one_on()
#time.sleep(1)
#multiple_leds.rotate_one_on()
#time.sleep(1)
#multiple_leds.rotate_one_on()
#time.sleep(1)
#multiple_leds.rotate_one_on()
#time.sleep(1)
#multiple_leds.all_off()


'''


LEDS = [7, 8]


def setupgpio():
    for led in LEDS:
        GPIO.setup(led, GPIO.OUT)


def alloff():
    for led in LEDS:
        GPIO.output(led, LEDOFF)


def led_change(led, on_or_off):
    #on = True
    if on_or_off:
        GPIO.output(LEDS[led], LEDON)
    else:
        GPIO.output(LEDS[led], LEDOFF)



setupgpio()
alloff()
#led_change(0, True)
#led_change(1, True)


button_toggled = [False] #[red, green, yellow, blue]
#BUTTON_LIST = [BUTTON_RED]
led_list = [False, False]


def change_lights(list_of_leds_to_change):
    for idx, instruction in enumerate(list_of_leds_to_change):
        if instruction == 1:
            led_list[idx] = not led_list[idx]
            led_change(idx, led_list[idx])


def flash(val):
    alloff()
    idx = 0
    if val % 2 == 0:
        idx += 1
    change_lights([1, 0])
    time.sleep(0.2)
    while idx < val * 2:
        change_lights([1, 1])
        time.sleep(0.2)
        idx +=1
    

itertools.repeat/cycle
flash(10)
alloff()



'''
