import wiringpi2
import string

def setup_display():
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

def clear_displays():
    i.write(fst, 0x76)
    i.write(scd, 0x76)

