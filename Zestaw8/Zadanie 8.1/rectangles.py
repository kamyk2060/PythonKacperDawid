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

    def center(self):  # zwraca środek prostokąta
        center_x = (self.pt1.x + self.pt2.x) / 2
        center_y = (self.pt1.y + self.pt2.y) / 2
        return Point(center_x, center_y)

    def area(self):  # pole powierzchni
        width = abs(self.pt2.x - self.pt1.x)
        height = abs(self.pt2.y - self.pt1.y)
        return width * height

    def move(self, x, y):  # przesunięcie o (x, y)
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
        """
        if len(points) != 2:
            raise ValueError("Musisz podać dokładnie dwa punkty")

        point1, point2 = points

        if not isinstance(point1, Point) or not isinstance(point2, Point):
            raise TypeError("Oba elementy muszą być instancjami klasy Point")

        return cls(point1.x, point1.y, point2.x, point2.y)