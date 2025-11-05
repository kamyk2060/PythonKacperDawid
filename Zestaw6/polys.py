class Poly:
    """Klasa reprezentująca wielomiany."""

    # wg Sedgewicka - tworzymy wielomian c*x^n
    def __init__(self, c=0, n=0):
        self.size = n + 1       # rozmiar tablicy
        self.a = self.size * [0]
        self.a[self.size-1] = c

    def __str__(self):
        return str(self.a)

    def __add__(self, other): pass  # poly1 + poly2

    def __sub__(self, other): pass  # poly1 - poly2

    def __mul__(self, other): pass  # poly1 * poly2

    def __pos__(self): pass         # +poly1 = (+1)*poly1

    def __neg__(self): pass         # -poly1 = (-1)*poly1

    def __eq__(self, other): pass   # obsługa poly1 == poly2

    def __ne__(self, other):        # obsługa poly1 != poly2
        return not self == other

    def eval(self, x): pass         # schemat Hornera

    def combine(self, other):       # złożenie poly1(poly2(x))

    def __pow__(self, n): pass      # poly(x)**n lub pow(poly(x),n)

    def diff(self): pass            # różniczkowanie

    def integrate(self): pass       # całkowanie

    def is_zero(self): pass         # bool, True dla [0], [0, 0],...

# Kod testujący moduł.

import unittest

class TestPoly(unittest.TestCase): pass
