import string
import wiringpi2
import math
import time
import Test_circuit as tc
import buttons
import keypad
import display

LEDS = [7, 8]

multiple_leds = tc.SetofLights(LEDS)

A_ENTRY, B_ENTRY, E_ENTRY = range(3)
OPERATIONS = ['+', '-', '/', '*', '^']
NUMBERS = {'pi':math.pi, 'e':math.e, 'tau':math.pi * 2}
TRIG = ['s', 'c', 't']
CLEAR = ['clear']

def round_digit(two_digits):
    if int(two_digits[1]) >= 5:
        end_digit = str(int(two_digits[0]) + 1)
        return end_digit
    else:
        return two_digits[0]

def round_number(string_number):
    len_string_number = len(string_number)
    upper_bound_length = 8
    if '.' in string_number:
        upper_bound_length += 1
    if upper_bound_length < len_string_number:
        if '.' in string_number:
            return string_number[:upper_bound_length - 1] + round_digit(string_number[upper_bound_length - 1 : upper_bound_length + 1])
        else:
            return ''
    else:
        return string_number


class Calculator:
    def __init__(self):
        self.a = 0
        self.b = 0
        self.decimal = 0
        self.o = None
        self.state = A_ENTRY
    def display(self):
        if self.state == A_ENTRY:
            if self.a % 1 == 0:
                return round_number(str(int(self.a)))
            else:
                return str(float(round_number(str(self.a))))
        elif self.state == B_ENTRY:
            return round_number(str(self.b))
        elif self.state == E_ENTRY:
            return 'error'
        else:
            assert(False)
    def apply_operation(self):
        if self.o:
            if len(self.o) == 2:
                if self.o[1] == '-':
                    self.b = -self.b
                elif self.o == 's':
                    self.b = math.sin(self.b)
                elif self.o == 'c':
                    self.b = math.cos(self.b)
                elif self.o == 't':
                    self.b = math.tan(self.b)
                self.o = self.o[0]
        if self.o == '+':
            self.a += self.b
        elif self.o == '-':
            self.a -= self.b
        elif self.o == '*':
            self.a *= self.b
        elif self.o == '/':
            self.a /= self.b
        elif self.o == '^':
            self.a = self.a ** self.b
        elif self.o == None:
            self.a = self.b
        else:
            assert(False)
        self.b = 0
    def clear_calc(self):
        self.a = 0
        self.b = 0
        self.decimal = 0
        self.o = None
        self.state = A_ENTRY
    def key(self, k):
        if k in CLEAR:
            self.clear_calc()
        elif self.state == A_ENTRY:
            if k == '=':
                self.o = None
            elif k in string.digits:
                self.b = int(k)
                self.state = B_ENTRY
            elif k == '.':
                self.b = 0
                self.decimal = 1
                self.state = B_ENTRY
            elif k in OPERATIONS:
                if k == '-' and self.o is not None:
                    self.o = self.o + k
                #elif k == '*' and self.o == '*':
                #    self.o = '^'
                else:
                    self.o = k
            elif k in NUMBERS.keys():
                self.b = NUMBERS[k]
                self.operation = None
        elif self.state == B_ENTRY:
            if k == '=':
                if self.o == '/' and self.b == 0:
                    self.state = E_ENTRY
                else:
                    self.apply_operation()
                    self.o = None
                    self.decimal = 0
                    self.state = A_ENTRY
            elif k in string.digits:
                if self.decimal == 0:
                    self.b = (self.b * 10) + int(k)
                    r_num = round_number(str(self.b))
                    if r_num == '':
                        self.state = E_ENTRY
                else:
                    self.b = self.b + (int(k) * 10**(-self.decimal))
                    self.decimal += 1
            elif k == '.':
                if self.decimal == 0:
                    self.decimal = 1
            elif k in OPERATIONS:
                self.apply_operation()
                self.o = k
                self.decimal = 0
                self.state = A_ENTRY
            elif k in NUMBERS.keys():
                self.a = NUMBERS[k]
                self.b = 0
                self.decimal = 0
                self.o = None
                self.state = A_ENTRY
        multiple_leds.rotate_one_on()



calc = Calculator()
list_of_relevent_characters = [n for n in string.digits] + list(NUMBERS.keys()) + OPERATIONS + CLEAR + ['='] + ['.'] + TRIG


def find_input():
    while True:
        button = buttons.scan()
        key = keypad.scan()
        if button:
            return button
        elif key:
            return key
        

def do_sums():
    while True:
        digit = find_input()
        if digit == 'kill':
            return ''
        elif digit not in list_of_relevent_characters:
            print('These are the usable characters')
            print(list_of_relevent_characters)
        else:
            calc.key(digit)
            display.write_new_values_to_display(calc.display())
        time.sleep(0.5)


if __name__ == '__main__':
    display.write_new_values_to_display('0')
    do_sums()
    display.clear_displays()
    multiple_leds.all_off()
