from pytest import approx
from math import sqrt
from r2point import R2Point
from convex import Figure, Void, Point, Segment, Polygon


class TestVoid:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Void()

    # Нульугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Void (нульугольник)
    def test_void(self):
        assert isinstance(self.f, Void)

    # Периметр нульугольника нулевой
    def test_perimeter(self):
        assert self.f.perimeter() == 0.0

    # Площадь нульугольника нулевая
    def test_аrea(self):
        assert self.f.area() == 0.0

    # Число острых углов нульугольника нулевое
    def test_angle_number(self):
        assert self.f.angle_number() == 0

    # При добавлении точки нульугольник превращается в одноугольник
    def test_add(self):
        assert isinstance(self.f.add(R2Point(0.0, 0.0)), Point)


class TestPoint:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Point(R2Point(0.0, 0.0))

    # Одноугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Point (одноугольник)
    def test_point(self):
        assert isinstance(self.f, Point)

    # Периметр одноугольника нулевой
    def test_perimeter(self):
        assert self.f.perimeter() == 0.0

    # Площадь одноугольника нулевая
    def test_аrea(self):
        assert self.f.area() == 0.0

    # Число острых углов одноугольника нулевое
    def test_angle_number(self):
        assert self.f.angle_number() == 0

    # При добавлении точки одноугольник может не измениться
    def test_add1(self):
        assert self.f.add(R2Point(0.0, 0.0)) is self.f

    # При добавлении точки одноугольник может превратиться в двуугольник
    def test_add2(self):
        assert isinstance(self.f.add(R2Point(1.0, 0.0)), Segment)


class TestSegment:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Segment(R2Point(0.0, 0.0), R2Point(1.0, 0.0))

    # Двуугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Segment (двуугольник)
    def test_segment(self):
        assert isinstance(self.f, Segment)

    # Периметр двуугольника равен удвоенной длине отрезка
    def test_perimeter(self):
        assert self.f.perimeter() == approx(2.0)

    # Площадь двуугольника нулевая
    def test_аrea(self):
        assert self.f.area() == 0.0

    # Число острых углов двуугольника нулевое
    def test_angle_number(self):
        assert self.f.angle_number() == 0

    # При добавлении точки двуугольник может не измениться
    def test_add1(self):
        assert self.f.add(R2Point(0.5, 0.0)) is self.f

    # При добавлении точки правее двуугольник может превратиться в другой
    # двуугольник
    def test_add2(self):
        assert isinstance(self.f.add(R2Point(2.0, 0.0)), Segment)

    # При добавлении точки левее двуугольник может превратиться в другой
    # двуугольник
    def test_add3(self):
        assert isinstance(self.f.add(R2Point(-1.0, 0.0)), Segment)

    # При добавлении точки двуугольник может превратиться в треугольник
    def test_add4(self):
        assert isinstance(self.f.add(R2Point(0.0, 1.0)), Polygon)


