import string
import wiringpi2
import math
import time
import Test_circuit as tc
import buttons
import keypad
import display
import calc_string
import decimal
import fractions
import music

LEDS = [7, 8]

A_ENTRY, B_ENTRY, E_ENTRY = range(3)
OPERATORS = ['+', '-', '/', '*', '^']
NUMBERS = {'pi':math.pi, 'e':math.e, 'tau':math.pi * 2}
CLEAR = ['clear']


def remove_zeros(string_number):
    if '.' in string_number and string_number[-1] == '0':
        return remove_zeros(string_number[:-1])
    else:
        return string_number

def convert_frac_to_string(frac_str):
    number = fractions.Fraction(frac_str)
    return str(number.numerator / number.denominator)

#print(convert_frac_to_string('-1/2'))

def round_number(number):
    if number == '':
        return ''
    string_number = convert_frac_to_string(number)
    if '.' in string_number:
        point = string_number.index('.')
        if point > 8:
            return ''
        else:
            if number[0] == '-':
                decimal.getcontext().prec = 7
            else:
                decimal.getcontext().prec = 8
            return remove_zeros(str(decimal.Decimal(float(string_number)) / decimal.Decimal(1)))
    elif len(string_number) <= 8:
        return string_number
    else:
        return ''

#print(round_number('1.23456789'))
#print(round_number('123456789'))
#print(round_number(calc_string.final_sum_string(['..1'])))


class Calculator:
    def __init__(self):
        self.sum_so_far = []
        self.state = A_ENTRY
    def display(self):
        #print(self.sum_so_far)
        if self.state == A_ENTRY or self.state == B_ENTRY:
            # If sum_so_far is empty print a 0
            #print('a')
            if not self.sum_so_far:
                #print('zero')
                return '0'
            elif self.sum_so_far == ['zeroerror']:
                ##print('error')
                return 'error'
            # If the last item in sum_so_far is an operation print the second to last item in sum_so_far
            elif self.sum_so_far[-1][-1] in OPERATORS:
                number = round_number(calc_string.final_sum_string([self.sum_so_far[-2]]))
                if number == '':
                    self.state == E_ENTRY
                    #print('error')
                    return 'error'
                else:
                    #print(number)
                    return number
            # Else print the last item in sum_so_far
            else:
                number = round_number(calc_string.final_sum_string([self.sum_so_far[-1]]))
                if number == '':
                    self.state == E_ENTRY
                    #print('error')
                    return 'error'
                else:
                    #print(number)
                    return number
        elif self.state == E_ENTRY:
            return 'error'
        else:
            assert(False)
    def clear_calc(self):
        self.sum_so_far = []
        self.state = A_ENTRY
    def key(self, k):
        print('key')
        print(k)
        if k in CLEAR:
            self.clear_calc()
        elif k == '=':
            self.sum_so_far = [str(calc_string.final_sum(self.sum_so_far))]
            self.state = A_ENTRY
        elif k in OPERATORS:
            if self.sum_so_far:
                if self.sum_so_far[-1][0] in OPERATORS:
                    self.sum_so_far[-1] += k
                else:
                    self.sum_so_far.append(k)
            self.state = A_ENTRY
        elif k in string.digits or k == '.':
            if self.state == A_ENTRY:
                self.sum_so_far.append(k)
                self.state = B_ENTRY
            elif self.state == B_ENTRY:
                if self.sum_so_far[-1] in NUMBERS.keys():
                    self.clear_calc()
                    self.sum_so_far = [k]
                elif self.sum_so_far[-1][0] in string.digits or self.sum_so_far[-1][0] in '.':
                    self.sum_so_far[-1] += k
        elif k in NUMBERS.keys():
            if self.state == A_ENTRY:
                self.sum_so_far.append(str(NUMBERS[k]))
            elif self.state == B_ENTRY:
                self.clear_calc()
                self.sum_so_far = [str(NUMBERS[k])]

list_of_relevent_characters = [n for n in string.digits] + list(NUMBERS.keys()) + OPERATORS + CLEAR + ['='] + ['.']

class CalcSums:
    def __init__(self):
        self.calc = Calculator()
        self.multiple_leds = tc.SetofLights(LEDS)
        self.button_inst = buttons.PressButton()
        self.display_inst = display.WriteToDisplay()
        self.keypad_inst = keypad.Keypad()
        self.music_player = music.MusicPlayer()

    def find_input(self):
        start_time = time.time()
        while True:
            current_time = time.time()
            if (current_time - start_time) > 2:
                self.music_player.pause_music()
            button = self.button_inst.scan()
            key = self.keypad_inst.scan()
            if button:
                return button
            elif key:
                return key

    def do_sums(self):
        while True:
            digit = self.find_input()
            self.music_player.play_music()
            if digit == 'kill':
                return ''
            else:
                self.calc.key(digit)
                self.multiple_leds.rotate_one_on()
                to_be_displayed = self.calc.display()
                if to_be_displayed == 'error':
                    self.display_inst.write_new_values_to_display(to_be_displayed)
                    self.music_player.change_music(music.error_song)
                    self.music_player.play_music()
                    time.sleep(12)
                    self.music_player.change_music(music.default_song)
                elif to_be_displayed == '5678':
                    self.display_inst.write_new_values_to_display(to_be_displayed)
                    self.music_player.change_music(music.song_5678)
                    self.music_player.play_music()
                    time.sleep(12)
                    self.music_player.change_music(music.default_song)
                else:
                    self.display_inst.write_new_values_to_display(to_be_displayed)
            time.sleep(0.5)
            

if __name__ == '__main__':
    calc_sums = CalcSums()
    calc_sums.display_inst.write_new_values_to_display('0')
    calc_sums.do_sums()
    calc_sums.display_inst.clear_displays()    
    calc_sums.multiple_leds.all_off()


