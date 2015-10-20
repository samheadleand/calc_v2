import wiringpi2
import string
import music

class FakeI2C:
    def __init__(self, real_i):
        self.real_i = real_i
    
    def write(self, *args, **kwargs):
        print(repr((args, kwargs)))
        return self.real_i.write(*args, **kwargs)
    
    def __getattr__(self, a):
        return getattr(self.real_i, a)

class WriteToDisplay:
    def __init__(self):
        self.i = FakeI2C(wiringpi2.I2C())
        self.fst = self.i.setupInterface("/dev/i2c-1", 0x72)
        self.scd = self.i.setupInterface("/dev/i2c-1", 0x71)
        self.i.write(self.fst, 0x7A)
        self.i.write(self.fst, 0xFF)
        self.i.write(self.scd, 0x7A)
        self.i.write(self.scd, 0xFF)
        self.music_player = music.MusicPlayer()

    def get_range(self, display):
        if display == self.fst:
            return range(0, 4)
        elif display == self.scd:
            return range(4, 8)

    def which_display_to_talk_to(self, number):
        if number in self.get_range(self.fst):
            return self.fst
        elif number in self.get_range(self.scd):
            return self.scd

    def move_decimal_in_serial(self, move):
        display = self.which_display_to_talk_to(move)
        number = move % 4
        number = 2 ** number
        self.i.write(self.fst, 0x77)
        self.i.write(self.fst, 0)
        self.i.write(self.scd, 0x77)
        self.i.write(self.scd, 0)
        self.i.write(display, 0x77)
        self.i.write(display, number)

    def count_digits_without_decimals(self, string_number):
        idx = 0
        for num in string_number:
            if num in string.digits:
                idx += 1
        return idx

    def move_cursor_in_serial(self, move):
        display = self.which_display_to_talk_to(move)
        number = move % 4
        self.i.write(display, 0x79)
        self.i.write(display, number)

    def display_error(self):
        self.i.write(self.scd, 0x7E)
        self.i.write(self.scd, 0b1111001)

    def display_negative(self, position):
        display = self.which_display_to_talk_to(position)
        number = position % 4
        if number == 0:
            self.i.write(display, 0x7B)
        elif number == 1:
            self.i.write(display, 0x7C)
        elif number == 2:
            self.i.write(display, 0x7D)
        elif number == 3:
            self.i.write(display, 0x7E)
        self.i.write(display, 0b1000000)

    def write_new_values_to_display(self, string_number):
        self.i.write(self.fst, 0x76)
        self.i.write(self.scd, 0x76)
        if string_number == 'error':
            self.display_error()
        else:
            idx = 8 - self.count_digits_without_decimals(string_number)
            if idx < 0:
                pass
            else:
                self.move_cursor_in_serial(idx)
                for num in str(string_number):
                    if num == '.':
                        self.move_decimal_in_serial(idx - 1)
                    elif num == '-':
                        self.display_negative(idx - 1)
                    elif idx in range(0, 4):
                        self.i.write(self.fst, int(num))
                        idx += 1
                    elif idx in range(4, 8):
                        self.i.write(self.scd, int(num))
                        idx += 1

    def clear_displays(self):
        self.i.write(self.fst, 0x76)
        self.i.write(self.scd, 0x76)

