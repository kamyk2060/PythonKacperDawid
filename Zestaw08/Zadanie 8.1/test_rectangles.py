# test_rectangles.py
import pytest
from points import Point
from rectangles import Rectangle


class TestRectangle:
    """Testy dla klasy Rectangle w formacie pytest."""

    @pytest.fixture
    def rect1(self):
        """Prostokąt testowy 1."""
        return Rectangle(0, 0, 3, 4)

    @pytest.fixture
    def rect2(self):
        """Prostokąt testowy 2."""
        return Rectangle(1, 1, 4, 5)

    @pytest.fixture
    def rect3(self):
        """Prostokąt testowy 3 (identyczny z rect1)."""
        return Rectangle(0, 0, 3, 4)

    def test_str(self, rect1):
        assert str(rect1) == "[(0, 0), (3, 4)]"

    def test_repr(self, rect1):
        assert repr(rect1) == "Rectangle(0, 0, 3, 4)"

    def test_eq(self, rect1, rect2, rect3):
        assert rect1 == rect3
        assert not (rect1 == rect2)

    def test_ne(self, rect1, rect2, rect3):
        assert rect1 != rect2
        assert not (rect1 != rect3)

    def test_center(self, rect1):
        center = rect1.center
        assert center.x == 1.5
        assert center.y == 2.0

    def test_area(self, rect1):
        assert rect1.area() == 12

    def test_move(self):
        rect = Rectangle(1, 1, 3, 3)
        rect.move(2, 3)
        assert rect.pt1 == Point(3, 4)
        assert rect.pt2 == Point(5, 6)

    def test_from_points_tuple(self, rect1):
        """Test tworzenia prostokąta z krotki punktów."""
        point1 = Point(0, 0)
        point2 = Point(3, 4)
        rect_from_tuple = Rectangle.from_points((point1, point2))
        assert rect_from_tuple == rect1

    def test_from_points_list(self, rect1):
        """Test tworzenia prostokąta z listy punktów."""
        point1 = Point(0, 0)
        point2 = Point(3, 4)
        rect_from_list = Rectangle.from_points([point1, point2])
        assert rect_from_list == rect1

    def test_from_points_invalid_count(self):
        """Test obsługi nieprawidłowej liczby punktów."""
        point1 = Point(0, 0)
        with pytest.raises(ValueError, match="Musisz podać dokładnie dwa punkty"):
            Rectangle.from_points((point1,))

    def test_from_points_invalid_type(self):
        """Test obsługi nieprawidłowego typu."""
        point1 = Point(0, 0)
        with pytest.raises(TypeError, match="Oba elementy muszą być instancjami klasy Point"):
            Rectangle.from_points((point1, "not_a_point"))

    def test_top_property(self):
        """Test właściwości top."""
        rect = Rectangle(1, 2, 5, 8)
        assert rect.top == 8

    def test_left_property(self):
        """Test właściwości left."""
        rect = Rectangle(1, 2, 5, 8)
        assert rect.left == 1

    def test_bottom_property(self):
        """Test właściwości bottom."""
        rect = Rectangle(1, 2, 5, 8)
        assert rect.bottom == 2

    def test_right_property(self):
        """Test właściwości right."""
        rect = Rectangle(1, 2, 5, 8)
        assert rect.right == 5

    def test_width_property(self):
        """Test właściwości width."""
        rect = Rectangle(1, 2, 5, 8)
        assert rect.width == 4

    def test_height_property(self):
        """Test właściwości height."""
        rect = Rectangle(1, 2, 5, 8)
        assert rect.height == 6

    def test_topleft_property(self):
        """Test właściwości topleft."""
        rect = Rectangle(1, 2, 5, 8)
        assert rect.topleft == Point(1, 8)

    def test_bottomleft_property(self):
        """Test właściwości bottomleft."""
        rect = Rectangle(1, 2, 5, 8)
        assert rect.bottomleft == Point(1, 2)

    def test_topright_property(self):
        """Test właściwości topright."""
        rect = Rectangle(1, 2, 5, 8)
        assert rect.topright == Point(5, 8)

    def test_bottomright_property(self):
        """Test właściwości bottomright."""
        rect = Rectangle(1, 2, 5, 8)
        assert rect.bottomright == Point(5, 2)

    def test_properties_with_reversed_coordinates(self):
        """Test właściwości gdy współrzędne są odwrócone."""
        rect = Rectangle(5, 8, 1, 2)  # odwrócone
        assert rect.left == 1
        assert rect.right == 5
        assert rect.bottom == 2
        assert rect.top == 8
        assert rect.width == 4
        assert rect.height == 6

    def test_properties_are_read_only(self, rect1):
        """Test że właściwości są tylko do odczytu."""
        with pytest.raises(AttributeError):
            rect1.top = 10
        with pytest.raises(AttributeError):
            rect1.left = 10
        with pytest.raises(AttributeError):
            rect1.width = 10
        with pytest.raises(AttributeError):
            rect1.center = Point(0, 0)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])