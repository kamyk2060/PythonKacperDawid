import unittest
from fracs import Frac


class TestFrac(unittest.TestCase):

    def test_init(self):
        # Podstawowa inicjalizacja
        self.assertEqual(str(Frac(1, 2)), "1/2")
        self.assertEqual(str(Frac(3, 1)), "3")
        self.assertEqual(str(Frac()), "0")

        # Uproszczenie
        self.assertEqual(str(Frac(2, 4)), "1/2")
        self.assertEqual(str(Frac(4, 2)), "2")
        self.assertEqual(str(Frac(-2, 4)), "-1/2")
        self.assertEqual(str(Frac(2, -4)), "-1/2")

        # Wyjątek dla zerowego mianownika
        with self.assertRaises(ValueError):
            Frac(1, 0)

    def test_float_conversion(self):
        # Konwersja z float
        f1 = Frac(0.5)
        self.assertEqual(str(f1), "1/2")

        f2 = Frac(0.25)
        self.assertEqual(str(f2), "1/4")

    def test_arithmetic(self):
        f1 = Frac(1, 2)
        f2 = Frac(1, 3)

        # Dodawanie
        self.assertEqual(f1 + f2, Frac(5, 6))
        self.assertEqual(f1 + 1, Frac(3, 2))
        self.assertEqual(1 + f1, Frac(3, 2))

        # Odejmowanie
        self.assertEqual(f1 - f2, Frac(1, 6))
        self.assertEqual(f1 - 1, Frac(-1, 2))
        self.assertEqual(1 - f1, Frac(1, 2))

        # Mnożenie
        self.assertEqual(f1 * f2, Frac(1, 6))
        self.assertEqual(f1 * 2, Frac(1, 1))
        self.assertEqual(2 * f1, Frac(1, 1))

        # Dzielenie
        self.assertEqual(f1 / f2, Frac(3, 2))
        self.assertEqual(f1 / 2, Frac(1, 4))
        self.assertEqual(2 / f1, Frac(4, 1))

    def test_comparison(self):
        f1 = Frac(1, 2)
        f2 = Frac(1, 3)
        f3 = Frac(2, 4)

        self.assertTrue(f1 > f2)
        self.assertTrue(f2 < f1)
        self.assertTrue(f1 == f3)
        self.assertTrue(f1 != f2)
        self.assertTrue(f1 >= f3)
        self.assertTrue(f1 <= f3)

        # Porównania z int/float
        self.assertTrue(f1 == 0.5)
        self.assertTrue(f1 < 1)
        self.assertTrue(f1 > 0.3)
        self.assertTrue(0.5 == f1)
        self.assertTrue(1 > f1)
        self.assertTrue(0.3 < f1)

    def test_unary_operators(self):
        f1 = Frac(1, 2)

        self.assertEqual(+f1, f1)
        self.assertEqual(-f1, Frac(-1, 2))
        self.assertEqual(~f1, Frac(2, 1))

    def test_float_conversion_method(self):
        f1 = Frac(1, 2)
        f2 = Frac(3, 4)

        self.assertEqual(float(f1), 0.5)
        self.assertEqual(float(f2), 0.75)

    def test_hash(self):
        f1 = Frac(1, 2)
        f2 = Frac(2, 4)

        self.assertEqual(hash(f1), hash(f2))
        self.assertEqual(hash(f1), hash(0.5))

    def test_repr(self):
        f1 = Frac(1, 2)
        self.assertEqual(repr(f1), "Frac(1, 2)")

    def test_mixed_operations(self):
        # Operacje mieszane z float
        f1 = Frac(1, 2)

        self.assertEqual(f1 + 0.5, Frac(1, 1))
        self.assertEqual(0.5 + f1, Frac(1, 1))
        self.assertEqual(f1 * 0.5, Frac(1, 4))
        self.assertEqual(0.5 * f1, Frac(1, 4))


if __name__ == '__main__':
    unittest.main()