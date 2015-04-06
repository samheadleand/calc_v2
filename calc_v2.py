import string
import math



A_ENTRY, B_ENTRY = range(2)
OPERATIONS = ['+', '-', '/', '*', '^']
NUMBERS = {'pi':math.pi, 'e':math.e, 'tau':math.pi * 2}
CLEAR = ['clear']


class Calculator:
    def __init__(self):
        self.a = 0
        self.b = 0
        self.decimal = 0
        self.o = None
        self.state = A_ENTRY
    def display(self):
        if self.state == A_ENTRY:
            return str(self.a)
        elif self.state == B_ENTRY:
            return str(self.b)
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
                self.o = k
            elif k in NUMBERS.keys():
                self.b = NUMBERS[k]
                self.apply_operation()
                self.operation = None
        elif self.state == B_ENTRY:
            if k == '=':
                self.apply_operation()
                self.o = None
                self.state = A_ENTRY
            elif k in string.digits:
                if self.decimal == 0:
                    self.b = (self.b * 10) + int(k)
                else:
                    self.b = self.b + (int(k) * 10**(-self.decimal))
                    self.decimal += 1
            elif k == '.':
                if self.decimal == 0:
                    self.decimal = 1
            elif k in OPERATIONS:
                self.apply_operation()
                self.o = k
                self.state = A_ENTRY
            elif k in NUMBERS.keys():
                self.a = NUMBERS[k]
                self.b = 0
                self.decimal = 0
                self.o = None
                self.state = A_ENTRY


#if __name__ == '__main__':
#    c = Calculator()
#    while True:
#        print (c.display())
#        k = input()
#    c.key(k)