class TestPolygon:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.a = R2Point(0.0, 0.0)
        self.b = R2Point(1.0, 0.0)
        self.c = R2Point(0.0, 1.0)
        self.f = Polygon(self.a, self.b, self.c)

    # Многоугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Polygon (многоугольник)
    def test_polygon1(self):
        assert isinstance(self.f, Polygon)

    # Изменение порядка точек при создании объекта всё равно порождает Polygon
    def test_polygon2(self):
        self.f = Polygon(self.b, self.a, self.c)
        assert isinstance(self.f, Polygon)

    # Изменение количества вершин многоугольника
    #   изначально их три
    def test_vertexes1(self):
        assert self.f.points.size() == 3

    #   добавление точки внутрь многоугольника не меняет их количества
    def test_vertexes2(self):
        assert self.f.add(R2Point(0.1, 0.1)).points.size() == 3

    #   добавление другой точки может изменить их количество
    def test_vertexes3(self):
        assert self.f.add(R2Point(1.0, 1.0)).points.size() == 4

    #   изменения выпуклой оболочки могут и уменьшать их количество
    def test_vertexes4(self):
        assert self.f.add(R2Point(0.4, 1.0)).add(R2Point(1.0, 0.4)).add(
            R2Point(0.8, 0.9)).add(R2Point(0.9, 0.8)).points.size() == 7
        assert self.f.add(R2Point(2.0, 2.0)).points.size() == 4

    def test_vertexes5(self):
        self.f.add(R2Point(0.8, -1.7))
        self.f.add(R2Point(-0.2, -1.2))
        self.f.add(R2Point(3.2, 1.6))
        self.f.add(R2Point(-3.3, -4.6))
        self.f.add(R2Point(-3.8, -3.4))
        self.f.add(R2Point(5.7, 1.5))
        assert self.f.points.size() == 5

    # Изменение периметра многоугольника
    #   изначально он равен сумме длин сторон
    def test_perimeter1(self):
        assert self.f.perimeter() == approx(2.0 + sqrt(2.0))

    #   добавление точки может его изменить
    def test_perimeter2(self):
        assert self.f.add(R2Point(1.0, 1.0)).perimeter() == approx(4.0)

    # Изменение площади многоугольника
    #   изначально она равна (неориентированной) площади треугольника
    def test_аrea1(self):
        assert self.f.area() == approx(0.5)

    #   добавление точки может увеличить площадь

    def test_area2(self):
        assert self.f.add(R2Point(1.0, 1.0)).area() == approx(1.0)

    # Изменение числа правильных углов многоугольника
    #   изначально их может быть ноль
    def test_angle_number1(self):
        assert self.f.angle_number() == 0

    #   добавление точки может изменить количество правильных углов
    def test_angle_number2(self):
        self.f.add(R2Point(-0.5, -0.5))
        assert self.f.angle_number() == 3

    #   добавление точки может изменить количество правильных углов
    def test_angle_number3(self):
        self.f.add(R2Point(1.5, 1.5))
        assert self.f.angle_number() == 1

    #   добавление точки может не изменить количество правильных углов
    def test_angle_number4(self):
        self.f.add(R2Point(1., 1.))
        assert self.f.angle_number() == 0

    #   добавление точки может изменить количество правильных углов
    def test_angle_number5(self):
        self.f.add(R2Point(1.5, 1.5))
        assert self.f.angle_number() == 1

    def test_angle_number6(self):
        self.f.add(R2Point(0., 2.5))
        self.f.add(R2Point(2., -1.))
        self.f.add(R2Point(-1., -1.5))
        assert self.f.angle_number() == 2

    def test_angle_number7(self):
        self.f.add(R2Point(-0.5, 2.0))
        self.f.add(R2Point(-1.0, 0.0))
        self.f.add(R2Point(-1.5, 1.0))
        assert self.f.angle_number() == 2

    def test_angle_number8(self):
        self.f.add(R2Point(0.0, -1.5))
        self.f.add(R2Point(2.0, 1.0))
        self.f.add(R2Point(2.5, 0.0))
        self.f.add(R2Point(-1.5, 1.0))
        self.f.add(R2Point(-1.0, -1.0))
        self.f.add(R2Point(0.0, 1.5))
        self.f.add(R2Point(1.5, -1.5))
        assert self.f.angle_number() == 0

    def test_angle_number9(self):
        self.f.add(R2Point(0.8, -1.7))
        self.f.add(R2Point(-0.2, -1.2))
        self.f.add(R2Point(3.2, 1.6))
        self.f.add(R2Point(-3.3, -4.6))
        self.f.add(R2Point(-3.8, -3.4))
        self.f.add(R2Point(5.7, 1.5))
        assert self.f.angle_number() == 1

    def test_angle_number10(self):
        self.f.add(R2Point(0.5, 2.6))
        self.f.add(R2Point(3.0, -3.4))
        self.f.add(R2Point(-4.1, 4.4))
        self.f.add(R2Point(-0.3, -4.3))
        self.f.add(R2Point(-2.2, -5.0))
        self.f.add(R2Point(-5.5, 1.3))
        assert self.f.angle_number() == 1

    def test_angle_number11(self):
        self.f = Polygon(R2Point(-1.0, 0.0), R2Point(2.0, -1.0),
                         R2Point(1.0, 2.0))
        self.f.add(R2Point(-5.0, -2.0))
        assert self.f.angle_number() == 2

    def test_angle_number12(self):
        self.f = Polygon(R2Point(-3.0, -2.0), R2Point(0.0, 0.0),
                         R2Point(-4.0, 0.0))
        self.f.add(R2Point(-5.0, 1.0))
        assert self.f.angle_number() == 0

    def test_angle_number13(self):
        self.f = Polygon(R2Point(4.0, 0.0), R2Point(2.0, 3.0),
                         R2Point(0.0, 0.0))
        self.f.add(R2Point(-3.0, -1.0))
        assert self.f.angle_number() == 2
