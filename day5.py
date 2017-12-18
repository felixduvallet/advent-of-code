import unittest

from data import day5 as day5_data

example_input = """0
3
0
1
-3"""



def convert(string):
    s = [int(x) for x in string.split('\n')]
    return s


def execute(string, simple=True):
    index = 0
    count = 0

    numbers = convert(string)

    while 0 <= index < len(numbers):
        if count < 100 or count % 1000 == 0:
            print('[{}, {}] - {}'.format(index, count, numbers))

        delta = numbers[index]

        offset = 1

        if not simple and delta >= 3:
            offset = -1

        numbers[index] += offset
        index += delta

        count += 1
    return count


class Day5(unittest.TestCase):
    def test_convert(self):
        self.assertEqual([0, 3, 0, 1, -3], convert(example_input))

    def test_execute(self):
        self.assertEqual(5, execute(example_input))

    def test_execute_data(self):
        self.assertEqual(373160, execute(day5_data))

    def test_execute_complex(self):
        self.assertEqual(10, execute(example_input, False))

    def ztest_execute_data_complex(self):
        self.assertEqual(373160, execute(day5_data, False))


def run():
    #ret = execute(day5_data, False)
    ret = execute(example_input, False)
    print(ret)

if __name__ == '__main__':
    #unittest.main()
    run()
