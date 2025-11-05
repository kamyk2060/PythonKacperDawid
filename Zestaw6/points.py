class Point:
    """Klasa reprezentująca punkty na płaszczyźnie."""

    def __init__(self, x, y):  # konstuktor
        self.x = x
        self.y = y

    def __str__(self):  # zwraca string "(x, y)"
        return f"({self.x}, {self.y})"

    def __repr__(self):  # zwraca string "Point(x, y)"
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other):  # obsługa point1 == point2
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):  # obsługa point1 != point2
        return not self == other

    # Punkty jako wektory 2D.
    def __add__(self, other):  # v1 + v2
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):  # v1 - v2
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):  # v1 * v2, iloczyn skalarny, zwraca liczbę
        return self.x * other.x + self.y * other.y

    def cross(self, other):  # v1 x v2, iloczyn wektorowy 2D, zwraca liczbę
        return self.x * other.y - self.y * other.x

    def length(self):  # długość wektora
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __hash__(self):
        return hash((self.x, self.y))  # bazujemy na tuple, immutable points


# Kod testujący moduł.

import unittest
import math


class TestPoint(unittest.TestCase):
    def test_constructor(self):
        p = Point(3, 4)
        self.assertEqual(p.x, 3)
        self.assertEqual(p.y, 4)

    def test_str(self):
        p = Point(2, 5)
        self.assertEqual(str(p), "(2, 5)")

    def test_repr(self):
        p = Point(-1, 3)
        self.assertEqual(repr(p), "Point(-1, 3)")

    def test_eq(self):
        p1 = Point(1, 2)
        p2 = Point(1, 2)
        p3 = Point(3, 4)
        self.assertTrue(p1 == p2)
        self.assertFalse(p1 == p3)

    def test_ne(self):
        p1 = Point(1, 2)
        p2 = Point(3, 4)
        self.assertTrue(p1 != p2)
        self.assertFalse(p1 != Point(1, 2))

    def test_add(self):
        p1 = Point(1, 2)
        p2 = Point(3, 4)
        result = p1 + p2
        self.assertEqual(result, Point(4, 6))

    def test_sub(self):
        p1 = Point(5, 7)
        p2 = Point(2, 3)
        result = p1 - p2
        self.assertEqual(result, Point(3, 4))

    def test_mul(self):
        p1 = Point(2, 3)
        p2 = Point(4, 5)
        result = p1 * p2
        self.assertEqual(result, 2 * 4 + 3 * 5)  # 8 + 15 = 23
        self.assertEqual(result, 23)

    def test_cross(self):
        p1 = Point(2, 3)
        p2 = Point(4, 5)
        result = p1.cross(p2)
        self.assertEqual(result, 2 * 5 - 3 * 4)  # 10 - 12 = -2
        self.assertEqual(result, -2)

    def test_length(self):
        p1 = Point(3, 4)
        self.assertEqual(p1.length(), 5.0)  # sqrt(3^2 + 4^2) = 5

        p2 = Point(0, 0)
        self.assertEqual(p2.length(), 0.0)

        p3 = Point(1, 1)
        self.assertAlmostEqual(p3.length(), math.sqrt(2))

    def test_edge_cases(self):
        # Punkty z wartościami ujemnymi
        p1 = Point(-2, -3)
        p2 = Point(-1, -1)
        self.assertEqual(p1 + p2, Point(-3, -4))
        self.assertEqual(p1 - p2, Point(-1, -2))

        # Punkty z wartościami zmiennoprzecinkowymi
        p3 = Point(1.5, 2.5)
        p4 = Point(0.5, 1.5)
        self.assertEqual(p3 + p4, Point(2.0, 4.0))
        self.assertAlmostEqual(p3.length(), (1.5 ** 2 + 2.5 ** 2) ** 0.5)


if __name__ == '__main__':
    unittest.main()