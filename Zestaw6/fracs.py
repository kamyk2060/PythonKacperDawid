#from fractions import gcd   # Py2
from math import gcd   # Py3

class Frac:
    """Klasa reprezentująca ułamek."""

    def __init__(self, x=0, y=1):
        self.x = x
        self.y = y

    def __str__(self): pass         # zwraca "x/y" lub "x" dla y=1

    def __repr__(self): pass        # zwraca "Frac(x, y)"

    #def __cmp__(self, other): pass  # cmp(frac1, frac2)    # Py2

    def __eq__(self, other): pass    # Py2.7 i Py3

    def __ne__(self, other): pass

    def __lt__(self, other): pass

    def __le__(self, other): pass

    #def __gt__(self, other): pass

    #def __ge__(self, other): pass

    def __add__(self, other): pass  # frac1 + frac2

    def __sub__(self, other): pass  # frac1 - frac2

    def __mul__(self, other): pass  # frac1 * frac2

    def __div__(self, other): pass  # frac1 / frac2, Py2

    def __truediv__(self, other): pass  # frac1 / frac2, Py3

    def __floordiv__(self, other): pass  # frac1 // frac2, opcjonalnie

    def __mod__(self, other): pass  # frac1 % frac2, opcjonalnie

    # operatory jednoargumentowe
    def __pos__(self):  # +frac = (+1)*frac
        return self

    def __neg__(self):  # -frac = (-1)*frac
        return Frac(-self.x, self.y)

    def __invert__(self):  # odwrotnosc: ~frac
        return Frac(self.y, self.x)

    def __float__(self): pass       # float(frac)

    def __hash__(self):
        return hash(float(self))   # immutable fracs
        # w Pythonie set([2]) == set([2.0])
        # chcemy set([2]) == set([Frac(2)])

# Kod testujący moduł.

import unittest

class TestFrac(unittest.TestCase): pass