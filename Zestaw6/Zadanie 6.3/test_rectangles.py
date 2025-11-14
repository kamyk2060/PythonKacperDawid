# test_rectangles.py
import unittest
from points import Point
from rectangles import Rectangle

class TestRectangle(unittest.TestCase):
    def setUp(self):
        self.rect1 = Rectangle(0, 0, 3, 4)
        self.rect2 = Rectangle(1, 1, 4, 5)
        self.rect3 = Rectangle(0, 0, 3, 4)

    def test_str(self):
        self.assertEqual(str(self.rect1), "[(0, 0), (3, 4)]")

    def test_repr(self):
        self.assertEqual(repr(self.rect1), "Rectangle(0, 0, 3, 4)")

    def test_eq(self):
        self.assertTrue(self.rect1 == self.rect3)
        self.assertFalse(self.rect1 == self.rect2)

    def test_ne(self):
        self.assertTrue(self.rect1 != self.rect2)
        self.assertFalse(self.rect1 != self.rect3)

    def test_center(self):
        center = self.rect1.center()
        self.assertEqual(center.x, 1.5)
        self.assertEqual(center.y, 2.0)

    def test_area(self):
        self.assertEqual(self.rect1.area(), 12)

    def test_move(self):
        rect = Rectangle(1, 1, 3, 3)
        rect.move(2, 3)
        self.assertEqual(rect.pt1, Point(3, 4))
        self.assertEqual(rect.pt2, Point(5, 6))

if __name__ == "__main__":
    unittest.main()