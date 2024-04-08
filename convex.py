from deq import Deq
from r2point import R2Point


class Figure:
    """ Абстрактная фигура """

    def perimeter(self):
        return 0.0

    def area(self):
        return 0.0

    def angle_number(self):
        return 0


class Void(Figure):
    """ "Hульугольник" """

    def add(self, p):
        return Point(p)


class Point(Figure):
    """ "Одноугольник" """

    def __init__(self, p):
        self.p = p

    def add(self, q):
        return self if self.p == q else Segment(self.p, q)


class Segment(Figure):
    """ "Двуугольник" """

    def __init__(self, p, q):
        self.p, self.q = p, q

    def perimeter(self):
        return 2.0 * self.p.dist(self.q)

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            return Polygon(self.p, self.q, r)
        elif self.q.is_inside(self.p, r):
            return Segment(self.p, r)
        elif self.p.is_inside(r, self.q):
            return Segment(r, self.q)
        else:
            return self


class Polygon(Figure):
    """ Многоугольник """

    def __init__(self, a, b, c):
        self.points = Deq()
        self.points.push_first(b)
        if b.is_light(a, c):
            self.points.push_first(a)
            self.points.push_last(c)
        else:
            self.points.push_last(a)
            self.points.push_first(c)
        self._perimeter = a.dist(b) + b.dist(c) + c.dist(a)
        self._area = abs(R2Point.area(a, b, c))
        self._angle_number = sum(1 for i, ii, iii in ((a, b, c), (a, c, b),
                                                      (b, a, c))
                                 if ii.good(i, iii))

    def __repr__(self):  # pragma: no cover
        return (f'Polygon {self.perimeter()=} {self.area()=} ' +
                f'{self.angle_number()=} {self.points}')

    def perimeter(self):
        return self._perimeter

    def area(self):
        return self._area

    def angle_number(self):
        return self._angle_number

    # добавление новой точки
    def add(self, newcomer):

        # поиск освещённого ребра
        for n in range(self.points.size()):
            if newcomer.is_light(self.points.last(), self.points.first()):
                break
            # циклический сдвиг дека
            self.points.push_last(self.points.pop_first())

        # хотя бы одно освещённое ребро есть
        if newcomer.is_light(self.points.last(), self.points.first()):

            # учёт удаления ребра, соединяющего конец и начало дека
            self._perimeter -= self.points.first().dist(self.points.last())
            self._area += abs(
                R2Point.area(newcomer, self.points.last(),
                             self.points.first()))
            # флаг первого удаления
            firstdeletion = True

            # удаление освещённых рёбер из начала дека
            current = self.points.pop_first()
            while newcomer.is_light(current, self.points.first()):
                self._perimeter -= current.dist(self.points.first())
                self._area += abs(
                    R2Point.area(newcomer, current, self.points.first()))
                if firstdeletion:
                    firstdeletion = False
                    if current.good(self.points.first(), self.points.last()):
                        self._angle_number -= 1
                    tempvert = self.points.pop_last()
                    if tempvert.good(current, self.points.last()):
                        self._angle_number -= 1
                    self.points.push_last(tempvert)
                if self.points.size() >= 2:
                    tempvert = self.points.pop_first()
                    if tempvert.good(self.points.first(), current):
                        self._angle_number -= 1
                    self.points.push_first(tempvert)
                current = self.points.pop_first()

            # учёт нового угла с левого края дека
            if current.good(self.points.first(), newcomer):
                self._angle_number += 1

            # возвращение крайней левой вершины в дек
            self.points.push_first(current)

            # удаление освещённых рёбер из конца дека
            current = self.points.pop_last()
            while newcomer.is_light(self.points.last(), current):
                self._perimeter -= current.dist(self.points.last())
                self._area += abs(
                    R2Point.area(newcomer, current, self.points.last()))
                if firstdeletion:
                    firstdeletion = False
                    if current.good(self.points.first(), self.points.last()):
                        self._angle_number -= 1
                    tempvert = self.points.pop_first()
                    if tempvert.good(self.points.first(), current):
                        self._angle_number -= 1
                    self.points.push_first(tempvert)
                if self.points.size() >= 2:
                    tempvert = self.points.pop_last()
                    if tempvert.good(current, self.points.last()):
                        self._angle_number -= 1
                    self.points.push_last(tempvert)
                current = self.points.pop_last()

            # учёт старых углов при вершинах по краям дека
            # в случае, если все прежние вершины оболочки сохранились
            if firstdeletion:
                if current.good(self.points.first(), self.points.last()):
                    self._angle_number -= 1
                tempvert = self.points.pop_first()
                if tempvert.good(self.points.first(), current):
                    self._angle_number -= 1
                self.points.push_first(tempvert)
            # учёт нового угла с правого края дека
            if current.good(newcomer, self.points.last()):
                self._angle_number += 1
            self.points.push_last(current)

            # добавление двух новых рёбер
            self._perimeter += newcomer.dist(
                self.points.first()) + newcomer.dist(self.points.last())

            # добавление подходящего угла при новой вершине
            if newcomer.good(self.points.last(), self.points.first()):
                self._angle_number += 1
            # помещение новой вершины в дек оболочки
            self.points.push_first(newcomer)

        return self


if __name__ == "__main__":  # pragma: no cover
    f = Void()
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(1.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 1.0))
    print(type(f), f.__dict__)
