# rectangles.py
from points import Point


class Rectangle:
    """Klasa reprezentująca prostokąt na płaszczyźnie."""

    def __init__(self, x1, y1, x2, y2):
        self.pt1 = Point(x1, y1)
        self.pt2 = Point(x2, y2)

    def __str__(self):  # "[(x1, y1), (x2, y2)]"
        return f"[{self.pt1}, {self.pt2}]"

    def __repr__(self):  # "Rectangle(x1, y1, x2, y2)"
        return f"Rectangle({self.pt1.x}, {self.pt1.y}, {self.pt2.x}, {self.pt2.y})"

    def __eq__(self, other):  # obsługa rect1 == rect2
        if not isinstance(other, Rectangle):
            return False
        return self.pt1 == other.pt1 and self.pt2 == other.pt2

    def __ne__(self, other):  # obsługa rect1 != rect2
        return not self == other

    @property
    def center(self):
        """Zwraca środek prostokąta."""
        center_x = (self.pt1.x + self.pt2.x) / 2
        center_y = (self.pt1.y + self.pt2.y) / 2
        return Point(center_x, center_y)

    @property
    def top(self):
        """Zwraca górną współrzędną y prostokąta."""
        return max(self.pt1.y, self.pt2.y)

    @property
    def left(self):
        """Zwraca lewą współrzędną x prostokąta."""
        return min(self.pt1.x, self.pt2.x)

    @property
    def bottom(self):
        """Zwraca dolną współrzędną y prostokąta."""
        return min(self.pt1.y, self.pt2.y)

    @property
    def right(self):
        """Zwraca prawą współrzędną x prostokąta."""
        return max(self.pt1.x, self.pt2.x)

    @property
    def width(self):
        """Zwraca szerokość prostokąta."""
        return abs(self.pt2.x - self.pt1.x)

    @property
    def height(self):
        """Zwraca wysokość prostokąta."""
        return abs(self.pt2.y - self.pt1.y)

    @property
    def topleft(self):
        """Zwraca lewy górny punkt prostokąta."""
        return Point(self.left, self.top)

    @property
    def bottomleft(self):
        """Zwraca lewy dolny punkt prostokąta."""
        return Point(self.left, self.bottom)

    @property
    def topright(self):
        """Zwraca prawy górny punkt prostokąta."""
        return Point(self.right, self.top)

    @property
    def bottomright(self):
        """Zwraca prawy dolny punkt prostokąta."""
        return Point(self.right, self.bottom)

    def area(self):
        """Zwraca pole powierzchni prostokąta."""
        return self.width * self.height

    def move(self, x, y):
        """Przesuwa prostokąt o wektor (x, y)."""
        self.pt1 = Point(self.pt1.x + x, self.pt1.y + y)
        self.pt2 = Point(self.pt2.x + x, self.pt2.y + y)
        return self

    @classmethod
    def from_points(cls, points):
        """Tworzy prostokąt z listy lub krotki zawierającej dwa punkty.

        Args:
            points: Krotka lub lista dwóch punktów (Point)

        Returns:
            Rectangle: Nowy prostokąt utworzony z punktów

        Raises:
            ValueError: Jeśli podano nieprawidłową liczbę punktów
            TypeError: Jeśli elementy nie są instancjami klasy Point
        """
        if len(points) != 2:
            raise ValueError("Musisz podać dokładnie dwa punkty")

        point1, point2 = points

        if not isinstance(point1, Point) or not isinstance(point2, Point):
            raise TypeError("Oba elementy muszą być instancjami klasy Point")

        return cls(point1.x, point1.y, point2.x, point2.y)