# test_points.py
import unittest
import math
from points import Point


class TestPoint(unittest.TestCase):
    def setUp(self):
        self.p1 = Point(1, 2)
        self.p2 = Point(3, 4)
        self.p3 = Point(1, 2)
        self.p4 = Point(0, 0)
        self.p5 = Point(-1, -2)

    def test_init(self):
        self.assertEqual(self.p1.x, 1)
        self.assertEqual(self.p1.y, 2)

    def test_str(self):
        self.assertEqual(str(self.p1), "(1, 2)")
        self.assertEqual(str(self.p4), "(0, 0)")
        self.assertEqual(str(self.p5), "(-1, -2)")

    def test_repr(self):
        self.assertEqual(repr(self.p1), "Point(1, 2)")
        self.assertEqual(repr(self.p4), "Point(0, 0)")

    def test_eq(self):
        self.assertTrue(self.p1 == self.p3)
        self.assertFalse(self.p1 == self.p2)
        self.assertFalse(self.p1 == "not a point")

    def test_ne(self):
        self.assertTrue(self.p1 != self.p2)
        self.assertFalse(self.p1 != self.p3)

    def test_add(self):
        result = self.p1 + self.p2
        self.assertEqual(result.x, 4)
        self.assertEqual(result.y, 6)

        # Test z punktem zerowym
        result2 = self.p1 + self.p4
        self.assertEqual(result2, self.p1)

        # Test z ujemnymi
        result3 = self.p1 + self.p5
        self.assertEqual(result3, Point(0, 0))

    def test_sub(self):
        result = self.p2 - self.p1
        self.assertEqual(result.x, 2)
        self.assertEqual(result.y, 2)

        result2 = self.p1 - self.p1
        self.assertEqual(result2, Point(0, 0))

    def test_mul(self):
        # Iloczyn skalarny
        result = self.p1 * self.p2
        self.assertEqual(result, 1 * 3 + 2 * 4)
        self.assertEqual(result, 11)

        # Iloczyn skalarny z punktem zerowym
        result2 = self.p1 * self.p4
        self.assertEqual(result2, 0)

    def test_cross(self):
        # Iloczyn wektorowy
        result = self.p1.cross(self.p2)
        self.assertEqual(result, 1 * 4 - 2 * 3)
        self.assertEqual(result, -2)

        # Iloczyn wektorowy z samym sobą
        result2 = self.p1.cross(self.p1)
        self.assertEqual(result2, 0)

    def test_length(self):
        self.assertEqual(self.p4.length(), 0)
        self.assertEqual(self.p1.length(), math.sqrt(1 + 4))
        self.assertEqual(self.p5.length(), math.sqrt(1 + 4))

        # Test z punktem (3, 4) - długość 5
        p = Point(3, 4)
        self.assertEqual(p.length(), 5)

    def test_hash(self):
        # Punkty równe powinny mieć ten sam hash
        self.assertEqual(hash(self.p1), hash(self.p3))

        # Różne punkty powinny mieć różne hashe (z dużym prawdopodobieństwem)
        self.assertNotEqual(hash(self.p1), hash(self.p2))

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            self.p1 + "string"
        with self.assertRaises(TypeError):
            self.p1 - "string"
        with self.assertRaises(TypeError):
            self.p1 * "string"
        with self.assertRaises(TypeError):
            self.p1.cross("string")


if __name__ == "__main__":
    unittest.main()