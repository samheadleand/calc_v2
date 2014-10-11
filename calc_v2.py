import string

A_ENTRY, B_ENTRY_0, B_ENTRY_N = range(3)

class Calculator:
    def __init__(self):
        self.a = 0
        self.b = 0
        self.state = A_ENTRY
    def display(self):
        if self.state == A_ENTRY:
            return str(self.a)
        elif self.state == B_ENTRY_0:
            return str(self.a)
        elif self.state == B_ENTRY_N:
            return str(self.b)
        else:
            assert(False)
    def key(self, k):
        if self.state == A_ENTRY:
            if k == '=':
                return
            elif k in string.digits:
                self.a = int(k)
            elif k == '+':
                self.state = B_ENTRY_0
            else:
                assert(False)
        elif self.state == B_ENTRY_0:
            if k == '=':
                return
            elif k in string.digits:
                self.b = int(k)
                self.state = B_ENTRY_N
            elif k == '+':
                return
            else:
                assert(False)
        elif self.state == B_ENTRY_N:
            if k == '=':
                self.a += self.b
                self.b = 0
                self.state = A_ENTRY
            elif k in string.digits:
                return
            elif k == '+':
                return
            else:
                assert(False)
