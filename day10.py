import unittest
import numpy as np


def unroll(numbers, sequence):
    count = sum(sequence) + sum(range(len(sequence)))
    return np.roll(numbers, count)


def apply(numbers, sequence):
    for (skip_size, seq) in enumerate(sequence):
        assert seq <= len(numbers)
        numbers[0:seq] = numbers[0:seq][::-1]
        numbers = np.roll(numbers, -(skip_size + seq))

    return numbers


class Day10(unittest.TestCase):
    def setUp(self):
        self.example = np.arange(5)

        self.data = np.arange(256)
        self.sequence = [147, 37, 249, 1, 31, 2, 226, 0, 161, 71, 254, 243, 183, 255, 30, 70]

    def test_apply_one(self):
        ret = apply(self.example, [3])
        np.testing.assert_array_equal(ret, [3, 4, 2, 1, 0])

    def test_unroll_one(self):
        ret = unroll(np.array([3, 4, 2, 1, 0]), [3])
        np.testing.assert_array_equal([2, 1, 0, 3, 4], ret)

    def test_apply_all(self):
        ret = apply(self.example, [3, 4, 1, 5])
        np.testing.assert_array_equal([0, 3, 4, 2, 1], ret)

    def test_unroll_all(self):
        sequence = [3, 4, 1, 5]
        ret = apply(self.example, sequence)
        ret = unroll(ret, sequence)
        np.testing.assert_array_equal([3, 4, 2, 1, 0], ret)

    def test_complete(self):
        roll = apply(self.data, self.sequence)
        ret = unroll(roll, self.sequence)

        val = ret[0] * ret[1]
        self.assertEqual(37230, val)
