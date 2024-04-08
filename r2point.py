from math import sqrt


class R2Point:
    """ Точка (Point) на плоскости (R2) """

    # Конструктор
    def __init__(self, x=None, y=None):
        if x is None:
            x = float(input("x -> "))
        if y is None:
            y = float(input("y -> "))
        self.x, self.y = x, y

    # Текстовое отображение
    def __repr__(self):  # pragma: no cover
        return f'({self.x}, {self.y})'

    # Разность радиус-векторов
    def __sub__(self, other):
        return R2Point(self.x - other.x, self.y - other.y)

    # Скалярное произведение радиус-векторов
    def __mul__(self, other):
        return self.x * other.x + self.y * other.y

    # Третья компонента векторного произведения радиус-векторов
    @staticmethod
    def cross_z(a, b):
        return a.x * b.y - a.y * b.x

    # Площадь треугольника
    @staticmethod
    def area(a, b, c):
        return 0.5 * R2Point.cross_z(a - c, b - c)

    # Лежат ли точки на одной прямой?
    @staticmethod
    def is_triangle(a, b, c):
        return R2Point.area(a, b, c) != 0.0

    # Расстояние до другой точки
    def dist(self, other):
        return sqrt((other.x - self.x)**2 + (other.y - self.y)**2)

    # Лежит ли точка внутри "стандартного" прямоугольника?
    def is_inside(self, a, b):
        return (((a.x <= self.x and self.x <= b.x) or
                 (a.x >= self.x and self.x >= b.x))
                and ((a.y <= self.y and self.y <= b.y) or
                     (a.y >= self.y and self.y >= b.y)))

    # Освещено ли из данной точки ребро (a,b)?
    def is_light(self, a, b):
        s = R2Point.area(a, b, self)
        return s < 0.0 or (s == 0.0 and not self.is_inside(a, b))

    # Совпадает ли точка с другой?
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.x == other.x and self.y == other.y
        return False

    # Угол при вершине острый и больший 45 градусов
    def good(self, a, b):
        return abs(R2Point.cross_z(a - self,
                                   b - self)) > (a - self) * (b - self) > 0


if __name__ == "__main__":  # pragma: no cover
    x = R2Point(1.0, 1.0)
    print(type(x), x.__dict__)
    print(x.dist(R2Point(1.0, 0.0)))
    a, b, c = R2Point(0.0, 0.0), R2Point(1.0, 0.0), R2Point(1.0, 1.0)
    print(R2Point.area(a, c, b))
