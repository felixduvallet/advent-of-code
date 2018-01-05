import unittest

from data import day11 as day11_data

"""
Compute the distance on a hexagonal grid

Represent the coordinates of the grid using Cube coordinates, using the tuple (x, y, z) where x + y + z = 0.

With this representation, moves are an addition, and the distance to the origin is simply the maximum (absolute) value
of the coordinate.

"""


class Cube(object):
    x = 0
    y = 0
    z = 0

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def add(self, x, y, z):
        self.x += x
        self.y += y
        self.z += z

    @property
    def tuple(self):
        return self.x, self.y, self.z

    @property
    def distance(self):
        return max(abs(self.x), abs(self.y), abs(self.z))


# Delta x/y/z when moving in that particular direction. NOTE: flat-topped hexagons.
movement = {
    'ne': (1, 0, -1),
    'se': (1, -1, 0),
    's': (0, -1, 1),
    'sw': (-1, 0, 1),
    'nw': (-1, 1, 0),
    'n': (0, 1, -1)
}


def move_sequence(cube, command):
    sequence = command.split(',')
    for s in sequence:
        assert s in movement
        cube.add(*movement[s])
    return cube


def move_sequence_max_dist(cube, command):
    sequence = command.split(',')
    max_dist = 0
    for s in sequence:
        assert s in movement
        cube.add(*movement[s])
        max_dist = max(max_dist, cube.distance)
    return cube, max_dist


class TestHexagons(unittest.TestCase):
    def test_move(self):
        c = Cube(0, 0, 0)
        c.add(*movement['n'])
        self.assertEqual(movement['n'], c.tuple)

    def test_cube(self):
        t = (1, 2, 3)
        c = Cube(*t)
        self.assertEqual(t, c.tuple)

        c.add(2, 3, 4)
        self.assertEqual((3, 5, 7), c.tuple)

    def test_distance(self):
        c = Cube(-5, 3, 1)
        self.assertEqual(5, c.distance)

    def test_example1(self):
        c = Cube()
        ret = move_sequence(c, 'ne,ne,ne')
        self.assertEqual(3, ret.distance)
        self.assertEqual((3, 0, -3), ret.tuple)

    def test_examples(self):
        ret = move_sequence(Cube(), 'ne,ne,sw,sw')
        self.assertEqual(0, ret.distance)

        ret = move_sequence(Cube(), 'ne,ne,s,s')
        self.assertEqual(2, ret.distance)

        ret = move_sequence(Cube(), 'se,sw,se,sw,sw')
        self.assertEqual(3, ret.distance)

    def test_data(self):
        ret = move_sequence(Cube(), day11_data)
        self.assertEqual(759, ret.distance)

    def test_data_max(self):
        (cube, max_dist) = move_sequence_max_dist(Cube(), day11_data)
        self.assertEqual(759, cube.distance)
        self.assertEqual(1501, max_dist)


if __name__ == '__main__':
    unittest.main()
