from points import Point

class Triangle:
    """Klasa reprezentująca trójkąt na płaszczyźnie."""

    def __init__(self, x1, y1, x2, y2, x3, y3):
        self.pt1 = Point(x1, y1)
        self.pt2 = Point(x2, y2)
        self.pt3 = Point(x3, y3)

    def __str__(self): pass         # "[(x1, y1), (x2, y2), (x3, y3)]"

    def __repr__(self): pass        # "Triangle(x1, y1, x2, y2, x3, y3)"

    def __eq__(self, other): pass   # obsługa tr1 == tr2
        # Trójkąty powinny być równe, jeżeli mają ten sam zbiór wierzchołków,
        # niezależnie od kolejności pt1, pt2, pt3.

    def __ne__(self, other):        # obsługa tr1 != tr2
        return not self == other

    def center(self): pass          # zwraca środek (masy) trójkąta

    def area(self): pass            # pole powierzchni

    def move(self, x, y): pass      # przesunięcie o (x, y)

# Kod testujący moduł.

import unittest

class TestTriangle(unittest.TestCase): pass