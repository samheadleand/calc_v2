import string
import math
import wiringpi2
import time
import Test_circuit as tc
import buttons

LEDS = [7, 8]

multiple_leds = tc.SetofLights(LEDS)

A_ENTRY, B_ENTRY, E_ENTRY = range(3)
OPERATIONS = ['+', '-', '/', '*', '^']
NUMBERS = {'pi':math.pi, 'e':math.e, 'tau':math.pi * 2}
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
        elif self.o == '+-':
            self.a -= self.b
        elif self.o == '--':
            self.a += self.b
        elif self.o == '*-':
            self.b = -self.b
            self.a *= self.b
        elif self.o == '/-':
            self.b = -self.b
            self.a /= (-self.b)
        elif self.o == '^-':
            self.a = self.a ** -self.b
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
                if k == '-' and self.o != None:
                    self.o = self.o + k
                else:
                    self.o = k
            elif k in NUMBERS.keys():
                self.b = NUMBERS[k]
                self.apply_operation()
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


i = wiringpi2.I2C()
fst = i.setupInterface("/dev/i2c-1", 0x72)
scd = i.setupInterface("/dev/i2c-1", 0x71)
i.write(fst, 0x7A)
i.write(fst, 0xFF)
i.write(scd, 0x7A)
i.write(scd, 0xFF)

def get_range(display):
    if display == fst:
        return range(0, 4)
    elif display == scd:
        return range(4, 8)

def which_display_to_talk_to(number):
    if number in get_range(fst):
        return fst
    elif number in get_range(scd):
        return scd

def move_decimal_in_serial(move):
    display = which_display_to_talk_to(move)
    number = move % 4
    number = 2 ** number
    i.write(fst, 0x77)
    i.write(fst, 0)
    i.write(scd, 0x77)
    i.write(scd, 0)
    i.write(display, 0x77)
    i.write(display, number)


def count_digits_without_decimals(string_number):
    idx = 0
    for num in string_number:
        if num in string.digits:
            idx += 1
    return idx

def move_cursor_in_serial(move):
    display = which_display_to_talk_to(move)
    number = move % 4
    i.write(display, 0x79)
    i.write(display, number)

def display_error():
    i.write(scd, 0x7E)
    i.write(scd, 0b1111001)

def display_negative(position):
    display = which_display_to_talk_to(position)
    number = position % 4
    if number == 0:
        i.write(display, 0x7B)
    elif number == 1:
        i.write(display, 0x7C)
    elif number == 2:
        i.write(display, 0x7D)
    elif number == 3:
        i.write(display, 0x7E)
    i.write(display, 0b1000000)

def write_new_values_to_display(string_number):
    i.write(fst, 0x76)
    i.write(scd, 0x76)
    if string_number == 'error':
        display_error()
    else:
        idx = 8 - count_digits_without_decimals(string_number)
        if idx < 0:
            pass
        else:
            move_cursor_in_serial(idx)
            for num in str(string_number):
                if num == '.':
                    move_decimal_in_serial(idx - 1)
                elif num == '-':
                    display_negative(idx - 1)
                elif idx in range(0, 4):
                    i.write(fst, int(num))
                    idx += 1
                elif idx in range(4, 8):
                    i.write(scd, int(num))
                    idx += 1
            

calc = Calculator()
list_of_relevent_characters = [n for n in string.digits] + list(NUMBERS.keys()) + OPERATIONS + CLEAR + ['='] + ['.']


def do_sums():
    while True:
        digit = buttons.key()
        if digit == 'kill':
            return ''
        elif digit not in list_of_relevent_characters:
            print('These are the usable characters')
            print(list_of_relevent_characters)
        else:
            calc.key(digit)
            write_new_values_to_display(calc.display())
        time.sleep(0.5)


do_sums()
i.write(fst, 0x76)
i.write(scd, 0x76)
multiple_leds.all_off()



#if __name__ == '__main__':
#    c = Calculator()
#    while True:
#        print (c.display())
#        k = input()
#    c.key(k)
