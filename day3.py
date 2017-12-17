import unittest


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


if __name__ == '__main__':
    unittest.main()
