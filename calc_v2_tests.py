import calc_v2
import unittest

class Tests(unittest.TestCase):
    def setUp(self):
        self.c = calc_v2.Calculator()

    def test_one_plus_two(self):
        self.assertEqual(self.c.display(), '0')
        self.c.key('1')
        self.assertEqual(self.c.display(), '1')
        self.c.key('+')
        self.assertEqual(self.c.display(), '1')
        self.c.key('2')
        self.assertEqual(self.c.display(), '2')
        self.c.key('=')
        self.assertEqual(self.c.display(), '3')

    def test_add_more_after_add(self):
        for k in '1+2=+':
            self.c.key(k)
        self.assertEqual(self.c.display(), '3')
        self.c.key('4')
        self.assertEqual(self.c.display(), '4')
        self.c.key('=')
        self.assertEqual(self.c.display(), '7')

    def test_add_three_numbers(self):
        #import nose; nose.tools.set_trace()
        self.assertEqual(self.c.display(), '0')
        self.c.key('1')
        self.assertEqual(self.c.display(), '1')
        self.c.key('+')
        self.assertEqual(self.c.display(), '1')
        self.c.key('2')
        self.assertEqual(self.c.display(), '2')
        self.c.key('+')
        self.assertEqual(self.c.display(), '3')
        self.c.key('3')
        self.assertEqual(self.c.display(), '3')
        self.c.key('=')
        self.assertEqual(self.c.display(), '6')
        
    def test_number_after_equals_without_operator(self):
        self.assertEqual(self.c.display(), '0')
        self.c.key('2')
        self.assertEqual(self.c.display(), '2')
        self.c.key('=')
        self.assertEqual(self.c.display(), '2')
        self.c.key('5')
        self.assertEqual(self.c.display(), '5')

    def test_double_equals(self):
        self.assertEqual(self.c.display(), '0')
        self.c.key('1')
        self.assertEqual(self.c.display(), '1')
        self.c.key('+')
        self.assertEqual(self.c.display(), '1')
        self.c.key('2')
        self.assertEqual(self.c.display(), '2')
        self.c.key('=')
        self.assertEqual(self.c.display(), '3')
        self.c.key('=')
        self.assertEqual(self.c.display(), '3')
