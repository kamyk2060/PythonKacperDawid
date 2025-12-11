import math


class Frac:
    """Klasa reprezentująca ułamki."""

    def __init__(self, x=0, y=1):
        if y == 0:
            raise ValueError("Mianownik nie może być zerem")

        # Konwersja z float
        if isinstance(x, float):
            x, y = x.as_integer_ratio()
        elif isinstance(y, float):
            x_ratio = x.as_integer_ratio() if isinstance(x, float) else (x, 1)
            y_ratio = y.as_integer_ratio() if isinstance(y, float) else (y, 1)
            x = x_ratio[0] * y_ratio[1]
            y = x_ratio[1] * y_ratio[0]

        # Konwersja z Frac
        if isinstance(x, Frac):
            self.x = x.x
            self.y = x.y
        elif isinstance(y, Frac):
            self.x = x * y.y
            self.y = y.x
        else:
            self.x = x
            self.y = y

        # Sprowadzenie do najprostszej postaci
        self._simplify()

    def _simplify(self):
        """Sprowadza ułamek do najprostszej postaci."""
        gcd = math.gcd(self.x, self.y)
        self.x //= gcd
        self.y //= gcd

        # Upewniamy się, że mianownik jest dodatni
        if self.y < 0:
            self.x = -self.x
            self.y = -self.y

    def __str__(self):
        if self.y == 1:
            return str(self.x)
        return f"{self.x}/{self.y}"

    def __repr__(self):
        return f"Frac({self.x}, {self.y})"

    def __eq__(self, other):
        if isinstance(other, (int, float)):
            other = Frac(other)
        if isinstance(other, Frac):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if isinstance(other, (int, float)):
            other = Frac(other)
        if isinstance(other, Frac):
            return self.x * other.y < other.x * self.y
        return NotImplemented

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other

    def __add__(self, other):
        if isinstance(other, (int, float)):
            other = Frac(other)
        if isinstance(other, Frac):
            return Frac(self.x * other.y + other.x * self.y, self.y * other.y)
        return NotImplemented

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            other = Frac(other)
        if isinstance(other, Frac):
            return Frac(self.x * other.y - other.x * self.y, self.y * other.y)
        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            return Frac(other) - self
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            other = Frac(other)
        if isinstance(other, Frac):
            return Frac(self.x * other.x, self.y * other.y)
        return NotImplemented

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            other = Frac(other)
        if isinstance(other, Frac):
            return Frac(self.x * other.y, self.y * other.x)
        return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            return Frac(other) / self
        return NotImplemented

    # Dla kompatybilności z Python 2
    __div__ = __truediv__
    __rdiv__ = __rtruediv__

    def __pos__(self):
        return self

    def __neg__(self):
        return Frac(-self.x, self.y)

    def __invert__(self):
        return Frac(self.y, self.x)

    def __float__(self):
        return self.x / self.y

    def __hash__(self):
        return hash(float(self))