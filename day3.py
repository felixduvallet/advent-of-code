import unittest

import numpy as np


def corner_above(number):
    # Returns the value of the corner "after" the given value, and the corner's L1 distance to the center.
    for (idx, odds) in enumerate(xrange(1, 1000, 2)):
        if odds**2 >= number:
            return odds ** 2, idx * 2
    raise AssertionError


def l1_distance(number):
    (squared, length) = corner_above(number)
    diff = squared - number

    offset = 0
    if diff > 0:  # Don't divide by zero.
        (quotient, remainder) = divmod(diff, length)
        offset = min(remainder, length-remainder)

    return length - offset


class TestSpiral(unittest.TestCase):

    def test_input(self):
        self.assertEqual(475, l1_distance(277678))

    def test_corner(self):
        self.assertEqual((9, 2), corner_above(6))
        self.assertEqual((25, 4), corner_above(14))
        self.assertEqual((49, 6), corner_above(26))
        self.assertEqual((49, 6), corner_above(49))
        self.assertEqual((1, 0), corner_above(1))

    def test_26(self):
        self.assertEqual(5, l1_distance(26))

    def test_1(self):
        self.assertEqual(0, l1_distance((1)))

    def test_12(self):
        self.assertEqual(3, l1_distance((12)))

    def test_23(self):
        self.assertEqual(2, l1_distance((23)))

    def test_1024(self):
        self.assertEqual(31, l1_distance((1024)))

    def test_corners(self):
        self.assertEqual(2, l1_distance(9))
        self.assertEqual(4, l1_distance(25))
        self.assertEqual(6, l1_distance(49))
        self.assertEqual(8, l1_distance(81))


"""
For part two, take a complete different approach: build up the matrix of value.

Do this by walking along the edges of the spiral, setting the value at each position
to the sum of the values around it.

Store the values in a numpy matrix with an offset to the center (0, 0) coordinate.

"""

def set(val, matrix, (i, j), offset):
    assert i + offset < matrix.shape[0]
    assert j + offset < matrix.shape[1]

    matrix[i + offset, j+offset] = val


def get_range(matrix, (i, j), offset):
    assert i + offset + 1 < matrix.shape[0]
    assert j + offset + 1< matrix.shape[1]

    return matrix[i + offset - 1 : i + offset + 2, j + offset - 1 : j + offset + 2]


def create_spiral(max_num):

    offset = 5
    matrix = np.zeros((2*offset + 1, 2*offset + 1))

    di_dj_store = [(0, 1), (-1, 0), (0, -1), (1, 0)]

    i, j = 0, 0
    counter = 0
    set(1, matrix, (i, j), offset)
    max_val = np.max(matrix)

    while max_val <= max_num:

        # Pick the current dimension.
        (di, dj) = di_dj_store[counter % 4]

        # dx is the number of spaces to advance along the current dimension.
        dx = counter // 2 + 1

        # Advance 'dx' spaces along this dimensions.
        for _ in range(dx):
            i += di
            j += dj

            # Compute the sum of all values in a 3x3 submatrix around the current point.
            submat = get_range(matrix, (i, j), offset)
            total = np.sum(submat)

            set(total, matrix, (i, j), offset)

            max_val = total

            if max_val > max_num:
                break

        counter += 1

    return matrix


class TestCreateSpiral(unittest.TestCase):
    def test_create_11(self):
        matrix = create_spiral(11)
        self.assertEqual(23, np.max(matrix))

    def test_create_747(self):
        matrix = create_spiral(747)
        self.assertEqual(806, np.max(matrix))

    def test_create_277678(self):
        matrix = create_spiral(277678)
        self.assertEqual(279138, np.max(matrix))


if __name__ == '__main__':
    unittest.main()
