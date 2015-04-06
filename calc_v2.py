import string
import math



A_ENTRY, B_ENTRY = range(2)
OPERATIONS = ['+', '-', '/', '*']
#NUMBERS = {'pi':math.pi, 'e':math.e}


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
        elif self.o == None:
            self.a = self.b
        else:
            assert(False)
        self.b = 0
    def key(self, k):
        if self.state == A_ENTRY:
            if k == '=':
                self.a = self.a
                self.b = self.b
                self.o = None
                self.state = A_ENTRY
            elif k in string.digits:
                self.a = self.a
                self.b = int(k)
                self.o = self.o
                self.state = B_ENTRY
            elif k == '.':
                self.a = self.a
                self.b = 0
                self.decimal = 1
                self.o - self.o
                self.state = B_ENTRY
            elif k in OPERATIONS:
                self.a = self.a
                self.b = self.b
                self.o = k
                self.state = A_ENTRY
        elif self.state == B_ENTRY:
            if k == '=':
                self.apply_operation()
                self.o = None
                self.state = A_ENTRY
            elif k in string.digits:
                if self.decimal == 0:
                    self.a = self.a
                    self.b = (self.b * 10) + int(k)
                    self.o = self.o
                    self.state = self.state
                else:
                    self.a = self.a
                    self.b = self.b + (int(k) * 10**(-self.decimal))
                    self.o = self.o
                    self.state = self.state
            elif k == '.':
                if self.decimal == 0:
                    self.a = self.a
                    self.b = self.b
                    self.decimal = 1
                    self.o = self.o
                    self.state = self.state
                else:
                    self.a = self.a
                    self.b = self.b
                    self.decimal = self.decimal
                    self.o = self.o
                    self.state = self.state
            elif k in OPERATIONS:
                self.apply_operation()
                self.o = k
                self.state = A_ENTRY


if __name__ == '__main__':
    c = Calculator()
    while True:
        print (c.display())
        k = input()
    c.key(k)
