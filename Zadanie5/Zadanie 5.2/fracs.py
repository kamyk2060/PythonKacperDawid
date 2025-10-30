
from math import gcd   # Py3


def normalizacja(frac):
    """Normalizuje ułamek - upewnia się, że mianownik jest dodatni i skraca ułamek"""
    if frac[1] == 0:
        raise ValueError("Mianownik nie może być zerem")

    licznik, mianownik = frac[0], frac[1]

    # Upewnij się, że mianownik jest dodatni
    if mianownik < 0:
        licznik = -licznik
        mianownik = -mianownik

    # Znajdź NWD i skróć ułamek
    nwd_val = gcd(int(abs(licznik)), int(abs(mianownik)))

    if nwd_val > 1:
        licznik = licznik // nwd_val
        mianownik = mianownik // nwd_val

    return [int(licznik), int(mianownik)]


def add_frac(frac1, frac2):        # frac1 + frac2
    licznik1, mianownik1 = frac1[0], frac1[1]
    licznik2, mianownik2 = frac2[0], frac2[1]

    wspolny_mianownik = mianownik1 * mianownik2
    wspolny_licznik = licznik1 * mianownik2 + licznik2 * mianownik1

    return normalizacja([wspolny_licznik, wspolny_mianownik])

def sub_frac(frac1, frac2):         # frac1 - frac2
    licznik1, mianownik1 = frac1[0], frac1[1]
    licznik2, mianownik2 = frac2[0], frac2[1]

    wspolny_mianownik = mianownik1 * mianownik2
    wspolny_licznik = licznik1 * mianownik2 - licznik2 * mianownik1

    return normalizacja([wspolny_licznik, wspolny_mianownik])

def mul_frac(frac1, frac2):        # frac1 * frac2
    licznik1, mianownik1 = frac1[0], frac1[1]
    licznik2, mianownik2 = frac2[0], frac2[1]

    wspolny_mianownik = mianownik1 * mianownik2
    wspolny_licznik = licznik1 * licznik2

    return normalizacja([wspolny_licznik, wspolny_mianownik])


def div_frac(frac1, frac2):       # frac1 / frac2
    licznik1, mianownik1 = frac1[0], frac1[1]
    licznik2, mianownik2 = frac2[0], frac2[1]

    if frac2[0] == 0:
        raise ValueError("Nie można dzielić przez zero")

    wspolny_mianownik = mianownik1 * licznik2
    wspolny_licznik = licznik1 * mianownik2

    return normalizacja([wspolny_licznik, wspolny_mianownik])

def is_positive(frac):              # bool, czy dodatni
    licznik1, mianownik1 = frac[0], frac[1]

    if (licznik1 > 0) and (mianownik1 > 0):
        return True
    if (licznik1 < 0) and (mianownik1 < 0):
        return True
    return False

def is_zero(frac):                 # bool, typu [0, x]
    licznik1, mianownik1 = frac[0], frac[1]
    if licznik1 == 0:
        return True

def cmp_frac(frac1, frac2):       # -1 | 0 | +1
    licznik1, mianownik1 = frac1[0], frac1[1]
    licznik2, mianownik2 = frac2[0], frac2[1]

    wspolny_mianownik = licznik1 * mianownik2
    licznik1 = licznik1 * mianownik2
    licznik2 = licznik2 * mianownik1

    if licznik1 < licznik2:
        return -1
    elif licznik1 > licznik2:
        return 1
    else:
        return 0


def frac2float(frac):            # konwersja do float
    licznik1, mianownik1 = frac[0], frac[1]

    return licznik1/mianownik1


# f1 = [-1, 2]      # -1/2
# f2 = [1, -2]      # -1/2 (niejednoznaczność)
# f3 = [0, 1]       # zero
# f4 = [0, 2]       # zero (niejednoznaczność)
# f5 = [3, 1]       # 3
# f6 = [6, 2]       # 3 (niejednoznaczność)

import unittest

class TestFractions(unittest.TestCase):

    def setUp(self):
        self.zero = [0, 1]

    def test_add_frac(self):
        self.assertEqual(add_frac([1, 2], [1, 3]), [5, 6])
        self.assertEqual(add_frac([1, -2], [1, 2]), [0, 1])

    def test_sub_frac(self):
        self.assertEqual(sub_frac([1, 2], [1, 3]), [1, 6])
        self.assertEqual(sub_frac([3, 4], [1, 4]), [1, 2])

    def test_mul_frac(self):
        self.assertEqual(mul_frac([3, 4], [4, 3]), [1, 1])
        self.assertEqual(mul_frac([-1, 2], [1, 2]), [-1, 4])

    def test_div_frac(self):
        self.assertEqual(div_frac([3, 4], [3, 4]), [1, 1])
        self.assertEqual(div_frac([-1, 2], [1, 2]), [-1, 1])

    def test_is_positive(self):
        self.assertTrue(is_positive([1, 2]))
        self.assertTrue(is_positive([-1, -2]))
        self.assertFalse(is_positive([-1, 2]))
        self.assertFalse(is_positive([0, 1]))

    def test_is_zero(self):
        self.assertTrue(is_zero([0, 5]))
        self.assertFalse(is_zero([1, 2]))

    def test_cmp_frac(self):
        self.assertEqual(cmp_frac([1, 2], [1, 3]), 1)
        self.assertEqual(cmp_frac([1, 3], [1, 2]), -1)
        self.assertEqual(cmp_frac([1, 2], [1, 2]), 0)

    def test_frac2float(self):
        self.assertAlmostEqual(frac2float([3, 4]), 0.75)
        self.assertAlmostEqual(frac2float([-1, 2]), -0.5)

    def tearDown(self): pass

if __name__ == '__main__':
    unittest.main()     # uruchamia wszystkie testy
